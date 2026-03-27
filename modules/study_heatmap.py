import pandas as pd
import plotly.express as px
import streamlit as st

def show_heatmap():

    df = pd.read_csv("data/study_log.csv")

    df["date"] = pd.to_datetime(df["date"])

    df["weekday"] = df["date"].dt.day_name()
    df["week"] = df["date"].dt.isocalendar().week

    heatmap = df.pivot_table(
        values="hours",
        index="weekday",
        columns="week",
        fill_value=0
    )

    fig = px.imshow(
        heatmap,
        color_continuous_scale="Blues",
        labels=dict(color="Study hours")
    )

    st.subheader("📅 Study Activity Heatmap")

    st.plotly_chart(fig, use_container_width=True)