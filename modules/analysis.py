import pandas as pd
import streamlit as st


# đọc dữ liệu điểm
def load_scores():
    try:
        df = pd.read_csv("data/scores.csv")
    except:
        df = pd.DataFrame(columns=["Subject", "Score", "StudyHours"])
    return df

# phân tích điểm
def analyze_scores(df):
    if df.empty:
        df["Category"] = []
        return df

    def categorize(score):
        try:
            val = float(score)
            if val >= 8.0:
                return "Strong"
            else:
                return "Weak"
        except:
            return "Weak"
            
    df["Category"] = df["Score"].apply(categorize)
    return df