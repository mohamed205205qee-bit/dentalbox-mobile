# -*- coding: utf-8 -*-
# mobile_app.py (النسخة الإمبراطورية النهائية المستقرة - حل مشكلة حفظ السلة والتسجيل الفوري 🚀🛒📸)

import streamlit as st
import datetime
import urllib.parse
import hashlib
from supabase import create_client
import pandas as pd
import streamlit.components.v1 as components

# 1. إعدادات الشاشة لتناسب الموبايل أوتوماتيكياً
st.set_page_config(
    page_title="Dental Box Mobile",
    page_icon="🦷",
    layout="centered"
)

# 2. التنسيق البرمجي الملوكي وألوان الكروت المضيئة وشريط الليزر 🌟
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e3a8a, #0284c7) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricLabel"] { color: #e0f2fe !important; font-weight: bold !important; font-size: 15px !important; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 26px !important; font-weight: 900 !important; }
    h1, h2, h3, p, div, label { text-align: right; direction: rtl; font-family: 'Cairo', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 15px; }
    .stButton>button { background-color: #1a9eff !important; color: white !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; }
    
    /* تنسيق مربع السكنر الفخم */
    .scanner-container {
        position: relative;
        width: 100%;
        max-width: 400px;
        margin: auto;
        border-radius: 12px;
        overflow: hidden;
        border: 3px solid #1a9eff;
        background-color: #000;
    }
    /* شريط الليزر الفوسفوري المتحرك 🟢 */
    .laser-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background-color: #10b981;
        box-shadow: 0 0 12px #10b981, 0 0 20px #10b981;
        animation: scanAnim 2s linear infinite;
        z-index: 10;
        pointer-events: none;
    }
    @keyframes scanAnim { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }
    </style>
""", unsafe_allow_html=True)

# 3. إعدادات ربط السيرفر السحابي المستقل (Supabase)
SUPABASE_URL = "https://tjviltavsumuilevcokh.supabase.co"
SUPABASE_KEY = "sb_secret_hT5IIyZF-EIjGtDalfq16g_gbQGV6G5"

@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# 🔥 القفل الأمني لحفظ الذاكرة والسلة الكلية ومنع تصفيرها نهائياً
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'cart' not in st.session_state: st.session_state['cart'] = [] 

# 🚪 شاشة تسجيل الدخول
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول للنظام السحابي</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        username_input = st.text_input("👤 اسم المستخدم (اليوزر):")
        password_input = st.text_input("🔑 كلمة المرور (الباسورد):", type="password")
        submit_login = st.form_submit_button("🔓 دخول آمن للسيستم", use_container_width=True)
        if submit_login:
            hashed_input = hashlib.sha256(password_input.encode()).hexdigest().lower()
            res = supabase.table('users').select('password, full_name').eq('username', username_input).execute()
            if res.data and res.data[0]['password'].lower() == hashed_input:
                st.session_state['logged_in'] = True
                st.session_state['user_full_name'] = res.data[0]['full_name']
                st.rerun()
            else:
                st.error("❌ بيانات الدخول غير صحيحة!")
else:
    st.markdown("<h1 style='text-align: center;'>🦷 لوحة تحكم Dental Box الكاملة</h1>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 خروج آمن"):
        st.session_state['logged_in'] = False
        st.rerun()

    tab_dashboard, tab_new_invoice, tab_add_product, tab_stock, tab_customers = st.tabs([
        "📊 الأرباح", "🛒 فاتورة جديدة", "➕ صنف جديد", "📦 جرد المخزن", "👥 العملاء"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ⚡ معالجة الكود الممسوح فوراً وحفظه بالسلة قبل أي عملية تحديث لشاشة الموبايل ⚡
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    query_params = st.query_params
    if "barcode" in query_params:
        raw_code = query_params["barcode"]
        scanned_code_str = str(raw_code[0] if isinstance(raw_code, list) else raw_code).strip()
        
        if scanned_code_str:
            try:
                # جلب بضاعة السحاب للتأكد من وجود الكود
                p_check = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').eq('code', scanned_code_str).execute()
                
                if p_check.data:
                    matched_p = p_check.data[0]
                    
                    # التحقق والزيادة في السلة المحمية
                    found_in_cart = False
                    for idx, item in enumerate(st.session_state['cart']):
                        if str(item['code']).strip() == scanned_code_str:
                            st.session_state['cart'][idx]['qty'] += 1
                            found_in_cart = True
                            break
                    
                    if not found_in_cart:
                        st.session_state['cart'].append({
                            'code': matched_p['code'], 
                            'name': matched_p['name'],
                            'purchase_price': float(matched_p['purchase_price'] or 0), 
                            'selling_price': float(matched_p['selling_price'] or 0),
                            'qty': 1, 
                            'max_qty': int(matched_p['quantity'] or 0)
                        })
                    st.toast(f"📥 تم بنجاح إضافة {matched_p['name']} للفاتورة!")
                else:
                    st.error(f"⚠️ الكود ({scanned_code_str}) لُقط بنجاح، لكنه غير مسجل بالسيستم!")
            except Exception as e:
                st.error(f"خطأ سحابي: {str(e)}")
        
        # تنظيف الرابط الفوري لإعادة تهيئة الرادار للصنف القادم
        st.query_params.clear()
        st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🧱 كود بناء الرادار المحدث لإجبار الكاميرا الخلفية 📸✨
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def html_scanner_component(key_id):
        return f"""
        <div style="width: 100%; text-align: center;">
            <div class="scanner-container">
                <div class="laser-line"></div>
                <div id="reader_{key_id}" style="width: 100%;"></div>
            </div>
            <p id="status_{key_id}" style="color: #10b981; font-family: sans-serif; font-weight: bold; margin-top: 8px;">📸 الرادار يبحث بالعدسة الخلفية...</p>
        </div>
        <script src="https://unpkg.com/html5-qrcode"></script>
        <script>
            function onScanSuccess(decodedText, decodedResult) {{
                document.getElementById("status_{key_id}").innerText = "🎯 تم اللقط: " + decodedText;
                window.parent.postMessage({{type: 'streamlit:set_query_params', query_params: {{barcode: decodedText}}}}, '*');
                html5QrcodeScanner.clear();
            }}
            
            const html5QrcodeScanner = new Html5QrcodeScanner("reader_{key_id}", {{ 
                fps: 25, 
                qrbox: {{ width: 250, height: 150 }},
                videoConstraints: {{ facingMode: {{ exact: "environment" }} }},
                experimentalFeatures: {{ useBarCodeDetectorIfSupported: true }}
            }}, false);
            html5QrcodeScanner.render(onScanSuccess);
        </script>
        """

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1️⃣ Tab 1: لوحة الإحصائيات والأرباح
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_dashboard:
        try:
            res = supabase.table('invoices').select('final_total, total_profit, date').execute()
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            today_rev, all_profit = 0.0, 0.0
            for inv in res.data:
                all_profit += float(inv.get('total_profit', 0) or 0)
                if inv.get('date') == today_str: today_rev += float(inv.get('final_total', 0) or 0)
            c1, c2 = st.columns(2)
            c1.metric(label="💰 مبيعات اليوم", value=f"{today_rev:.2f} ج.م")
            c2.metric(label="💸 صافي الأرباح", value=f"{all_profit:.2f} ج.م")
        except: pass

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 2️⃣ Tab 2: الفاتورة الجديدة (السلة المحمية والحديدية 🛒🔥)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_new_invoice:
        st.markdown("### 🛒 تجهيز فاتورة مبيعات متعددة الأصناف")
        
        # تشغيل الرادار
        components.html(html_scanner_component("invoice"), height=310)

        st.markdown("---")
        inv_cust_name = st.text_input("👤 اسم الدكتور / العيادة:", value="عميل نقدي", key="main_cust_name")
        inv_cust_phone = st.text_input("📱 رقم هاتف الدكتور:", key="main_cust_phone")

        # عرض محتويات السلة الحديدية التي لا تقبل الحذف مع الـ Rerun
        st.markdown("##### 🛒 قائمة الأصناف داخل الفاتورة الحالية:")
        if st.session_state['cart']:
            total_bill_before_discount = 0.0
            total_cost_price = 0.0
            
            for idx, item in enumerate(st.session_state['cart']):
                item_total_price = item['selling_price'] * item['qty']
                total_bill_before_discount += item_total_price
                total_cost_price += item['purchase_price'] * item['qty']
                
                col_name, col_qty, col_del = st.columns([3, 2, 1])
                col_name.write(f"**{item['name']}** \n سعر: {item['selling_price']:.2f} ج.م")
                
                new_qty = col_qty.number_input("الكمية:", min_value=1, max_value=item['max_qty'], value=item['qty'], key=f"qty_{item['code']}_{idx}")
                st.session_state['cart'][idx]['qty'] = new_qty
                
                if col_del.button("🗑️", key=f"del_{item['code']}_{idx}"):
                    st.session_state['cart'].pop(idx)
                    st.rerun()
            
            st.markdown("---")
            discount_input = st.number_input("📉 الخصم الممنوح الكلي للفاتورة (ج.م):", min_value=0.0, step=5.0, value=0.0)
            final_invoice_total = total_bill_before_discount - discount_input
            final_invoice_profit = max(0.0, (total_bill_before_discount - total_cost_price) - discount_input)
            
            st.markdown(f"💼 **الإجمالي المبدئي:** {total_bill_before_discount:.2f} ج.م")
            st.markdown(f"### 🎯 الصافي النهائي المطلوب: {final_invoice_total:.2f} ج.م")
            
            generated_inv_num = f"INV-MOB-{datetime.datetime.now().strftime('%M%S')}"
            if st.button("💾 ترحيل الفاتورة بالكامل وحفظها في السحاب", use_container_width=True):
                try:
                    supabase.table('invoices').insert({
                        'invoice_num': generated_inv_num, 'customer_name': inv_cust_name, 'phone_num': inv_cust_phone,
                        'date': datetime.date.today().strftime('%Y-%m-%d'), 'total': total_bill_before_discount, 'discount': discount_input, 'final_total': final_invoice_total, 'total_profit': final_invoice_profit
                    }).execute()
                    
                    for item in st.session_state['cart']:
                        supabase.table('invoice_items').insert({
                            'invoice_num': generated_inv_num, 'product_code': item['code'], 'product_name': item['name'], 'quantity': item['qty'], 'unit_price': item['selling_price'], 'total_price': item['selling_price'] * item['qty']
                        }).execute()
                        supabase.table('products').update({'quantity': max(0, item['max_qty'] - item['qty'])}).eq('code', item['code']).execute()
                    
                    st.success(f"🎉 تم ترحيل الفاتورة رقم {generated_inv_num} بنجاح!")
                    st.session_state['cart'] = [] 
                    st.rerun()
                except Exception as e: st.error(str(e))
                
            if st.button("❌ تفريغ السلة بالكامل وإلغاء المواد"):
                st.session_state['cart'] = []
                st.rerun()
        else:
            st.info("🛒 الفاتورة فارغة حالياً؛ وجه شريط الليزر فوق على باركود المنتجات وهتلاقيها بتتسجل أوتوماتيك!")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ Tab 3: صنف جديد مع الرادار الخلفي ➕📸
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_add_product:
        st.markdown("### ➕ تسجيل صنف جديد في مخزن مستلزمات الأسنان")
        components.html(html_scanner_component("add_product"), height=310)
        
        # عرض الكود الممسوح في الخانة
        scanned_new = ""
        if 'js_scanned_code' in st.session_state and st.session_state['js_scanned_code']:
            scanned_new = st.session_state['js_scanned_code']

        with st.form("add_product_form_js"):
            new_p_code = st.text_input("📝 كود المنتج (امسحه بالرادار أعلاه أو اكتبه):", value=scanned_new)
            new_p_name = st.text_input("📦 اسم المنتج / المادة:")
            new_p_cat = st.text_input("🗂️ الفئة:")
            new_p_purchase = st.number_input("💰 سعر الشراء الأصلي (ج.م):", min_value=0.0)
            new_p_selling = st.number_input("💵 سعر البيع للعيادات (ج.م):", min_value=0.0)
            new_p_qty = st.number_input("🔢 الكمية الابتدائية المتوفرة:", min_value=0, value=10)
            
            submit_btn = st.form_submit_button("📥 إدراج الصنف في مخزن السحاب", use_container_width=True)
            if submit_btn:
                if new_p_code and new_p_name:
                    try:
                        supabase.table('products').insert({
                            'code': new_p_code, 'name': new_p_name, 'category': new_p_cat,
                            'purchase_price': new_p_purchase, 'selling_price': new_p_selling, 'quantity': new_p_qty
                        }).execute()
                        st.success(f"✅ تم إدراج الصنف الجديد ({new_p_name}) بنجاح!")
                        st.rerun()
                    except Exception as e: st.error(f"خطأ بالحفظ: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4️⃣ & 5️⃣ الجرد والعملاء
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_stock:
        prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').order('id').execute()
        if prod_res.data: st.dataframe(pd.DataFrame(prod_res.data), use_container_width=True, hide_index=True)
        
    with tab_customers:
        st.markdown("### 👥 إدارة العيادات وحجوزات الأصناف الكلية")
        with st.expander("➕ تسجيل دكتور / عيادة جديدة في السجل"):
            with st.form("add_new_customer_form"):
                c_new_name = st.text_input("👤 اسم الطبيب / العيادة:")
                c_new_phone = st.text_input("📱 رقم الجوال:")
                c_new_balance = st.text_area("📋 المنتجات المحجوزة مبدئياً:")
                if st.form_submit_button("💾 حفظ الطبيب الجديد للسحاب"):
                    if c_new_name and c_new_phone:
                        try:
                            supabase.table('customers').insert({'name': c_new_name, 'phone': c_new_phone, 'balance': c_new_balance}).execute()
                            st.success(f"✅ تم تسجيل د. {c_new_name} بنجاح!")
                            st.rerun()
                        except Exception as e: st.error(f"خطأ: {str(e)}")
        
        st.markdown("---")
        try:
            cust_res = supabase.table('customers').select('id, name, phone, balance').order('id').execute()
            if cust_res.data:
                for cust in cust_res.data:
                    c_id = cust['id']
                    c_name = cust['name']
                    c_phone = cust['phone']
                    c_res = str(cust.get('balance', '') or '').strip()
                    if not c_res: c_res = "لا توجد طلبات محجوزة حالياً"
                    
                    with st.expander(f"👤 د. {c_name} (ID: {c_id})"):
                        st.write(f"📱 **الجوال:** {c_phone}")
                        st.markdown(f"📋 **الحجوزات:** `{c_res}`")
                        st.markdown("---")
                        edit_name = st.text_input("الاسم:", value=c_name, key=f"name_{c_id}")
                        edit_phone = st.text_input("رقم الجوال:", value=c_phone, key=f"phone_{c_id}")
                        edit_balance = st.text_area("المنتجات المحجوزة للعيادة:", value=c_res if c_res != "لا توجد طلبات محجوزة حالياً" else "", key=f"bal_{c_id}")
                        
                        if st.button("💾 حفظ التعديلات والحجوزات أونلاين", key=f"save_{c_id}", use_container_width=True):
                            supabase.table('customers').update({'name': edit_name, 'phone': edit_phone, 'balance': edit_balance}).eq('id', c_id).execute()
                            st.success("✅ تم التحديث بنجاح!")
                            st.rerun()
                        
                        st.markdown("---")
                        msg = (
                            f"🦷 *نظام Dental Box لمستلزمات الأسنان* 🦷\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"أهلاً دكتور *{c_name}*، يسعدنا تواصلكم معنا عبر النظام السحابي.\n\n"
                            f"🆔 *رقم المعرف الخاص بك:* {c_id}\n"
                            f"📋 *المنتجات والمواد المحجوزة لعيادتكم حالياً:*\n• {edit_balance.replace(' ، ', '\n• ').replace(' || ', '\n• ')}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"تم قيد حجزكم وتجهيز طلباتكم مسبقاً بنجاح دكتور."
                        )
                        whatsapp_url = f"https://api.whatsapp.com/send?phone={edit_phone.replace('+', '').replace(' ', '')}&text={urllib.parse.quote(msg)}"
                        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#10b981; color:white; border:none; padding:12px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 إرسال تفاصيل الحجز عبر واتساب</button></a>', unsafe_allow_html=True)
        except Exception as e: st.error(str(e))
