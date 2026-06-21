# -*- coding: utf-8 -*-
# mobile_app.py (تطبيق الموبايل السحابي - نسخة الحماية الملوكية والخطوط المضيئة 🚀)

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

# 2. التنسيق البرمجي الفخم وتفتيح ألوان الكروت والخطوط لتظهر بوضوح شديد 🌟
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    
    /* تعديل كروت الإحصائيات لتظهر بخلفية فخمة وخطوط بيضاء مضيئة الواضحة 100% */
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
        font-size: 18px !important; 
    }
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-size: 28px !important; 
        font-weight: 900 !important;
    }
    
    h1, h2, h3, p, div { text-align: right; direction: rtl; font-family: 'Cairo', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 16px; }
    
    /* تنسيق صندوق تسجيل الدخول */
    .login-box {
        background-color: #1e293b;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #1a9eff;
        margin-top: 20px;
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

# 🔐 إدارة نظام جلسة تسجيل الدخول لحماية التطبيق
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 🚪 شاشة تسجيل الدخول الملوكية المطابقة لقاعدة البيانات
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
                    # تشفير المدخلات لمطابقتها مع السحاب SHA-256
                    hashed_input = hashlib.sha256(password_input.encode()).hexdigest().lower()
                    
                    # البحث عن المستخدم في جدول users السحابي
                    res = supabase.table('users').select('password, full_name, role').eq('username', username_input).execute()
                    
                    if res.data and res.data[0]['password'].lower() == hashed_input:
                        st.session_state['logged_in'] = True
                        st.session_state['user_full_name'] = res.data[0]['full_name']
                        st.success(f"🎉 أهلاً بك دكتور {res.data[0]['full_name']}، جاري فتح النظام...")
                        st.rerun()
                    else:
                        st.error("❌ عذراً دكتور، اسم المستخدم أو كلمة المرور غير صحيحة!")
                except Exception as e:
                    st.error(f"فشل التحقق الأمني: {str(e)}")
            else:
                st.warning("⚠️ يرجى ملء الحقول المطلوبة للدخول!")
else:
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🦷 النظام الأساسي يفتح بالكامل فقط بعد تسجيل الدخول الناجح
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown("<h1 style='text-align: center;'>🦷 لوحة تحكم Dental Box للموبايل</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #10b981; font-weight: bold;'>👋 مرحباً دكتور {st.session_state['user_full_name']} | متصل أونلاين بنجاح</p>", unsafe_allow_html=True)
    
    # زر تسجيل الخروج لقفل التطبيق عند الانتهاء
    if st.sidebar.button("🚪 تسجيل الخروج الآمن"):
        st.session_state['logged_in'] = False
        st.rerun()

    # تقسيم الشاشة لتبويبات (Tabs) مريحة للّمس على الموبايل
    tab_dashboard, tab_stock, tab_customers, tab_purchase = st.tabs([
        "📊 الأرباح والمبيعات", 
        "📦 جرد المخزن", 
        "👥 سجل العملاء", 
        "📥 إضافة مشتريات"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Tab 1: لوحة التحكم المالي وإجمالي الأرباح الكلية
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_dashboard:
        st.markdown("### 📊 أداء النظام المالي العام")
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
                    
            # عرض البيانات في مربعات فخمة منيرة والخط أبيض ناصع وواضح جداً ديلوقتي ✨
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="💰 مبيعات اليوم الحالي", value=f"{today_revenue:.2f} ج.م")
            with col2:
                st.metric(label="💸 إجمالي صافي الأرباح", value=f"{all_time_profit:.2f} ج.م")
                
            st.metric(label="📄 إجمالي عدد الفواتير الناجحة", value=f"{total_inv_count} فاتورة صادرة")
            
        except Exception as e:
            st.error(f"فشل اتصال لوحة التحكم: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Tab 2: جرد أصناف المخزن ومراقبة النواقص
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_stock:
        st.markdown("### 📦 كميات المواد والمستلزمات الحالية")
        try:
            prod_res = supabase.table('products').select('code, name, selling_price, quantity').order('id').execute()
            products_data = prod_res.data if prod_res.data else []
            
            if products_data:
                df = pd.DataFrame(products_data)
                df.columns = ["كود الصنف", "اسم المنتج", "سعر البيع", "الكمية المتاحة"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("المخزن فارغ حالياً، لا توجد منتجات مسجلة.")
        except Exception as e:
            st.error(f"خطأ في قراءة المخزن: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Tab 3: سجل العملاء وإرسال رسائل الواتساب الفخمة
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_customers:
        st.markdown("### 👥 سجل العيادات وإرسال الحجوزات فوراً")
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
                st.info("سجل العملاء لا يحتوي على أطباء مسجلين.")
        except Exception as e:
            st.error(f"خطأ في سجل العملاء: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Tab 4: إضافة المشتريات وتزويد Bضاعة من الموبايل
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_purchase:
        st.markdown("### 📥 تزويد كميات المخزن أونلاين")
        try:
            prod_res = supabase.table('products').select('code, name, quantity').order('id').execute()
            all_prods = prod_res.data if prod_res.data else []
            
            if all_prods:
                prod_options = {p['name']: (p['code'], p['quantity']) for p in all_prods}
                selected_prod_name = st.selectbox("🎯 اختر المنتج المراد تزويده بضاعة جديدة:", list(prod_options.keys()))
                
                if selected_prod_name:
                    code, current_qty = prod_options[selected_prod_name]
                    st.warning(f"📉 المخزون الحالي الفعلي بالسحاب: {current_qty} unidade")
                    
                    new_qty_bought = st.number_input("➕ عدد الوحدات المشتراة الجديدة:", min_value=1, step=1, value=1)
                    
                    if st.button("📥 تحديث المخزن وتأكيد الشراء الفوري", use_container_width=True):
                        updated_total = current_qty + new_qty_bought
                        supabase.table('products').update({'quantity': updated_total}).eq('code', code).execute()
                        st.success(f"✅ تم الحفظ! الكمية الجديدة لـ ({selected_prod_name}) أصبحت: {updated_total} وحدة")
                        st.rerun()
            else:
                st.warning("لا توجد منتجات لتزويدها، أضف أصناف أولاً من الكمبيوتر.")
        except Exception as e:
            st.error(f"فشلت عملية المشتريات: {str(e)}")
