import streamlit as st
import time
import pandas as pd
from datetime import datetime


@st.fragment(run_every="1s")
def display_timer():

    start_time = st.session_state.get("start_time")
    elapsed = st.session_state.get("elapsed", 0)

    # nếu timer đang chạy
    if start_time is not None:
        current_elapsed = elapsed + int(time.time() - start_time)
    else:
        current_elapsed = elapsed

    minutes = current_elapsed // 60
    seconds = current_elapsed % 60

    st.markdown(f"### ⏱ {minutes:02}:{seconds:02}")


def focus_timer():

    st.subheader("Focus Timer")

    # khởi tạo session state
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    if "elapsed" not in st.session_state:
        st.session_state.elapsed = 0

    is_running = st.session_state.start_time is not None

    col1, col2 = st.columns(2)

    # start
    with col1:
        if st.button("▶ Start Study", disabled=is_running):
            st.session_state.start_time = time.time()
            st.rerun()

    # stop
    with col2:
        if st.button("⏹ Stop Study", disabled=not is_running):

            if st.session_state.start_time is not None:

                st.session_state.elapsed += int(
                    time.time() - st.session_state.start_time
                )

                st.session_state.start_time = None

                st.rerun()

    # hiển thị timer
    display_timer()

    # save time
    if st.button("💾 Lưu thời gian học"):

        current_elapsed = st.session_state.get("elapsed", 0)
        if st.session_state.get("start_time") is not None:
            current_elapsed += int(time.time() - st.session_state.start_time)

        if current_elapsed > 0:

            hours_studied = current_elapsed / 3600
            today = datetime.now().strftime("%Y-%m-%d")

            try:
                log_df = pd.read_csv("data/study_log.csv")
            except:
                log_df = pd.DataFrame(columns=["date", "hours"])

            # nếu hôm nay đã có
            if today in log_df["date"].values:
                log_df.loc[log_df["date"] == today, "hours"] += hours_studied
            else:
                new_row = pd.DataFrame({
                    "date": [today],
                    "hours": [hours_studied]
                })
                log_df = pd.concat([log_df, new_row], ignore_index=True)

            log_df.to_csv("data/study_log.csv", index=False)

            st.success(f"Đã lưu {hours_studied:.2f} giờ học hôm nay!")

            # reset timer
            st.session_state.elapsed = 0
            st.session_state.start_time = None

        else:
            st.warning("Chưa có thời gian học để lưu!")