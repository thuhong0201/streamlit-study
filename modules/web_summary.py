import streamlit as st
import google.generativeai as genai

def show_web_summary():
    st.title("🌐 Tóm tắt Website")
    st.markdown("Nhập một đường link (URL) bất kỳ để AI đọc và tóm tắt lại nội dung chính cho bạn.")

    # Cấu hình Gemini
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("Chưa cấu hình GEMINI_API_KEY trong .streamlit/secrets.toml")
        return
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.5-flash')

    url = st.text_input("🔗 Nhập URL trang web cần tóm tắt:", placeholder="Ví dụ: https://vnexpress.net/...")

    if st.button("✨ Tóm tắt ngay"):
        if not url:
            st.warning("Vui lòng nhập URL hợp lệ!")
            return
            
        if not url.startswith("http"):
            url = "https://" + url

        prompt = f"""Hãy tóm tắt nội dung trang web từ URL sau một cách ngắn gọn, dễ hiểu, nêu ý chính:
Hãy đọc nội dung từ URL sau và tóm tắt:
- Ý chính
- 5–7 gạch đầu dòng quan trọng
- Kết luận ngắn

URL: {url}"""

        with st.spinner("🤖 AI đang đọc và tóm tắt trang web..."):
            try:
                response = model.generate_content(prompt)
                st.success("✅ Tóm tắt thành công!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra khi tóm tắt: {str(e)}")
