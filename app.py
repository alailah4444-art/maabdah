import streamlit as st
import datetime
import os

# تحديد أيقونة الصفحة بالشعار الرسمي للجمعية إذا وجد، وإلا فأيقونة افتراضية
page_icon_path = "logo.jpg" if os.path.exists("logo.jpg") else ("logo.png" if os.path.exists("logo.png") else "🕋")

# إعدادات الصفحة والهوية البصرية للجمعية وتفعيل اتجاه اليمين لليسار (RTL)
st.set_page_config(page_title="مهام الإدارة التنفيذية - جمعية الدعوة بالمعابدة", page_icon=page_icon_path, layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }
    .main { background-color: #F4F3F4; }
    .stButton>button { background-color: #196470; color: white; border-radius: 12px; font-weight: bold; width: 100%; padding: 10px; }
    .stButton>button:hover { background-color: #278E8E; color: white; }
    .stSelectbox, .stTextInput, .stTextArea { text-align: right; }
    </style>
""", unsafe_allow_html=True)

# تهيئة البيانات في الجلسة
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"id": "1", "title": "متابعة برامج توعية الجاليات الأسبوعية", "desc": "تجهيز القاعات والمحاضرين للبرامج الدعوية", "assignee": "عبدالله السلمي (قسم الجاليات)", "date": "2026-06-15", "status": "قيد التنفيذ", "priority": "عالية"},
        {"id": "2", "title": "تقرير انجاز الحملات الرمضانية", "desc": "حصر أعداد المستفيدين من البرامج", "assignee": "سعد القرشي (البرامج الدعوية)", "date": "2026-05-10", "status": "منفذة", "priority": "متوسطة"}
    ]

if 'team' not in st.session_state:
    st.session_state.team = [
        'عبدالله السلمي (قسم الجاليات)',
        'سعد القرشي (البرامج الدعوية)',
        'ساره أحمد (الإدارة المالية)',
        'محمد خالد (العلاقات العامة)'
    ]

# قراءة حالة الصفحة من الرابط لتفعيل زر المتصفح (السهم)
query_params = st.query_params
page_mode = query_params.get("section", "login")

if page_mode == "login":
    st.session_state.logged_in_user = None

# ==================== شاشة تسجيل الدخول الرئيسية ====================
if st.session_state.get('logged_in_user') is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if os.path.exists("logo.jpg"):
            st.image("logo.jpg", width=220)
        elif os.path.exists("logo.png"):
            st.image("logo.png", width=220)
            
        st.markdown("<h1 style='text-align: center; color: #196470;'>الإدارة التنفيذية</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #555; font-size: 16px;'><b>جمعية الدعوة والإرشاد وتوعية الجاليات بالمعابدة</b></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("<h4 style='text-align: right;'>اختر صفة الدخول للنظام:</h4>", unsafe_allow_html=True)
        
        login_option = st.selectbox("اختر حسابك:", ["اختر حساب المستخدم..."] + ["مشرف تنفيذي (Admin - صلاحيات كاملة)"] + st.session_state.team, key="login_select")
        
        if st.button("دخول إلى النظام"):
            if login_option == "اختر حساب المستخدم...":
                st.warning("الرجاء اختيار حساب صحيح للبدء.")
            else:
                st.session_state.logged_in_user = login_option
                st.query_params["section"] = "dashboard"
                st.rerun()

# ==================== لوحة التحكم الرئيسية بعد الدخول ====================
else:
    user_role = st.session_state.logged_in_user
    is_admin = "مشرف تنفيذي" in user_role

    # الشريط الجانبي
    if os.path.exists("logo.jpg"):
        st.sidebar.image("logo.jpg", width=180)
    elif os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=180)

    st.sidebar.markdown(f"<h3 style='color: #196470; text-align: right;'>مرحباً، {user_role}</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    if st.sidebar.button("تسجيل الخروج (الرئيسية)"):
        st.session_state.logged_in_user = None
        st.query_params["section"] = "login"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='text-align: right;'>📊 لوحة التحكم السريعة</h3>", unsafe_allow_html=True)
    
    visible_tasks_count = st.session_state.tasks if is_admin else [t for t in st.session_state.tasks if t['assignee'] == user_role]
    total_tasks = len(visible_tasks_count)
    completed_tasks = len([t for t in visible_tasks_count if t['status'] == 'منفذة'])
    
    st.sidebar.metric(label="إجمالي المهام", value=total_tasks)
    st.sidebar.metric(label="المهام المنفذة", value=completed_tasks)

    # الواجهة الرئيسية
    st.markdown("<h1 style='text-align: right;'>📋 نظام مهام الإدارة التنفيذية</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: right; color: #555;'>جمعية الدعوة والإرشاد وتوعية الجاليات بالمعابدة</h4>", unsafe_allow_html=True)
    st.markdown("---")

    navigation = st.radio("القائمة الرئيسية:", ["📌 استعراض ومتابعة المهام", "➕ إضافة مهمة جديدة", "👥 إدارة أعضاء الفريق"], horizontal=True)
    st.markdown("---")

    if navigation == "📌 استعراض ومتابعة المهام":
        st.subheader("قائمة المهام التنفيذية")
        current_user_name = user_role if not is_admin else "الكل"
        display_tasks = st.session_state.tasks if is_admin else [t for t in st.session_state.tasks if t['assignee'] == current_user_name]

        if not display_tasks:
            st.info("لا توجد مهام مسجلة حالياً.")
        else:
            for t in display_tasks:
                with st.expander(f"📌 {t['title']} — المسؤول: {t['assignee']} ({t['status']})"):
                    st.write(f"**الوصف:** {t['desc']}")
                    st.write(f"**تاريخ الاستحقاق:** {t['date']} | **الأولوية:** {t['priority']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox("تحديث الحالة", ["قيد الانتظار", "قيد التنفيذ", "منفذة"], index=["قيد الانتظار", "قيد التنفيذ", "منفذة"].index(t['status']), key=f"status_{t['id']}")
                        if new_status != t['status']:
                            t['status'] = new_status
                            st.rerun()
                    with col2:
                        if is_admin or t['assignee'] == current_user_name:
                            if st.button("حذف المهمة", key=f"del_{t['id']}"):
                                st.session_state.tasks = [task for task in st.session_state.tasks if task['id'] != t['id']]
                                st.rerun()

    elif navigation == "➕ إضافة مهمة جديدة":
        st.subheader("إضافة مهمة تنفيذية جديدة")
        with st.form("new_task_form"):
            title = st.text_input("عنوان المهمة")
            desc = st.text_area("وصف المهمة التفصيلي")
            assignee = st.selectbox("العضو المسؤول", st.session_state.team)
            date = st.date_input("تاريخ الاستحقاق", datetime.date.today())
            priority = st.selectbox("الأولوية", ["منخفضة", "متوسطة", "عالية"])
            status = st.selectbox("الحالة الأولية", ["قيد الانتظار", "قيد التنفيذ", "منفذة"])
            
            submitted = st.form_submit_button("حفظ وإضافة المهمة")
            if submitted and title:
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
                st.success("تمت إضافة المهمة بنجاح!")
                st.rerun()

    elif navigation == "👥 إدارة أعضاء الفريق":
        st.subheader("إدارة أعضاء الإدارة التنفيذية")
        if is_admin:
            new_member = st.text_input("اسم العضو الجديد أو القسم")
            if st.button("إضافة عضو للنظام"):
                if new_member and new_member not in st.session_state.team:
                    st.session_state.team.append(new_member)
                    st.success(f"تمت إضافة {new_member} بنجاح!")
                    st.rerun()
            
            st.markdown("**الأعضاء الحاليون:**")
            for m in st.session_state.team:
                st.write(f"- {m}")
        else:
            st.warning("هذه الصفحة مخصصة للمشرف التنفيذي (Admin) فقط لإدارة الأعضاء.")