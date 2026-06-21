# -*- coding: utf-8 -*-
# mobile_app.py (النسخة الإمبراطورية الكاملة للموبايل - نظام البيع والمشتريات والمخزن والعملاء المحمي 🚀)

import streamlit as st
import datetime
import urllib.parse
import hashlib
from supabase import create_client
import pandas as pd

# 1. إعدادات الشاشة لتناسب الموبايل أوتوماتيكياً وتفتح بشكل Centered متناسق
st.set_page_config(
    page_title="Dental Box Mobile",
    page_icon="🦷",
    layout="centered"
)

# 2. التنسيق البرمجي الفخم والإضاءة الكاملة للكروت والخطوط البيضاء الواضحة 🌟
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    
    /* ستايل كروت الإحصائيات المضيئة المصلحة تماماً */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e3a8a, #0284c7) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricLabel"] { 
        color: #e0f2fe !important; 
        font-weight: bold !important; 
        font-size: 16px !important; 
    }
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-size: 26px !important; 
        font-weight: 900 !important;
    }
    
    h1, h2, h3, p, div, label { text-align: right; direction: rtl; font-family: 'Cairo', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 15px; }
    
    /* تنسيق الأزرار الملوكية للموبايل */
    .stButton>button {
        background-color: #1a9eff !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إعدادات ربط السيرفر السحابي المستقل (Supabase)
SUPABASE_URL = "https://tjviltavsumuilevcokh.supabase.co"
SUPABASE_KEY = "sb_secret_hT5IIyZF-EIjGtDalfq16g_gbQGV6G5"

@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# 🔐 إدارة جلسة تسجيل الدخول لحماية أرباحك وبياناتك
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 🚪 شاشة تسجيل الدخول المرتبطة بجدول الموظفين أونلاين
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول للنظام السحابي</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>يرجى إدخال بيانات حسابك المعتمد في Dental Box</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username_input = st.text_input("👤 اسم المستخدم (اليوزر):")
        password_input = st.text_input("🔑 كلمة المرور (الباسورد):", type="password")
        submit_login = st.form_submit_button("🔓 دخول آمن للسيستم", use_container_width=True)
        
        if submit_login:
            if username_input and password_input:
                try:
                    hashed_input = hashlib.sha256(password_input.encode()).hexdigest().lower()
                    res = supabase.table('users').select('password, full_name').eq('username', username_input).execute()
                    
                    if res.data and res.data[0]['password'].lower() == hashed_input:
                        st.session_state['logged_in'] = True
                        st.session_state['user_full_name'] = res.data[0]['full_name']
                        st.success(f"🎉 أهلاً بك دكتور {res.data[0]['full_name']}...")
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")
                except Exception as e:
                    st.error(f"فشل التحقق الأمني: {str(e)}")
            else:
                st.warning("⚠️ يرجى ملء الحقول المطلوبة!")
else:
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🦷 فتح النظام الإمبراطوري بالكامل بعد الدخول الناجح
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown("<h1 style='text-align: center;'>🦷 لوحة تحكم Dental Box الكاملة</h1>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 خروج آمن"):
        st.session_state['logged_in'] = False
        st.rerun()

    # 📱 الـ 5 شاشات الأساسية المطابقة للكمبيوتر بالظبط لتسهيل اللمس
    tab_dashboard, tab_new_invoice, tab_add_product, tab_stock, tab_customers = st.tabs([
        "📊 الأرباح", 
        "🛒 فاتورة جديدة", 
        "➕ صنف جديد",
        "📦 جرد المخزن", 
        "👥 العملاء"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1️⃣ Tab 1: لوحة التحكم المالي والأرباح
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_dashboard:
        st.markdown("### 📊 الأداء المالي العام")
        try:
            res = supabase.table('invoices').select('final_total, total_profit, date').execute()
            invoices = res.data if res.data else []
            
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            today_revenue = 0.0
            all_time_profit = 0.0
            total_inv_count = len(invoices)
            
            for inv in invoices:
                final_total = float(inv.get('final_total', 0) or 0)
                profit_val = float(inv.get('total_profit', 0) or 0)
                all_time_profit += profit_val
                if inv.get('date') == today_str:
                    today_revenue += final_total
                    
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="💰 مبيعات اليوم الحالي", value=f"{today_revenue:.2f} ج.م")
            with col2:
                st.metric(label="💸 إجمالي صافي الأرباح", value=f"{all_time_profit:.2f} ج.م")
            st.metric(label="📄 إجمالي عدد الفواتير الناجحة", value=f"{total_inv_count} فاتورة صادرة")
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 2️⃣ Tab 2: إنشاء فاتورة بيع مبيعات جديدة بالكامل من الموبايل 🛒
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_new_invoice:
        st.markdown("### 🛒 إصدار فاتورة مبيعات سحابية جديدة")
        
        # إنشاء رقم فاتورة تلقائي ذكي للموبايل
        generated_inv_num = f"INV-MOB-{datetime.datetime.now().strftime('%M%S')}"
        st.subheader(f"📄 رقم الفاتورة: {generated_inv_num}")
        
        inv_cust_name = st.text_input("👤 السيد الدكتور / العيادة:", value="عميل نقدي")
        inv_cust_phone = st.text_input("📱 رقم هاتف الدكتور:")
        
        # جلب المنتجات لكي نختار منها في الفاتورة باللمس
        try:
            prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').execute()
            all_prods = prod_res.data if prod_res.data else []
            
            if all_prods:
                prod_options = {p['name']: p for p in all_prods}
                selected_item_name = st.selectbox("📦 اختر المستلزم الطبي المراد بيعه:", list(prod_options.keys()))
                
                item_details = prod_options[selected_item_name]
                max_available = int(item_details['quantity'] or 0)
                st.caption(f"📊 الكمية المتاحة على الرف حالياً: {max_available} وحدة")
                
                # منع البيع إذا كان المنتج صفر 🛑
                if max_available <= 0:
                    st.error("⚠️ عذراً دكتور، هذا المنتج نفد تماماً من المخزن (0 وحدة)؛ لا يمكن بيعه!")
                else:
                    qty_to_sell = st.number_input("🔢 الكمية المطلوبة:", min_value=1, max_value=max_available, step=1, value=1)
                    discount_input = st.number_input("📉 الخصم الممنوح للفاتورة (ج.م):", min_value=0.0, step=5.0, value=0.0)
                    
                    # الحسابات الآلية الفورية
                    unit_selling_price = float(item_details['selling_price'] or 0)
                    unit_purchase_price = float(item_details['purchase_price'] or 0)
                    
                    sub_total = unit_selling_price * qty_to_sell
                    final_total_bill = sub_total - discount_input
                    
                    # حسبة صافي ربح الفاتورة الذكي = (سعر البيع - سعر الشراء) * الكمية - الخصم
                    invoice_profit = ((unit_selling_price - unit_purchase_price) * qty_to_sell) - discount_input
                    invoice_profit = max(0.0, invoice_profit)
                    
                    st.write(f"💵 الإجمالي المبدئي: {sub_total:.2f} ج.م")
                    st.markdown(f"### 🎯 الصافي المطلوب: {final_total_bill:.2f} ج.م")
                    
                    if st.button("💾 ترحيل الفاتورة وحفظها في السحاب", use_container_width=True):
                        # 1. إدراج الفاتورة في جدول invoices
                        supabase.table('invoices').insert({
                            'invoice_num': generated_inv_num,
                            'customer_name': inv_cust_name if inv_cust_name else "عميل نقدي",
                            'phone_num': inv_cust_phone if inv_cust_phone else "بدون",
                            'date': datetime.date.today().strftime('%Y-%m-%d'),
                            'total': sub_total,
                            'discount': discount_input,
                            'final_total': final_total_bill,
                            'total_profit': invoice_profit
                        }).execute()
                        
                        # 2. إدراج المواد المباعة في جدول invoice_items
                        supabase.table('invoice_items').insert({
                            'invoice_num': generated_inv_num,
                            'product_code': item_details['code'],
                            'product_name': selected_item_name,
                            'quantity': qty_to_sell,
                            'unit_price': unit_selling_price,
                            'total_price': sub_total
                        }).execute()
                        
                        # 3. خصم الكمية المباعة من جدول المنتجات فوراً
                        new_stock_qty = max_available - qty_to_sell
                        supabase.table('products').update({'quantity': new_stock_qty}).eq('code', item_details['code']).execute()
                        
                        st.success("🎉 تم إصدار الفاتورة السحابية بنجاح وخصم الكمية من المخزن!")
                        st.rerun()
            else:
                st.warning("لا توجد منتجات بالمخزن للبيع!")
        except Exception as e:
            st.error(f"فشلت العملية: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ Tab 3: إضافة وتسجيل صنف ومنتج جديد تماماً من التليفون ➕
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_add_product:
        st.markdown("### ➕ تسجيل صنف جديد في مخزن مستلزمات الأسنان")
        with st.form("add_new_product_form"):
            new_p_code = st.text_input("📝 كود المنتج / الباركود (أو اكتب كود فريد):")
            new_p_name = st.text_input("📦 اسم المنتج / المادة:")
            new_p_cat = st.text_input("🗂️ الفئة (مثال: حشوات، أدوات جراحة):")
            new_p_purchase = st.number_input("💰 سعر الشراء الأصلي (ج.م):", min_value=0.0, step=10.0, value=0.0)
            new_p_selling = st.number_input("💵 سعر البيع للعيادات (ج.م):", min_value=0.0, step=10.0, value=0.0)
            new_p_qty = st.number_input("🔢 الكمية الابتدائية المتوفرة:", min_value=0, step=1, value=10)
            
            submit_new_prod = st.form_submit_button("📥 إدراج الصنف في مخزن السحاب", use_container_width=True)
            
            if submit_new_prod:
                if new_p_code and new_p_name:
                    try:
                        # التحقق إذا كان الكود موجود مسبقاً
                        check_exist = supabase.table('products').select('id').eq('code', new_p_code).execute()
                        if check_exist.data:
                            st.error("⚠️ هذا الكود مسجل مسبقاً لصنف آخر! استخدم كود مختلف.")
                        else:
                            supabase.table('products').insert({
                                'code': new_p_code,
                                'name': new_p_name,
                                'category': new_p_cat,
                                'purchase_price': new_p_purchase,
                                'selling_price': new_p_selling,
                                'quantity': new_p_qty
                            }).execute()
                            st.success(f"✅ تم حفظ المنتج الجديد ({new_p_name}) بنجاح في السحاب!")
                    except Exception as e:
                        st.error(f"فشل الحفظ: {str(e)}")
                else:
                    st.warning("⚠️ يرجى كتابة كود واسم المنتج على الأقل!")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4️⃣ Tab 4: جرد أصناف المخزن ومراقبة النواقص وتزويد المشتريات
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_stock:
        st.markdown("### 📦 كميات المواد الحالية وتزويد المشتريات")
        try:
            prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').order('id').execute()
            products_data = prod_res.data if prod_res.data else []
            
            if products_data:
                df = pd.DataFrame(products_data)
                df.columns = ["كود الصنف", "اسم المنتج", "سعر الشراء", "سعر البيع", "الكمية المتاحة"]
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # قسم سريع لتزويد بضاعة مشتريات فورية باللمس للأصناف الموجودة
                st.markdown("---")
                st.markdown("##### 📥 تزويد بضاعة سريعة لصنف موجود:")
                prod_options_p = {p['name']: (p['code'], p['quantity']) for p in products_data}
                selected_prod_p = st.selectbox("اختر الصنف المراد تزويده:", list(prod_options_p.keys()))
                
                if selected_prod_p:
                    c_code, c_qty = prod_options_p[selected_prod_name := selected_prod_p]
                    new_units = st.number_input("عدد الوحدات الجديدة المشتراة:", min_value=1, step=1, value=5)
                    
                    if st.button("📥 تحديث كمية الرف الفوري", use_container_width=True):
                        supabase.table('products').update({'quantity': (c_qty + new_units)}).eq('code', c_code).execute()
                        st.success("✅ تم تحديث كمية المخزن السحابي فوراً!")
                        st.rerun()
            else:
                st.info("المخزن فارغ حالياً.")
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 5️⃣ Tab 5: سجل العملاء وإرسال رسائل الواتساب الفخمة شاملة الـ ID والحجوزات
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_customers:
        st.markdown("### 👥 سجل العيادات والرسائل الفورية")
        try:
            cust_res = supabase.table('customers').select('id, name, phone, balance').order('id').execute()
            customers_data = cust_res.data if cust_res.data else []
            
            if customers_data:
                for cust in customers_data:
                    c_id = cust['id']
                    c_name = cust['name']
                    c_phone = cust['phone']
                    c_res = cust.get('balance', 'لا توجد طلبات محجوزة حالياً') or 'لا توجد طلبات محجوزة حالياً'
                    
                    with st.expander(f"👤 د. {c_name} (ID: {c_id})"):
                        st.write(f"📱 **رقم الجوال:** {c_phone}")
                        st.write(f"📋 **المحجوزات الحالية:** {c_res}")
                        
                        msg = (
                            f"🦷 *نظام Dental Box لمستلزمات الأسنان* 🦷\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"أهلاً دكتور *{c_name}*، يسعدنا تواصلكم معنا عبر النظام السحابي.\n\n"
                            f"🆔 *رقم المعرف الخاص بك:* {c_id}\n"
                            f"📋 *المنتجات والمواد المحجوزة لعيادتكم حالياً:*\n• {c_res.replace(' ، ', '\n• ').replace(' || ', '\n• ')}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"تم قيد حجزكم وتجهيز طلباتكم مسبقاً بنجاح دكتور، يرجى إفادتنا بأي مستلزمات طبية إضافية تحتاجونها لعيادتكم الموقرة."
                        )
                        encoded_msg = urllib.parse.quote(msg)
                        whatsapp_url = f"https://api.whatsapp.com/send?phone={c_phone.replace('+', '').replace(' ', '')}&text={encoded_msg}"
                        
                        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#10b981; color:white; border:none; padding:10px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 إرسال تفاصيل الحجز عبر واتساب</button></a>', unsafe_allow_html=True)
            else:
                st.info("لا يوجد عملاء مسجلين.")
        except Exception as e:
            st.error(f"خطأ: {str(e)}")
