# -*- coding: utf-8 -*-
# mobile_app.py (تطبيق الويب المستقل للموبايل عبر السحاب - Dental Box 🚀)

import streamlit as st
import datetime
import urllib.parse
from supabase import create_client
import pandas as pd

# 1. إعدادات الشاشة لتناسب الموبايل أوتوماتيكياً وتفتح بشكلCentered متناسق
st.set_page_config(
    page_title="Dental Box Mobile",
    page_icon="🦷",
    layout="centered"
)

# 2. التنسيق البرمجي الفخم والدعم الكامل للتصفح باللغة العربية
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 2px solid #1a9eff;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    div[data-testid="stMetricLabel"] { color: #38bdf8 !important; font-weight: bold; font-size: 16px !important; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; }
    h1, h2, h3, p, div { text-align: right; direction: rtl; font-family: 'Cairo', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 16px; }
    </style>
""", unsafe_allowed_html=True)

# 3. إعدادات ربط السيرفر السحابي المستقل (Supabase)
SUPABASE_URL = "https://tjviltavsumuilevcokh.supabase.co"
SUPABASE_KEY = "sb_secret_hT5IIyZF-EIjGtDalfq16g_gbQGV6G5"

@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# العنوان الرئيسي الفخم للوحة الموبايل
st.markdown("<h1 style='text-align: center;'>🦷 لوحة تحكم Dental Box للموبايل</h1>", unsafe_allowed_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>نظام الإدارة السحابي المستقل دكتور محمد ترك</p>", unsafe_allowed_html=True)

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
                
        # عرض البيانات في مربعات فخمة متناسقة على التليفون
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
                
                # صندوق فخم لكل عميل يناسب شاشة الموبايل
                with st.expander(f"👤 د. {c_name} (ID: {c_id})"):
                    st.write(f"📱 **رقم الجوال:** {c_phone}")
                    st.write(f"📋 **المحجوزات الحالية:** {c_res}")
                    
                    # قفل رسالة الواتساب المطور والشامل للـ ID والطلبات الحالية 👑
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
                    
                    # زرار أخضر ملوكي كبير وسهل اللمس للإرسال
                    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#10b981; color:white; border:none; padding:10px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 إرسال تفاصيل الحجز عبر واتساب</button></a>', unsafe_allowed_html=True)
        else:
            st.info("سجل العملاء لا يحتوي على أطباء مسجلين.")
    except Exception as e:
        st.error(f"خطأ في سجل العملاء: {str(e)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Tab 4: إضافة المشتريات وتزويد البضاعة من الموبايل
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
                st.warning(f"📉 المخزون الحالي الفعلي بالسحاب: {current_qty} وحدة")
                
                new_qty_bought = st.number_input("➕ عدد الوحدات المشتراة الجديدة:", min_value=1, step=1, value=1)
                
                if st.button("📥 تحديث المخزن وتأكيد الشراء الفوري", use_container_width=True):
                    updated_total = current_qty + new_qty_bought
                    
                    # تحديث سحابي فوري يسمع في جهاز العيادة
                    supabase.table('products').update({'quantity': updated_total}).eq('code', code).execute()
                    st.success(f"✅ تم الحفظ! الكمية الجديدة لـ ({selected_prod_name})صبحت: {updated_total} وحدة")
                    st.rerun()
        else:
            st.warning("لا توجد منتجات لتزويدها، أضف أصناف أولاً من الكمبيوتر.")
    except Exception as e:
        st.error(f"فشلت عملية المشتريات: {str(e)}")