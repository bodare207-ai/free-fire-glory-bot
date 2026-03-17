import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. THE "REAL" VERIFICATION INJECTOR ---
# This JavaScript code reaches out of the Streamlit iframe and 
# injects your meta tags into the main page <head>.
components.html(
    """
    <script>
    const head = window.parent.document.getElementsByTagName('head')[0];
    
    // Inject 7Search PPC Tag
    if (!window.parent.document.querySelector('meta[name="7searchppc"]')) {
        const meta7 = window.parent.document.createElement('meta');
        meta7.name = "7searchppc";
        meta7.content = "5b8d3e361b46def86de68b945a1f71cd";
        head.appendChild(meta7);
    }

    // Inject Monetag Tag
    if (!window.parent.document.querySelector('meta[name="monetag"]')) {
        const metaM = window.parent.document.createElement('meta');
        metaM.name = "monetag";
        metaM.content = "39e4b7e52020ed41676ee541cdfd2fb2";
        head.appendChild(metaM);
    }
    </script>
    """,
    height=0,
)

# --- 2. CONFIG & STYLING ---
st.set_page_config(page_title="Queen Arsenal Bot", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%);
        color: white; border: none; border-radius: 8px;
        height: 3em; width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception:
    st.error("⚠️ Supabase Keys Missing! Add them to Streamlit Secrets.")
    st.stop()

# --- 4. APP LOGIC ---
if 'page' not in st.session_state: st.session_state.page = "login"

if st.session_state.page == "login":
    st.title("👑 Queen Arsenal Bot")
    st.subheader("Login to start pushing Glory")
    email = st.text_input("Gmail Address")
    
    if st.button("Access Dashboard"):
        if "@" in email:
            # Sync user to DB
            supabase.table("users").upsert({"email": email}).execute()
            st.session_state.user_email = email
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Bot Menu")
    choice = st.sidebar.selectbox("Tools", ["🔥 Guild Glory Push", "💰 Earn Coins", "⚙️ Account Settings"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    if choice == "🔥 Guild Glory Push":
        st.header("🔥 Cloud Glory Pushing")
        st.write("Current Status: **Cloud Engine Online** 🟢")
        
        # SHOW AD BEFORE ALLOWING INPUT
        st.info("⚠️ Watch the ad below for 30 seconds to unlock the 'Start' button.")
        components.html("""
            <div style='text-align:center;'>
                <script type="text/javascript">
                    atags = { "id": "7SWB1069B7EB7EA18FF" };
                </script>
                <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
            </div>
        """, height=250)
        
        guild_id = st.text_input("Enter Guild ID", placeholder="1002345678")
        
        if st.button("🚀 Push Real Glory Now"):
            if len(guild_id) > 6:
                # Add to Queue for the Cloud Server to see
                job = {
                    "guild_id": guild_id,
                    "status": "pending",
                    "user": st.session_state.user_email,
                    "created_at": "now()"
                }
                supabase.table("bot_queue").insert(job).execute()
                st.success("✅ Job sent to Cloud! Our bots will join your guild in 1-5 minutes.")
            else:
                st.error("Please enter a valid Guild ID.")

    elif choice == "💰 Earn Coins":
        st.header("Claim Free Coins")
        st.write("Watch these daily ads to keep your bot running for free.")
        # Monetag Banner can go here
