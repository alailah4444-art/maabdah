import streamlit as st
import datetime
import os

# 1. إعدادات الصفحة والأيقونة (إخفاء الشريط الجانبي نهائياً لحل مشكلة الجوال)
page_icon_path = "logo.jpg" if os.path.exists("logo.jpg") else ("logo.png" if os.path.exists("logo.png") else "🕋")

st.set_page_config(
    page_title="مهام الإدارة التنفيذية - جمعية الدعوة بالمعابدة",
    page_icon=page_icon_path,
    layout="centered",  # تصميم مركزي متوافق 100% مع شاشات الجوال والكمبيوتر
    initial_sidebar_state="collapsed"
)

# 2. تنسيقات CSS احترافية تمنع الشريط الجانبي وتضبط الخطوط العربية والجوال
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* إخفاء الشريط الجانبي وأزراره نهائياً لمنع تقطيع الحروف على الجوال */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    html, body, [class*="css"], .stMarkdown, div, p, span, h1, h2, h3, h4, label {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
        writing-mode: horizontal-tb !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
    }
    
    .main {
        background-color: #F8F9FA;
    }
    
    /* تنسيق الأزرار الرسمية */
    .stButton>button {
        background-color: #196470 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 10px !important;
        border: none !important;
        font-size: 16px !important;
    }
    .stButton>button:hover {
        background-color: #124952 !important;
    }
    
    /* بطاقات الإحصائيات والترحيب المتوافقة مع الجوال */
    .header-box {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        border-right: 6px solid #196470;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin-bottom: 15px;
        width: 100%;
    }
    
    .stats-container {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        width: 100%;
    }
    .stat-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        text-align: center !important;
        flex: 1;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    .stat-num {
        font-size: 26px;
        font-weight: bold;
        color: #196470;
        text-align: center !important;
    }
    .stat-label {
        font-size: 14px;
        color: #666;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تهيئة قاعدة البيانات المؤقتة في الجلسة
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"id": "1", "title": "متابعة برامج توعية الجاليات الأسبوعية", "desc": "تجهيز القاعات والمحاضرين للبرامج الدعوية", "assignee": "عبدالله السلمي (قسم الجاليات)", "date": "2026-06-15", "status": "قيد التنفيذ", "priority": "عالية"},
        {"id": "2", "title": "تقرير إنجاز الحملات الرمضانية", "desc": "حصر أعداد المستفيدين من البرامج", "assignee": "سعد القرشي (البرامج الدعوية)", "date": "2026-05-10", "status": "منفذة", "priority": "متوسطة"}
    ]

if 'team' not in st.session_state:
    st.session_state.team = [
        'عبدالله السلمي (قسم الجاليات)',
        'سعد القرشي (البرامج الدعوية)',
        'ساره أحمد (الإدارة المالية)',
        'محمد خالد (العلاقات العامة)'
    ]

# 4. تفعيل عمل سهم الرجوع في المتصفح عبر رابط الصفحة (Query Params)
query_params = st.query_params
current_page = query_params.get("page", "login")
current_user = query_params.get("user", None)

# ==================== الواجهة الأولى: شاشة تسجيل الدخول ====================
if current_page == "login" or not current_user:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # عرض الشعار في المنتصف بشكل متناسق
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("logo.jpg"):
            st.image("logo.jpg", use_container_width=True)
        elif os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)

    st.markdown("""
        <div style="text-align: center !important; margin-top: 10px;">
            <h1 style="color: #196470; text-align: center !important; font-size: 28px; margin-bottom: 5px;">الإدارة التنفيذية</h1>
            <p style="color: #555; text-align: center !important; font-size: 16px; font-weight: bold;">جمعية الدعوة والإرشاد وتوعية الجاليات بالمعابدة</p>
        </div>
        <hr style="margin: 20px 0;">
    """, unsafe_allow_html=True)

    login_options = ["اختر حساب المستخدم..."] + ["مشرف تنفيذي (Admin - صلاحيات كاملة)"] + st.session_state.team
    selected_user = st.selectbox("اختر صفة الدخول للنظام:", login_options)

    if st.button("دخول إلى النظام"):
        if selected_user == "اختر حساب المستخدم...":
            st.warning("⚠️ الرجاء اختيار حساب المستخدم أولاً.")
        else:
            st.query_params["page"] = "dashboard"
            st.query_params["user"] = selected_user
            st.rerun()

# ==================== الواجهة الثانية: لوحة التحكم والمهام ====================
else:
    user_role = current_user
    is_admin = "مشرف تنفيذي" in user_role

    # شريط علوي بعرض كامل لا يمكن أن يتقطع في الجوال
    st.markdown(f"""
        <div class="header-box">
            <div style="font-size: 18px; font-weight: bold; color: #196470; margin-bottom: 4px;">📋 نظام مهام الإدارة التنفيذية</div>
            <div style="font-size: 13px; color: #666; margin-bottom: 8px;">جمعية الدعوة والإرشاد وتوعية الجاليات بالمعابدة</div>
            <div style="font-size: 14px; color: #333; background: #eef5f6; padding: 6px 10px; border-radius: 6px;">👤 <b>المستخدم الحالي:</b> {user_role}</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 تسجيل الخروج والعودة للرئيسية"):
        st.query_params.clear()
        st.query_params["page"] = "login"
        st.rerun()

    # حساب الإحصائيات وعرضها في بطاقات متجاوبة
    visible_tasks = st.session_state.tasks if is_admin else [t for t in st.session_state.tasks if t['assignee'] == user_role]
    total_tasks = len(visible_tasks)
    completed_tasks = len([t for t in visible_tasks if t['status'] == 'منفذة'])

    st.markdown(f"""
        <div class="stats-container" style="margin-top: 15px;">
            <div class="stat-card">
                <div class="stat-num">{total_tasks}</div>
                <div class="stat-label">إجمالي المهام</div>
            </div>
            <div class="stat-card">
                <div class="stat-num" style="color: #2e7d32;">{completed_tasks}</div>
                <div class="stat-label">المهام المنفذة</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # قائمة تنقل منسدلة أو أزرار واضحة متوافقة 100% مع شاشات الجوال
    navigation = st.selectbox(
        "📌 اختر القسم المطلوب:",
        ["استعراض ومتابعة المهام", "إضافة مهمة جديدة", "إدارة أعضاء الفريق"]
    )
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

    # القسم الأول: استعراض المهام
    if navigation == "استعراض ومتابعة المهام":
        st.markdown("#### 📌 قائمة المهام التنفيذية")
        if not visible_tasks:
            st.info("لا توجد مهام مسجلة حالياً لهذا الحساب.")
        else:
            for t in visible_tasks:
                with st.expander(f"🔹 {t['title']} — ({t['status']})"):
                    st.markdown(f"**👤 المسؤول:** {t['assignee']}")
                    st.markdown(f"**📝 الوصف:** {t['desc']}")
                    st.markdown(f"**📅 تاريخ الاستحقاق:** `{t['date']}` | **⚡ الأولوية:** `{t['priority']}`")
                    
                    st.markdown("---")
                    status_list = ["قيد الانتظار", "قيد التنفيذ", "منفذة"]
                    current_idx = status_list.index(t['status']) if t['status'] in status_list else 0
                    
                    new_status = st.selectbox("تحديث حالة المهمة:", status_list, index=current_idx, key=f"status_{t['id']}")
                    if new_status != t['status']:
                        t['status'] = new_status
                        st.success("تم تحديث الحالة!")
                        st.rerun()
                        
                    if is_admin or t['assignee'] == user_role:
                        if st.button("🗑️ حذف المهمة", key=f"del_{t['id']}"):
                            st.session_state.tasks = [task for task in st.session_state.tasks if task['id'] != t['id']]
                            st.rerun()

    # القسم الثاني: إضافة مهمة جديدة
    elif navigation == "إضافة مهمة جديدة":
        st.markdown("#### ➕ إضافة مهمة تنفيذية جديدة")
        with st.form("new_task_form", clear_on_submit=True):
            title = st.text_input("عنوان المهمة")
            desc = st.text_area("وصف المهمة التفصيلي")
            assignee = st.selectbox("العضو المسؤول", st.session_state.team)
            date = st.date_input("تاريخ الاستحقاق", datetime.date.today())
            priority = st.selectbox("الأولوية", ["منخفضة", "متوسطة", "عالية"])
            status = st.selectbox("الحالة الأولية", ["قيد الانتظار", "قيد التنفيذ", "منفذة"])
            
            submitted = st.form_submit_button("💾 حفظ وإضافة المهمة")
            if submitted:
                if title.strip():
                    new_task = {
                        "id": str(datetime.datetime.now().timestamp()),
                        "title": title,
                        "desc": desc,
                        "assignee": assignee,
                        "date": str(date),
                        "status": status,
                        "priority": priority
                    }
                    st.session_state.tasks.append(new_task)
                    st.success("✅ تمت إضافة المهمة بنجاح! يمكنك رؤيتها في قسم استعراض المهام.")
                else:
                    st.error("⚠️ يرجى كتابة عنوان المهمة.")

    # القسم الثالث: إدارة أعضاء الفريق
    elif navigation == "إدارة أعضاء الفريق":
        st.markdown("#### 👥 إدارة أعضاء الإدارة التنفيذية")
        if is_admin:
            new_member = st.text_input("اسم العضو الجديد والمسمى الوظيفي (مثال: خالد العتيبي - العلاقات العامة)")
            if st.button("➕ إضافة عضو للنظام"):
                if new_member.strip() and new_member not in st.session_state.team:
                    st.session_state.team.append(new_member.strip())
                    st.success(f"✅ تمت إضافة ({new_member}) بنجاح!")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**📋 قائمة الأعضاء الحاليين:**")
            for idx, m in enumerate(st.session_state.team, 1):
                st.markdown(f"{idx}. {m}")
        else:
            st.warning("🔒 هذه الصلاحية مخصصة للمشرف التنفيذي (Admin) فقط.")
