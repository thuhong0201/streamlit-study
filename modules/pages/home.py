import streamlit as st


def show_home():
    """Hiển thị trang chủ."""

    st.markdown("""
    <div class="title">📚 AI Study Planner</div>
    <div class="subtitle">
    Hệ thống hỗ trợ phân tích kết quả học tập và lập kế hoạch học tập cá nhân bằng AI
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 Các chức năng chính")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">📊 Dashboard</div>
            <div class="card-text">
            Xem biểu đồ điểm các môn và phân tích kết quả học tập
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">📝 Quiz</div>
            <div class="card-text">
            Làm bài kiểm tra để đánh giá kiến thức
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">⏱ Focus Timer</div>
            <div class="card-text">
            Theo dõi thời gian học tập và tập trung
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
            <div class="card-title">🤖 AI Coach</div>
            <div class="card-text">
            Nhận tư vấn học tập thông minh từ AI
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="card">
            <div class="card-title">📚Web Summary</div>
            <div class="card-text">
            Tóm tắt website bằng AI
            </div>
        </div>
        """, unsafe_allow_html=True)

