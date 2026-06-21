# -*- coding: utf-8 -*-
# config.py

import os
from supabase import create_client, Client

class Config:
    APP_NAME = "Dental Box"  
    APP_VERSION = "VIP MANAGER (Cloud)"
    
    # 🔗 بيانات الاتصال بـ Supabase 
    SUPABASE_URL = "https://tjviltavsumuilevcokh.supabase.co"
    SUPABASE_KEY = "sb_secret_hT5IIyZF-EIjGtDalfq16g_gbQGV6G5"
    
    # 🎨 الألوان
    COLORS = {
        "primary": "#e2e8f0",
        "secondary": "#cbd5e1",
        "cyan": "#1d4ed8",
        "purple": "#7c3aed",
        "dark_card": "#f1f5f9",
        "danger": "#ef4444",
        "warning": "#ff7c00",
        "light": "#0f172a",
        "gray": "#475569",
        "border": "#94a3b8",
    }
    
    DEFAULT_CURRENCY = "ج.م"
    
    @classmethod
    def get_db(cls) -> Client:
        """هذه هي الدالة التي يتصل من خلالها البرنامج بالسحابة"""
        return create_client(cls.SUPABASE_URL, cls.SUPABASE_KEY)

    @classmethod
    def initialize_db(cls):
        """لم نعد بحاجة لإنشاء الجداول محلياً لأننا أنشأناها في Supabase"""
        print("[INFO] النظام يعمل الآن بنظام السحابة (Supabase).")

    @classmethod
    def get_db_connection(cls):
        """
        تنبيه لمنع الأخطاء: هذه الدالة كانت للاتصال المحلي القديم.
        إذا تم استدعاؤها بالخطأ ستنبهنا لنقوم بتحديث الكود المتبقي.
        """
        raise Exception("تم إيقاف قاعدة البيانات المحلية. يرجى استخدام get_db() للاتصال بالسحابة.")