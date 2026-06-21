# -*- coding: utf-8 -*-
# mobile_app.py (النسخة الإمبراطورية النهائية - إسكانر الكاميرا اللايف الفوري بدون أزرار 🚀📸)

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

# 2. التنسيق البرمجي الملوكي وألوان الكروت المضيئة 🌟
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
    div[data-testid="stMetricLabel"] { color: #e0f2fe !important; font-weight: bold !important; font-size: 16px !important; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 26px !important; font-weight: 900 !important; }
    h1, h2, h3, p, div, label { text-align: right; direction: rtl; font-family: 'Cairo', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 15px; }
    .stButton>button { background-color: #1a9eff !important; color: white !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. إعدادات ربط السيرفر السحابي المستقل (Supabase)
SUPABASE_URL = "https://tjviltavsumuilevcokh.supabase.co"
SUPABASE_KEY = "sb_secret_hT5IIyZF-EIjGtDalfq16g_gbQGV6G5"

@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'js_scanned_code' not in st.session_state: st.session_state['js_scanned_code'] = ""

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
    
    # التقاط الكود المرسل من كاميرا الجافا سكريبت اللايف
    query_params = st.query_params
    if "barcode" in query_params:
        st.session_state['js_scanned_code'] = query_params["barcode"]

    tab_dashboard, tab_new_invoice, tab_add_product, tab_stock, tab_customers = st.tabs([
        "📊 الأرباح", "🛒 فاتورة جديدة", "➕ صنف جديد", "📦 جرد المخزن", "👥 العملاء"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # دالة السحر: بناء الإسكانر التلقائي الذكي بدون أزرار 📸✨
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def render_live_scanner_component():
        st.markdown("##### 📸 رادار مسح الباركود التلقائي (Live Video):")
        
        # كود جافا سكريبت مدمج بيفتح الكاميرا الخلفية وبيعمل Scan فوري لحظي
        scanner_html = """
        <div style="width: 100%; text-align: center;">
            <div id="reader" style="width: 100%; max-width: 400px; margin: auto; border-radius: 12px; overflow: hidden;"></div>
            <p id="status" style="color: #64748b; font-family: sans-serif; margin-top: 8px;">جاري تشغيل عدسة الرادار...</p>
        </div>
        <script src="https://unpkg.com/html5-qrcode"></script>
        <script>
            const html5QrcodeScanner = new Html5Qrcode("reader");
            const config = { fps: 20, qrbox: { width: 250, height: 150 } };
            
            // فتح الكاميرا الخلفية للموبايل علطول
            Html5Qrcode.getCameras().then(devices => {
                if (devices && devices.length) {
                    let backCameraId = devices[0].id;
                    for (let device of devices) {
                        if (device.label.toLowerCase().includes('back') || device.label.toLowerCase().includes('rear')) {
                            backCameraId = device.id;
                            break;
                        }
                    }
                    
                    html5QrcodeScanner.start(
                        backCameraId, 
                        config,
                        (decodedText) => {
                            document.getElementById("status").innerText = "🎯 تم اللقط: " + decodedText;
                            html5QrcodeScanner.stop().then(() => {
                                // إرسال الكود فوراً لصفحة المراقبة
                                window.parent.postMessage({type: 'streamlit:set_query_params', query_params: {barcode: decodedText}}, '*');
                            });
                        },
                        (errorMessage) => { /* مراقبة صامتة */ }
                    );
                }
            }).catch(err => {
                document.getElementById("status").innerText = "⚠️ برجاء إعطاء إذن الكاميرا للمتصفح!";
            });
        </script>
        """
        components.html(scanner_html, height=320)
        if st.session_state['js_scanned_code']:
            st.success(f"🎯 الرادار لقط كود: {st.session_state['js_scanned_code']}")
            if st.button("🔄 إعادة مسح صنف آخر"):
                st.session_state['js_scanned_code'] = ""
                st.query_params.clear()
                st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1️⃣ Tab 1: لوحة التحكم والماليات
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
    # 2️⃣ Tab 2: الفاتورة الجديدة مع الرادار الفوري 🛒
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_new_invoice:
        render_live_scanner_component()
        
        generated_inv_num = f"INV-MOB-{datetime.datetime.now().strftime('%M%S')}"
        inv_cust_name = st.text_input("👤 اسم الدكتور / العيادة:", value="عميل نقدي")
        inv_cust_phone = st.text_input("📱 رقم هاتف الدكتور:")

        try:
            prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').execute()
            if prod_res.data:
                prod_options = {p['name']: p for p in prod_res.data}
                
                # توجيه المؤشر أوتوماتيكياً للصنف الممسوح بالرادار
                default_index = 0
                if st.session_state['js_scanned_code']:
                    for idx, name in enumerate(list(prod_options.keys())):
                        if str(prod_options[name]['code']).strip() == str(st.session_state['js_scanned_code']).strip():
                            default_index = idx
                            break
                
                selected_item_name = st.selectbox("📦 اختر المستلزم المراد بيعه:", list(prod_options.keys()), index=default_index, key="inv_select")
                item_details = prod_options[selected_item_name]
                max_available = int(item_details['quantity'] or 0)
                st.caption(f"📊 كود الصنف: {item_details['code']} | المتاح: {max_available} وحدة")
                
                if max_available <= 0:
                    st.error("⚠️ المنتج نفد من المخزن!")
                else:
                    qty_to_sell = st.number_input("🔢 الكمية المطلوبة:", min_value=1, max_value=max_available, step=1, value=1)
                    discount_input = st.number_input("📉 الخصم (ج.م):", min_value=0.0, value=0.0)
                    
                    sub_total = float(item_details['selling_price'] or 0) * qty_to_sell
                    final_total_bill = sub_total - discount_input
                    invoice_profit = ((float(item_details['selling_price'] or 0) - float(item_details['purchase_price'] or 0)) * qty_to_sell) - discount_input
                    
                    st.markdown(f"### 🎯 الصافي المطلوب: {final_total_bill:.2f} ج.م")
                    
                    if st.button("💾 حفظ وترحيل الفاتورة أونلاين", use_container_width=True):
                        supabase.table('invoices').insert({
                            'invoice_num': generated_inv_num, 'customer_name': inv_cust_name, 'phone_num': inv_cust_phone,
                            'date': datetime.date.today().strftime('%Y-%m-%d'), 'total': sub_total, 'discount': discount_input, 'final_total': final_total_bill, 'total_profit': max(0.0, invoice_profit)
                        }).execute()
                        supabase.table('invoice_items').insert({
                            'invoice_num': generated_inv_num, 'product_code': item_details['code'], 'product_name': selected_item_name, 'quantity': qty_to_sell, 'unit_price': item_details['selling_price'], 'total_price': sub_total
                        }).execute()
                        supabase.table('products').update({'quantity': (max_available - qty_to_sell)}).eq('code', item_details['code']).execute()
                        st.success("🎉 تم حفظ الفاتورة بنجاح!")
                        st.session_state['js_scanned_code'] = ""
                        st.query_params.clear()
                        st.rerun()
        except Exception as e: st.error(str(e))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ Tab 3: صنف جديد بالرادار الفوري ➕
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_add_product:
        st.markdown("### ➕ تسجيل صنف جديد بكاميرا الرادار")
        with st.form("add_product_form_js"):
            new_p_code = st.text_input("📝 كود المنتج (امسحه بالرادار فوق أولاً):", value=st.session_state['js_scanned_code'])
            new_p_name = st.text_input("📦 اسم المنتج / المادة:")
            new_p_cat = st.text_input("🗂️ الفئة:")
            new_p_purchase = st.number_input("💰 سعر الشراء الاصلي:", min_value=0.0)
            new_p_selling = st.number_input("💵 سعر البيع للعيادات:", min_value=0.0)
            new_p_qty = st.number_input("🔢 الكمية الابتدائية:", min_value=0, value=10)
            submit_btn = st.form_submit_button("📥 إدراج الصنف في مخزن السحاب", use_container_width=True)
            if submit_btn:
                if new_p_code and new_p_name:
                    supabase.table('products').insert({
                        'code': new_p_code, 'name': new_p_name, 'category': new_p_cat,
                        'purchase_price': new_p_purchase, 'selling_price': new_p_selling, 'quantity': new_p_qty
                    }).execute()
                    st.success("✅ تم إدراج الصنف الجديد!")
                    st.session_state['js_scanned_code'] = ""
                    st.query_params.clear()
                    st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4️⃣ & 5️⃣ الجرد والعملاء
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_stock:
        prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').order('id').execute()
        if prod_res.data: st.dataframe(pd.DataFrame(prod_res.data), use_container_width=True, hide_index=True)
    with tab_customers:
        cust_res = supabase.table('customers').select('id, name, phone, balance').order('id').execute()
        if cust_res.data:
            for c in cust_res.data:
                with st.expander(f"👤 د. {c['name']} (ID: {c['id']})"):
                    st.write(f"📱 جوال: {c['phone']} | طلبات: {c.get('balance', 'لا يوجد')}")
