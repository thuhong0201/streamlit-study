import streamlit as st


def apply_styles():
    """Áp dụng CSS tùy chỉnh cho ứng dụng."""
    st.markdown("""
    <style>

    .stApp{
    background-image: url("https://cdn-media.sforum.vn/storage/app/media/ctvseo_15/Background%20xanh/background-xanh-1.jpg");
    background-size: cover;
    background-attachment: fixed;
    }

    .title{
    font-size:50px;
    font-weight:800;
    text-align:center;
    color:white;
    }

    .subtitle{
    text-align:center;
    color:#cbd5f5;
    margin-bottom:40px;
    }

    .card{
    padding:30px;
    border-radius:18px;
    background: rgba(30,41,59,0.7);
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
    transition:0.3s;
    }

    .card:hover{
    transform:translateY(-6px);
    border:1px solid #38bdf8;
    box-shadow:0px 0px 20px rgba(56,189,248,0.5);
    }

    .card-title{
    font-size:20px;
    font-weight:600;
    margin-bottom:10px;
    }

    .card-text{
    color:#cbd5f5;
    }

    .section-title{
    font-size:28px;
    font-weight:700;
    color:white;
    margin-bottom:20px;
    }

    .footer{
    text-align:center;
    color:#94a3b8;
    margin-top:40px;
    }

    </style>
    """, unsafe_allow_html=True)
