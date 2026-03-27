import streamlit as st
from modules.styles import apply_styles
from modules.sidebar import render_sidebar
from modules.pages.home import show_home
from modules.pages.dashboard import show_dashboard
from modules.quiz import run_quiz
from modules.focus_timer import focus_timer
from modules.ai_chat import ai_chat
from modules.web_summary import show_web_summary


# cấu hình
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide"
)

# css
apply_styles()

# side bar
menu = render_sidebar()

# pages

if menu == "🏠 Trang chủ":
    show_home()

elif menu == "📊 Dashboard":
    show_dashboard()

elif menu == "📝 Quiz":
    run_quiz()

elif menu == "⏱ Focus Timer":
    focus_timer()

elif menu == "🤖 AI Chat":
    ai_chat()

elif menu == "🌐 Tóm tắt Web":
    show_web_summary()