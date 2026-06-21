# -*- coding: utf-8 -*-
# mobile_app.py (نسخة السكنر السحابي الفوري - تفعيل كاميرا الموبايل لقراءة الباركود 🚀)

import streamlit as st
import datetime
import urllib.parse
import hashlib
from supabase import create_client
import pandas as pd
# استيراد أداة الكاميرا المباشرة للموبايل
from streamlit_camera_input_live import camera_input_live
import cv2
import numpy as np

# 1. إعدادات الشاشة لتناسب الموبايل أوتوماتيكياً
st.set_page_config(
    page_title="Dental Box Mobile Scanner",
    page_icon="🦷",
    layout="centered"
)

# 2. التنسيق البرمجي الفخم والإضاءة الكاملة للكروت والخطوط البيضاء الواضحة 🌟
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    
    /* ستايل كروت الإحصائيات المضيئة */
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
if 'scanned_code' not in st.session_state:
    st.session_state['scanned_code'] = ""

# 🚪 شاشة تسجيل الدخول
if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول للنظام السحابي</h2>", unsafe_allow_html=True)
    
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
    st.markdown("<h1 style='text-align: center;'>🦷 لوحة تحكم Dental Box الكاملة</h1>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 خروج آمن"):
        st.session_state['logged_in'] = False
        st.rerun()

    tab_dashboard, tab_new_invoice, tab_add_product, tab_stock, tab_customers = st.tabs([
        "📊 الأرباح", 
        "🛒 فاتورة جديدة", 
        "➕ صنف جديد",
        "📦 جرد المخزن", 
        "👥 العملاء"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1️⃣ Tab 1: الأرباح
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_dashboard:
        st.markdown("### 📊 الأداء المالي العام")
        try:
            res = supabase.table('invoices').select('final_total, total_profit, date').execute()
            invoices = res.data if res.data else []
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            today_revenue = 0.0
            all_time_profit = 0.0
            for inv in invoices:
                all_time_profit += float(inv.get('total_profit', 0) or 0)
                if inv.get('date') == today_str:
                    today_revenue += float(inv.get('final_total', 0) or 0)
            
            col1, col2 = st.columns(2)
            with col1: st.metric(label="💰 مبيعات اليوم الحالي", value=f"{today_revenue:.2f} ج.م")
            with col2: st.metric(label="💸 إجمالي صافي الأرباح", value=f"{all_time_profit:.2f} ج.m")
        except Exception as e: st.error(f"خطأ: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 2️⃣ Tab 2: إنشاء فاتورة جديدة مع السكنر 🛒📸
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_new_invoice:
        st.markdown("### 🛒 إصدار فاتورة مبيعات سحابية جديدة")
        
        # تفعيل كاميرا السكنر الفوري للموبايل
        st.markdown("##### 📸 اضغط على زر الكاميرا أدناه لعمل سكان للباركود فوراً:")
        image = camera_input_live()
        
        if image:
            try:
                # قراءة الصورة الملتقطة من الكاميرا للبحث عن باركود
                bytes_data = image.read()
                cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                detector = cv2.BarcodeDetector()
                retval, decoded_info, decoded_type = detector.detectAndDecode(cv2_img)
                
                if retval and decoded_info[0]:
                    st.session_state['scanned_code'] = decoded_info[0]
                    st.success(f"🎯 تم لقط الباركود بنجاح: {st.session_state['scanned_code']}")
            except Exception as e:
                pass

        generated_inv_num = f"INV-MOB-{datetime.datetime.now().strftime('%M%S')}"
        inv_cust_name = st.text_input("👤 السيد الدكتور / العيادة:", value="عميل نقدي")
        inv_cust_phone = st.text_input("📱 رقم هاتف الدكتور:")

        # لو السكنر لقط كود، هيعلم عليه أوتوماتيك في الاختيار
        try:
            prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').execute()
            all_prods = prod_res.data if prod_res.data else []
            
            if all_prods:
                prod_options = {p['name']: p for p in all_prods}
                
                # تحديث تلقائي لو الكود ممسوح بالسكنر
                default_index = 0
                if st.session_state['scanned_code']:
                    for idx, name in enumerate(list(prod_options.keys())):
                        if prod_options[name]['code'] == st.session_state['scanned_code']:
                            default_index = idx
                            break
                
                selected_item_name = st.selectbox("📦 المستلزم الطبي المراد بيعه:", list(prod_options.keys()), index=default_index)
                
                item_details = prod_options[selected_item_name]
                max_available = int(item_details['quantity'] or 0)
                st.info(f"📊 كود الصنف الحالي: {item_details['code']} | المتاح: {max_available} وحدة")
                
                if max_available <= 0:
                    st.error("⚠️ الصنف نفد من المخزن!")
                else:
                    qty_to_sell = st.number_input("🔢 الكمية المطلوبة:", min_value=1, max_value=max_available, step=1, value=1)
                    discount_input = st.number_input("📉 الخصم (ج.م):", min_value=0.0, value=0.0)
                    
                    sub_total = float(item_details['selling_price'] or 0) * qty_to_sell
                    final_total_bill = sub_total - discount_input
                    invoice_profit = ((float(item_details['selling_price'] or 0) - float(item_details['purchase_price'] or 0)) * qty_to_sell) - discount_input
                    
                    st.markdown(f"### 🎯 الصافي المطلوب: {final_total_bill:.2f} ج.م")
                    
                    if st.button("💾 ترحيل الفاتورة وحفظها في السحاب", use_container_width=True):
                        supabase.table('invoices').insert({
                            'invoice_num': generated_inv_num, 'customer_name': inv_cust_name,
                            'phone_num': inv_cust_phone, 'date': datetime.date.today().strftime('%Y-%m-%d'),
                            'total': sub_total, 'discount': discount_input, 'final_total': final_total_bill, 'total_profit': invoice_profit
                        }).execute()
                        
                        supabase.table('invoice_items').insert({
                            'invoice_num': generated_inv_num, 'product_code': item_details['code'],
                            'product_name': selected_item_name, 'quantity': qty_to_sell, 'unit_price': item_details['selling_price'], 'total_price': sub_total
                        }).execute()
                        
                        supabase.table('products').update({'quantity': (max_available - qty_to_sell)}).eq('code', item_details['code']).execute()
                        st.success("🎉 تم حفظ الفاتورة بنجاح!")
                        st.session_state['scanned_code'] = "" # تصفير السكنر للفاتورة الجاية
                        st.rerun()
            else:
                st.warning("المخزن فارغ!")
        except Exception as e: st.error(f"خطأ: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ Tab 3: صنف جديد مع ميزة السكنر لقراءة الكود الجديد ➕📸
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_add_product:
        st.markdown("### ➕ تسجيل صنف جديد بكاميرا الباركود")
        
        st.markdown("##### 📸 وجه الكاميرا لباركود المنتج الجديد لملء الخانة تلقائياً:")
        image_new = camera_input_live(key="new_prod_cam")
        scanned_new_code = ""
        
        if image_new:
            try:
                bytes_data_n = image_new.read()
                cv2_img_n = cv2.imdecode(np.frombuffer(bytes_data_n, np.uint8), cv2.IMREAD_COLOR)
                detector_n = cv2.BarcodeDetector()
                retval_n, decoded_info_n, _ = detector_n.detectAndDecode(cv2_img_n)
                if retval_n and decoded_info_n[0]:
                    scanned_new_code = decoded_info_n[0]
                    st.success(f"🎯 تم التقاط باركود المنتج الجديد: {scanned_new_code}")
            except:
                pass

        with st.form("add_new_product_form"):
            # لو الكاميرا لقطت باركود هتحطه هنا علطول تلقائي
            new_p_code = st.text_input("📝 كود المنتج / الباركود:", value=scanned_new_code if scanned_new_code else "")
            new_p_name = st.text_input("📦 اسم المنتج / المادة:")
            new_p_cat = st.text_input("🗂️ الفئة:")
            new_p_purchase = st.number_input("💰 سعر الشراء الاصلي:", min_value=0.0)
            new_p_selling = st.number_input("💵 سعر البيع للعيادات:", min_value=0.0)
            new_p_qty = st.number_input("🔢 الكمية الابتدائية:", min_value=0, value=10)
            
            submit_new_prod = st.form_submit_button("📥 إدراج الصنف في مخزن السحاب", use_container_width=True)
            
            if submit_new_prod:
                if new_p_code and new_p_name:
                    try:
                        check_exist = supabase.table('products').select('id').eq('code', new_p_code).execute()
                        if check_exist.data:
                            st.error("⚠️ هذا الكود مسجل مسبقاً لصنف آخر!")
                        else:
                            supabase.table('products').insert({
                                'code': new_p_code, 'name': new_p_name, 'category': new_p_cat,
                                'purchase_price': new_p_purchase, 'selling_price': new_p_selling, 'quantity': new_p_qty
                            }).execute()
                            st.success(f"✅ تم حفظ المنتج الجديد ({new_p_name}) بنجاح!")
                    except Exception as e: st.error(f"فشل الحفظ: {str(e)}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4️⃣ Tab 4 و 5️⃣ Tab 5: جرد المخزن والعملاء (كما هي بكفاءة)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_stock:
        st.markdown("### 📦 جرد الكميات الحالية بالسحاب")
        try:
            prod_res = supabase.table('products').select('code, name, purchase_price, selling_price, quantity').order('id').execute()
            if prod_res.data:
                st.dataframe(pd.DataFrame(prod_res.data), use_container_width=True, hide_index=True)
        except Exception as e: st.error(str(e))
        
    with tab_customers:
        st.markdown("### 👥 سجل العيادات والرسائل الفورية")
        try:
            cust_res = supabase.table('customers').select('id, name, phone, balance').order('id').execute()
            if cust_res.data:
                for cust in cust_res.data:
                    with st.expander(f"👤 د. {cust['name']} (ID: {cust['id']})"):
                        st.write(f"📱 جوال: {cust['phone']} | محجوزات: {cust.get('balance', 'لا يوجد')}")
        except Exception as e: st.error(str(e))
