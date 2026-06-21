# -*- coding: utf-8 -*-
# mobile_app.py (النسخة الإمبراطورية الشاملة - إدارة العملاء والحجوزات والواتساب الفوري من الموبايل 🚀👥)

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
    div[data-testid="stMetricLabel"] { color: #e0f2fe !important; font-weight: bold !important; font-size: 15px !important; }
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

# تهيئة المتغيرات المؤقتة
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'js_scanned_code' not in st.session_state: st.session_state['js_scanned_code'] = ""
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
        "📊 الأرباح", "🛒 فاتورة جديدة", "➕ صنف جديد", "📦 جرد المخزن", "👥 سجل العملاء"
    ])

    # جلب باركود الرادار
    if "barcode" in st.query_params:
        st.session_state['js_scanned_code'] = st.query_params["barcode"]

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
    # 2️⃣ Tab 2: الفاتورة الجديدة مع شريط الليزر 🛒
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_new_invoice:
        st.markdown("### 🛒 تجهيز فاتورة مواد متعددة الأصناف")
        scanner_html = """
        <div style="width: 100%; text-align: center;">
            <div style="position: relative; width: 100%; max-width: 400px; margin: auto; border-radius: 12px; overflow: hidden; border: 3px solid #1a9eff;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background-color: #10b981; box-shadow: 0 0 12px #10b981; animation: scanAnim 2s linear infinite; z-index: 10; pointer-events: none;"></div>
                <div id="reader" style="width: 100%;"></div>
            </div>
            <p id="status" style="color: #10b981; font-family: sans-serif; font-weight: bold; margin-top: 8px;">📸 الرادار يبحث عن باركود حالياً...</p>
        </div>
        <script src="https://unpkg.com/html5-qrcode"></script>
        <script>
            @keyframes scanAnim { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }
            const html5QrcodeScanner = new Html5Qrcode("reader");
            const config = { fps: 25, qrbox: { width: 260, height: 160 } };
            Html5Qrcode.getCameras().then(devices => {
                if (devices && devices.length) {
                    let backId = devices[0].id;
                    for (let d of devices) { if (d.label.toLowerCase().includes('back') || d.label.toLowerCase().includes('rear')) { backId = d.id; break; } }
                    html5QrcodeScanner.start(backId, config, (txt) => {
                        window.parent.postMessage({type: 'streamlit:set_query_params', query_params: {barcode: txt}}, '*');
                        html5QrcodeScanner.stop();
                    }, (err) => {});
                }
            }).catch(err => {});
        </script>
        """
        components.html(scanner_html, height=295)

        try:
            prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').execute()
            all_products_dict = {p['code']: p for p in prod_res.data} if prod_res.data else {}
            all_products_by_name = {p['name']: p for p in prod_res.data} if prod_res.data else {}
            
            if st.session_state['js_scanned_code']:
                scanned_code_str = str(st.session_state['js_scanned_code']).strip()
                if scanned_code_str in all_products_dict:
                    matched_prod = all_products_dict[scanned_code_str]
                    found_in_cart = False
                    for idx, item in enumerate(st.session_state['cart']):
                        if item['code'] == scanned_code_str:
                            st.session_state['cart'][idx]['qty'] += 1
                            found_in_cart = True
                            break
                    if not found_in_cart:
                        st.session_state['cart'].append({
                            'code': matched_prod['code'], 'name': matched_prod['name'],
                            'purchase_price': float(matched_prod['purchase_price'] or 0), 'selling_price': float(matched_prod['selling_price'] or 0),
                            'qty': 1, 'max_qty': int(matched_prod['quantity'] or 0)
                        })
                    st.toast(f"📥 تم إضافة: {matched_prod['name']}")
                st.session_state['js_scanned_code'] = ""
                st.query_params.clear()
                st.rerun()
        except: pass

        st.markdown("---")
        inv_cust_name = st.text_input("👤 اسم الدكتور / العيادة:", value="عميل نقدي", key="main_cust_name")
        inv_cust_phone = st.text_input("📱 رقم هاتف الدكتور:", key="main_cust_phone")

        st.markdown("##### 🛒 قائمة الأصناف داخل الفاتورة:")
        if st.session_state['cart']:
            total_bill_before_discount = 0.0
            total_cost_price = 0.0
            for idx, item in enumerate(st.session_state['cart']):
                item_total_price = item['selling_price'] * item['qty']
                total_bill_before_discount += item_total_price
                total_cost_price += item['purchase_price'] * item['qty']
                col_name, col_qty, col_del = st.columns([3, 2, 1])
                col_name.write(f"**{item['name']}** \n سعر: {item['selling_price']} | إجمالي: {item_total_price}")
                new_qty = col_qty.number_input("الكمية:", min_value=1, max_value=item['max_qty'], value=item['qty'], key=f"qty_{item['code']}_{idx}")
                st.session_state['cart'][idx]['qty'] = new_qty
                if col_del.button("🗑️", key=f"del_{item['code']}_{idx}"):
                    st.session_state['cart'].pop(idx)
                    st.rerun()
            
            discount_input = st.number_input("📉 الخصم الكلي (ج.م):", min_value=0.0, step=5.0, value=0.0)
            final_invoice_total = total_bill_before_discount - discount_input
            final_invoice_profit = max(0.0, (total_bill_before_discount - total_cost_price) - discount_input)
            
            st.markdown(f"### 🎯 الصافي النهائي المطلوب: {final_invoice_total:.2f} ج.م")
            
            generated_inv_num = f"INV-MOB-{datetime.datetime.now().strftime('%M%S')}"
            if st.button("💾 ترحيل الفاتورة بالكامل وحفظها في السحاب", use_container_width=True):
                supabase.table('invoices').insert({
                    'invoice_num': generated_inv_num, 'customer_name': inv_cust_name, 'phone_num': inv_cust_phone,
                    'date': datetime.date.today().strftime('%Y-%m-%d'), 'total': total_bill_before_discount, 'discount': discount_input, 'final_total': final_invoice_total, 'total_profit': final_invoice_profit
                }).execute()
                for item in st.session_state['cart']:
                    supabase.table('invoice_items').insert({
                        'invoice_num': generated_inv_num, 'product_code': item['code'], 'product_name': item['name'], 'quantity': item['qty'], 'unit_price': item['selling_price'], 'total_price': item['selling_price'] * item['qty']
                    }).execute()
                    supabase.table('products').update({'quantity': max(0, item['max_qty'] - item['qty'])}).eq('code', item['code']).execute()
                st.success("🎉 تم ترحيل الفاتورة بنجاح!")
                st.session_state['cart'] = []
                st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ Tab 3: صنف جديد ➕
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_add_product:
        st.markdown("### ➕ تسجيل صنف جديد في مخزن مستلزمات الأسنان")
        with st.form("add_product_form_js"):
            new_p_code = st.text_input("📝 كود المنتج:")
            new_p_name = st.text_input("📦 اسم المنتج / المادة:")
            new_p_cat = st.text_input("🗂️ الفئة:")
            new_p_purchase = st.number_input("💰 سعر الشراء الأصلي:", min_value=0.0)
            new_p_selling = st.number_input("💵 سعر البيع للعيادات:", min_value=0.0)
            new_p_qty = st.number_input("🔢 الكمية الابتدائية:", min_value=0, value=10)
            if st.form_submit_button("📥 إدراج الصنف في مخزن السحاب", use_container_width=True):
                if new_p_code and new_p_name:
                    supabase.table('products').insert({'code': new_p_code, 'name': new_p_name, 'category': new_p_cat, 'purchase_price': new_p_purchase, 'selling_price': new_p_selling, 'quantity': new_p_qty}).execute()
                    st.success("✅ تم إدراج الصنف الجديد!")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4️⃣ Tab 4: جرد المخزن
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_stock:
        st.markdown("### 📦 كميات المواد الحالية بالسحاب")
        prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').order('id').execute()
        if prod_res.data: st.dataframe(pd.DataFrame(prod_res.data), use_container_width=True, hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 5️⃣ Tab 5: سجل العملاء المطور (التعديل، الحجز الجديد، والواتساب الفوري) 👥🔥
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_customers:
        st.markdown("### 👥 إدارة العيادات وحجوزات الأصناف")
        
        # 🆕 أولاً: ميزة إضافة دكتور/عيادة جديدة بالكامل من الموبايل
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
                    else: st.warning("⚠️ يرجى كتابة الاسم ورقم الجوال!")

        st.markdown("---")
        st.markdown("##### 👥 قائمة الأطباء المتعاقدين (اضغط للتعديل أو الإرسال):")
        
        # جلب بيانات العملاء أونلاين
        try:
            cust_res = supabase.table('customers').select('id, name, phone, balance').order('id').execute()
            customers_data = cust_res.data if cust_res.data else []
            
            if customers_data:
                for cust in customers_data:
                    c_id = cust['id']
                    c_name = cust['name']
                    c_phone = cust['phone']
                    # قراءة النص من السحاب بأمان
                    c_res = str(cust.get('balance', '') or '').strip()
                    if not c_res: c_res = "لا توجد طلبات محجوزة حالياً"
                    
                    # صندوق منسدل فخم لكل عميل
                    with st.expander(f"👤 د. {c_name} (ID: {c_id})"):
                        st.write(f"📱 **رقم الجوال الحركي:** {c_phone}")
                        st.markdown(f"📋 **الحجوزات المسجلة حالياً:** \n `{c_res}`")
                        
                        # 🛠️ فورم داخلي لتعديل المنتجات أو إضافة حجز جديد فوراً من التليفون
                        st.markdown("---")
                        st.markdown("✏️ **تعديل البيانات أو إضافة منتجات للحجز:**")
                        edit_name = st.text_input("الاسم:", value=c_name, key=f"name_{c_id}")
                        edit_phone = st.text_input("رقم الجوال:", value=c_phone, key=f"phone_{c_id}")
                        edit_balance = st.text_area("المنتجات المحجوزة (اكتب هنا الصنف الجديد):", value=c_res if c_res != "لا توجد طلبات محجوزة حالياً" else "", key=f"bal_{c_id}")
                        
                        if st.button("💾 حفظ التعديلات والحجوزات أونلاين", key=f"save_{c_id}", use_container_width=True):
                            try:
                                supabase.table('customers').update({
                                    'name': edit_name,
                                    'phone': edit_phone,
                                    'balance': edit_balance
                                }).eq('id', c_id).execute()
                                st.success("✅ تم تحديث الحجز والبيانات في السحاب فوراً!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"فشل التعديل السحابي: {str(e)}")
                        
                        # 💬 زرار إرسال تفاصيل الحجز الفوري للدكتور عبر واتساب
                        st.markdown("---")
                        msg = (
                            f"🦷 *نظام Dental Box لمستلزمات الأسنان* 🦷\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"أهلاً دكتور *{c_name}*، يسعدنا تواصلكم معنا عبر النظام السحابي.\n\n"
                            f"🆔 *رقم المعرف الخاص بك:* {c_id}\n"
                            f"📋 *المنتجات والمواد المحجوزة لعيادتكم حالياً:*\n• {edit_balance.replace(' ، ', '\n• ').replace(' || ', '\n• ')}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"تم قيد حجزكم وتجهيز طلباتكم بنجاح دكتور، يرجى إفادتنا بأي مستلزمات طبية إضافية تحتاجونها لعيادتكم الموقرة."
                        )
                        encoded_msg = urllib.parse.quote(msg)
                        whatsapp_url = f"https://api.whatsapp.com/send?phone={edit_phone.replace('+', '').replace(' ', '')}&text={encoded_msg}"
                        
                        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#10b981; color:white; border:none; padding:12px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 إرسال تفاصيل الحجز عبر واتساب</button></a>', unsafe_allow_html=True)
            else:
                st.info("لا يوجد أطباء مسجلين حالياً.")
        except Exception as e:
            st.error(f"خطأ في قراءة العملاء: {str(e)}")
