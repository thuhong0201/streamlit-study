import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from modules.analysis import load_scores, analyze_scores
from modules.study_heatmap import show_heatmap


PLAN_FILE = "data/study_plan.csv"


def load_plan():
    if os.path.exists(PLAN_FILE):
        return pd.read_csv(PLAN_FILE)
    else:
        return pd.DataFrame(columns=["Subject", "Date", "Time", "Method"])


def save_plan(df):
    df.to_csv(PLAN_FILE, index=False)


def show_dashboard():
    """Hiển thị trang Dashboard kết quả học tập."""

    st.header("📊 Dashboard kết quả học tập")

    # heatmap
    show_heatmap()

    # nhập dữ liệu

    st.subheader("✏️ Nhập kết quả học tập")

    try:
        df = pd.read_csv("data/scores.csv")
    except:
        df = pd.DataFrame(columns=["Subject", "Score", "StudyHours"])

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True
    )

    if st.button("💾 Lưu dữ liệu"):
        edited_df.to_csv("data/scores.csv", index=False)
        st.success("Đã lưu dữ liệu!")

    # load data
    df = load_scores()

    if df.empty:
        st.warning("Chưa có dữ liệu điểm. Hãy nhập điểm trước.")
        st.stop()

    # bảng điểm

    st.subheader("📋 Bảng điểm")
    st.dataframe(df, use_container_width=True)

    # biểu đồ điểm

    st.subheader("📈 Biểu đồ điểm các môn")

    fig, ax = plt.subplots()
    ax.bar(df["Subject"], df["Score"])
    ax.set_ylabel("Score")
    ax.set_xlabel("Subject")
    st.pyplot(fig)

    # biểu đồ thời gian học

    if "StudyHours" in df.columns:
        st.subheader("⏱ Thời gian học")

        fig2, ax2 = plt.subplots()
        ax2.bar(df["Subject"], df["StudyHours"])
        ax2.set_ylabel("Study Hours")
        ax2.set_xlabel("Subject")
        st.pyplot(fig2)

    # phân tích kết quả

    st.subheader("📊 Phân tích kết quả học tập")

    df = analyze_scores(df)

    strong_subjects = df[df["Category"] == "Strong"]["Subject"].tolist()
    weak_subjects = df[df["Category"] == "Weak"]["Subject"].tolist()

    st.success(f"Môn mạnh: {', '.join(strong_subjects)}")
    st.warning(f"Môn cần cải thiện: {', '.join(weak_subjects)}")

    # kế hoạch
    st.header("📅 Lập kế hoạch học tập")

    plan_df = load_plan()

    st.subheader("➕ Thêm kế hoạch")

    subject = st.selectbox(
        "Môn học",
        ["Toán", "Lý", "Hóa", "Sinh", "Anh", "Tin", "Sử", "Địa", "GDCD"]
    )

    date = st.date_input("Ngày học")

    time = st.time_input("Giờ học")

    method = st.text_area(
        "Cách học",
        placeholder="Ví dụ: làm 10 bài tập, ôn chương 2..."
    )

    if st.button("Thêm kế hoạch"):

        new_row = pd.DataFrame({
            "Subject": [subject],
            "Date": [date],
            "Time": [time],
            "Method": [method]
        })

        plan_df = pd.concat([plan_df, new_row], ignore_index=True)

        save_plan(plan_df)

        st.success("Đã thêm kế hoạch!")

        st.rerun()

    st.subheader("📋 Danh sách kế hoạch học")

    if plan_df.empty:
        st.info("Chưa có kế hoạch học.")
    else:

        for i, row in plan_df.iterrows():

            col1, col2 = st.columns([8,1])

            with col1:
                st.write(
                    f"**{i+1}. {row['Subject']}** | "
                    f"📅 {row['Date']} | "
                    f"⏰ {row['Time']}  \n"
                    f"📖 {row['Method']}"
                )

            with col2:
                if st.button("❌", key=f"delete_{i}"):

                    plan_df = plan_df.drop(i).reset_index(drop=True)

                    save_plan(plan_df)

                    st.rerun()