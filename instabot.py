import streamlit as st
import streamlit.components.v1 as components

# ✅ Monetag verification (CORRECT WAY)
components.html(
"""
<head>
<meta name="monetag" content="39e4b7e52020ed41676ee541cdfd2fb2">
</head>
""",
height=0,
)

# Page config
st.set_page_config(page_title="Free Fire Glory Bot", page_icon="🔥")

st.title("🔥 Free Fire Glory Bot")
st.write("Monetag verification working page")
