# cấu hình gemini

import streamlit as st
import random
import html
import json
from datetime import datetime

import google.generativeai as genai

def get_gemini_client():

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        st.error("Chưa cấu hình GEMINI_API_KEY")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    return model

# tạo câu hỏi

def generate_questions_with_ai(model, subject, grade, difficulty, amount, q_type):
    """Gọi Gemini để sinh câu hỏi quiz."""

    difficulty_map = {
        "easy": "dễ",
        "medium": "trung bình",
        "hard": "khó"
    }
    diff_vi = difficulty_map.get(difficulty, "trung bình")

    if q_type == "multiple":
        type_instruction = "trắc nghiệm 4 đáp án (1 đúng, 3 sai)"
        json_format = '''[
  {
    "question": "Nội dung câu hỏi?",
    "correct_answer": "Đáp án đúng",
    "incorrect_answers": ["Đáp án sai 1", "Đáp án sai 2", "Đáp án sai 3"],
    "explanation": "Giải thích chi tiết vì sao đây là đáp án đúng"
  }
]'''
    else:
        type_instruction = "đúng/sai (True/False)"
        json_format = '''[
  {
    "question": "Nội dung câu hỏi?",
    "correct_answer": "True",
    "incorrect_answers": ["False"],
    "explanation": "Giải thích chi tiết vì sao mệnh đề này đúng hoặc sai"
  }
]'''

    if subject == "English":
        language_instruction = "Generate all questions and answers in ENGLISH."
    else:
        language_instruction = "Tạo toàn bộ câu hỏi và đáp án bằng TIẾNG VIỆT."

    prompt = f"""Bạn là một giáo viên chuyên nghiệp. Hãy tạo {amount} câu hỏi {type_instruction} về môn {subject} cho học sinh lớp {grade}, độ khó: {diff_vi}.

{language_instruction}

Yêu cầu:
- Câu hỏi phải chính xác về mặt kiến thức.
- Đáp án đúng phải chính xác.
- Các đáp án sai phải hợp lý nhưng sai.
- Câu hỏi phải đa dạng, không nên quá giống nhau.
- Phù hợp với chương trình giáo dục Việt Nam lớp {grade}.
- TUYỆT ĐỐI KHÔNG sử dụng ký hiệu LaTeX (như $, \\infty, \\cap, \\vec, \\le, \\ge, \\sqrt, v.v.). Hãy viết công thức toán bằng Unicode hoặc chữ viết thông thường. Ví dụ: viết "x² - 5x + 6 ≤ 0" thay vì "$x^2 - 5x + 6 \\le 0$", viết "√13" thay vì "$\\sqrt{{13}}$", viết "vectơ AB" thay vì "$\\vec{{AB}}$".
- Kết quả JSON phải hợp lệ, không chứa ký tự backslash đặc biệt ngoài các escape chuẩn JSON (\\n, \\t, \\\", \\\\).

Trả về KẾT QUẢ ĐÚNG THEO ĐỊNH DẠNG JSON sau (CHỈ TRẢ VỀ JSON, KHÔNG CÓ GÌ KHÁC):
{json_format}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

       
        if text.startswith("```"):
            text = text.split("\n", 1)[1]  # Bỏ dòng đầu ```json
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]  # Bỏ ``` cuối
        text = text.strip()

        import re

        text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)

        questions = json.loads(text)
        return questions
    except json.JSONDecodeError as e:
        st.error(f"❌ Lỗi phân tích kết quả từ AI: {e}")
        st.code(text, language="json")
        return None
    except Exception as e:
        st.error(f"❌ Lỗi khi gọi AI: {e}")
        return None


# quiz

def run_quiz():

    st.title("📝 Quiz kiểm tra kiến thức")

    # môn

    subject = st.selectbox(
        "Chọn môn học",
        ["English", "Toán", "Hóa học", "Lịch sử", "Tin học", "Sinh học", "Vật lý", "Địa lý", "GDCD"]
    )

    # lớp

    grade = st.selectbox(
        "Chọn lớp",
        ["10", "11", "12"]
    )

    # độ khó

    difficulty = st.selectbox(
        "Chọn độ khó",
        ["easy", "medium", "hard"]
    )

    # số lượng

    amount = st.selectbox(
        "Số lượng câu hỏi",
        [5, 10, 15, 20]
    )

    # ===== LOẠI CÂU HỎI =====

    q_type_display = st.selectbox(
        "Loại câu hỏi",
        ["Trắc nghiệm", "Đúng/Sai"]
    )
    
    q_type = "multiple" if q_type_display == "Trắc nghiệm" else "boolean"

    # tạo đề

    if st.button("🎲 Tạo đề mới"):

        model = get_gemini_client()
        if model is None:
            st.stop()

        with st.spinner("🤖 AI đang tạo đề thi... Vui lòng chờ..."):
            questions = generate_questions_with_ai(model, subject, grade, difficulty, amount, q_type)

        if questions is None:
            st.error("Không thể tạo đề thi. Vui lòng thử lại.")
            st.stop()

        st.session_state.questions = questions
        st.session_state.start_time = datetime.now()
        st.session_state.quiz_subject = subject
        st.session_state.quiz_difficulty = difficulty
        st.session_state.quiz_amount = amount

        # Xáo trộn đáp án 1 lần duy nhất và lưu vào session_state
        shuffled = []
        for q in questions:
            opts = q["incorrect_answers"] + [q["correct_answer"]]
            random.shuffle(opts)
            shuffled.append(opts)
        st.session_state.shuffled_options = shuffled
        st.success(f"✅ Đã tạo {len(questions)} câu hỏi thành công!")

    # lịch sử
    
    with st.expander("📈 Xem lịch sử làm bài"):
        try:
            import pandas as pd
            history_df = pd.read_csv("data/quiz_log.csv")
            history_df = history_df.sort_values(by="date", ascending=False)
            
            display_cols = [c for c in history_df.columns if c != "details"]
            st.dataframe(history_df[display_cols], use_container_width=True)
            
            if "details" in history_df.columns and not history_df.empty:
                # Chỉ lấy các bản ghi có dữ liệu chi tiết thật sự
                valid_history = history_df[history_df["details"].notna() & (history_df["details"] != "")]
                
                if not valid_history.empty:
                    st.write("---")
                    st.subheader("🔍 Xem chi tiết bài làm")
                    
                    def format_option(r):
                        subj = r.get('subject', 'N/A')
                        sc = r.get('score', 0)
                        total = r.get('total_questions', 5)
                        return f"{r['date']} | Môn: {subj} | Điểm: {sc}/{total}"
                        
                    options = valid_history.apply(format_option, axis=1).tolist()
                    selected_option = st.selectbox("Chọn bài làm muốn xem:", options)
                    
                    if selected_option:
                        selected_date = selected_option.split(" | ")[0]
                        row = valid_history[valid_history["date"] == selected_date].iloc[0]
                        
                        try:
                            details_data = json.loads(row["details"])
                            for idx, item in enumerate(details_data):
                                st.markdown(f"**Câu {idx+1}: {item['question']}**")
                                if item['is_correct']:
                                    st.success(f"✅ Đáp án của bạn: {item['user_answer']} (Chính xác)")
                                else:
                                    st.error(f"❌ Đáp án của bạn: {item['user_answer']} — Đáp án đúng: {item['correct_answer']}")
                                if "explanation" in item:
                                    st.info(f"💡 **Giải thích:** {item['explanation']}")
                        except:
                            st.write("Không thể tải chi tiết câu hỏi cho bài làm này.")
        except:
            st.write("Chưa có dữ liệu lịch sử.")

    # chưa có đề

    if "questions" not in st.session_state:

        st.info("Nhấn 'Tạo đề mới' để bắt đầu")

        return

    # quiz

    st.subheader("📚 Bài kiểm tra")

    answers = []

    for i, q in enumerate(st.session_state.questions):

        question = q["question"]

        st.write(f"### Câu {i+1}: {question}")

        # Sử dụng thứ tự đáp án đã được xáo trộn sẵn
        options = st.session_state.shuffled_options[i]

        answer = st.radio(
            "Chọn đáp án",
            options,
            key=f"quiz_q_{i}"
        )

        answers.append(answer)

    # nộp bài

    if st.button("📊 Nộp bài"):

        score = 0
        details = []

        st.subheader("📋 Kết quả")

        for i, q in enumerate(st.session_state.questions):

            correct = q["correct_answer"]
            user = answers[i]
            question_text = q["question"]
            explanation = q.get("explanation", "Không có giải thích chi tiết.")
            is_correct = (user == correct)

            details.append({
                "question": question_text,
                "user_answer": user,
                "correct_answer": correct,
                "is_correct": is_correct,
                "explanation": explanation
            })

            if is_correct:

                st.success(f"Câu {i+1}: Đúng")

                score += 1

            else:

                st.error(
                    f"Câu {i+1}: Sai — Đáp án đúng: {correct}"
                )

            st.info(f"💡 **Giải thích:** {explanation}")

        st.write("")

        total_questions = len(st.session_state.questions)
        st.success(f"🎉 Điểm của bạn: {score}/{total_questions}")

        # Tính thời gian
        end_time = datetime.now()
        start_time = st.session_state.get('start_time', end_time)
        time_taken = (end_time - start_time).seconds
        
        st.info(f"⏱ Thời gian hoàn thành: {time_taken} giây")

        # Lưu kết quả quiz
        import pandas as pd
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_file = "data/quiz_log.csv"
        try:
            q_df = pd.read_csv(log_file)
            if "subject" not in q_df.columns:
                q_df["subject"] = "N/A"
                q_df["difficulty"] = "N/A"
                q_df["total_questions"] = 5
                q_df["time_taken_seconds"] = 0
            if "details" not in q_df.columns:
                q_df["details"] = ""
        except:
            q_df = pd.DataFrame(columns=["date", "subject", "difficulty", "score", "total_questions", "time_taken_seconds", "details"])
            
        details_str = json.dumps(details, ensure_ascii=False)
            
        new_row = pd.DataFrame({
            "date": [today],
            "subject": [st.session_state.get('quiz_subject', "N/A")],
            "difficulty": [st.session_state.get('quiz_difficulty', "N/A")],
            "score": [score],
            "total_questions": [total_questions],
            "time_taken_seconds": [time_taken],
            "details": [details_str]
        })
        q_df = pd.concat([q_df, new_row], ignore_index=True)
        q_df.to_csv(log_file, index=False)
        st.info("Đã lưu kết quả bài Quiz (Kèm chi tiết câu hỏi)!")