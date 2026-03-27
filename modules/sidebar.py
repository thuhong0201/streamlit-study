import streamlit as st
import pandas as pd
from datetime import datetime


def render_sidebar():
    """Hiển thị sidebar với menu, thống kê và thông tin người dùng. Trả về menu đã chọn."""

    st.sidebar.title("📚 AI Study Planner")

    menu = st.sidebar.selectbox(
        "Chọn chức năng",
        [
            "🏠 Trang chủ",
            "📊 Dashboard",
            "📝 Quiz",
            "⏱ Focus Timer",
            "🤖 AI Chat",
            "🌐 Tóm tắt Web"
        ]
    )

    st.sidebar.markdown("---")

    # tính toán dữ liệu tự động
    total_hours, streak, progress, progress_pct = _compute_study_stats()
    total_quizzes = _compute_quiz_count()
    avg_score = _compute_avg_score()

    # user profile
    st.sidebar.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=80
    )

    st.sidebar.markdown("""
    **👤 Thu Hồng**  
    🎓 Học sinh
    """)

    # progress
    st.sidebar.markdown("### 📈 Tiến độ học tập")
    st.sidebar.progress(progress)
    st.sidebar.caption(f"Bạn đã hoàn thành **{progress_pct}% mục tiêu tuần này** 🎯")

    # quick star
    st.sidebar.markdown("### 📊 Thống kê")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Giờ học", f"{total_hours:.1f}h")
    with col2:
        st.metric("Quiz", f"{total_quizzes}")

    st.sidebar.metric("Điểm trung bình", f"{avg_score:.1f}")

    # streak
    st.sidebar.markdown("### 🔥 Study Streak")
    st.sidebar.success(f"Bạn đã học **{streak} ngày liên tiếp**!")

    # motivation
    st.sidebar.markdown("### 💡 Motivation")
    
    quote_dict = {
        "Beginner": "The expert in anything was once a beginner.",
        "Impossible": "It always seems impossible until it's done.",
        "Don't Stop": "Don't stop when you're tired. Stop when you're done.",
        "Courage": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Believe": "Believe you can and you're halfway there.",
        "Future": "Do something today that your future self will thank you for.",
        "Hành trình": "Hành trình vạn dặm bắt đầu từ một bước chân.",
        "Thành công": "Trên bước đường thành công không có dấu chân của kẻ lười biếng."
    }
    
    options = ["🎲 Ngẫu nhiên"] + list(quote_dict.keys())
    choice = st.sidebar.selectbox("Chọn câu nói:", options)
    
    import random
    if choice == "🎲 Ngẫu nhiên":
        if "random_quote" not in st.session_state:
            st.session_state.random_quote = random.choice(list(quote_dict.values()))
        
        st.sidebar.info(f"*{st.session_state.random_quote}*")
        
        if st.sidebar.button("🔄 Đổi câu"):
            st.session_state.random_quote = random.choice(list(quote_dict.values()))
            st.rerun()
    else:
        st.sidebar.info(f"*{quote_dict[choice]}*")

    # footer
    st.sidebar.markdown("---")
    st.sidebar.caption("AI Study Planner v1.0")

    return menu


def _compute_study_stats():
    """Tính tổng giờ học, streak, tiến độ tuần."""
    try:
        study_df = pd.read_csv("data/study_log.csv")
        total_hours = study_df["hours"].sum()

        # Tính streak
        study_df['date'] = pd.to_datetime(study_df['date']).dt.normalize()
        daily = study_df.groupby('date')['hours'].sum().reset_index()
        active_dates = sorted(daily[daily['hours'] > 0]['date'].unique(), reverse=True)

        streak = 0
        today = pd.to_datetime(datetime.now().date())

        if len(active_dates) > 0:
            if active_dates[0] == today:
                current_date = today
            elif active_dates[0] == today - pd.Timedelta(days=1):
                current_date = today - pd.Timedelta(days=1)
            else:
                current_date = None

            if current_date is not None:
                for d in active_dates:
                    if d == current_date:
                        streak += 1
                        current_date -= pd.Timedelta(days=1)
                    else:
                        break

        # Tính tiến độ tuần (mục tiêu 10h/tuần)
        one_week_ago = today - pd.Timedelta(days=7)
        week_hours = study_df[study_df['date'] >= one_week_ago]['hours'].sum()
        progress = min(week_hours / 10.0, 1.0)
        progress_pct = int(progress * 100)

        return total_hours, streak, progress, progress_pct
    except:
        return 0, 0, 0.0, 0


def _compute_quiz_count():
    """Tính tổng số quiz đã làm."""
    try:
        quiz_df = pd.read_csv("data/quiz_log.csv")
        return len(quiz_df)
    except:
        return 0

def _compute_avg_score():
    """Tính điểm trung bình."""
    try:
        score_df = pd.read_csv("data/scores.csv")
        return score_df["Score"].mean()
    except:
        return 0.0
