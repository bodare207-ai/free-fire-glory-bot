import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import os

# --- 1. 7SEARCH PPC VERIFICATION (TOP PRIORITY) ---
# This method uses three different ways to ensure the crawler sees your tag.
# 1. HTML Component Injection
components.html(
    """
    <head>
        <meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/>
    </head>
    """,
    height=0,
)

# 2. Markdown Injection (Standard fallback)
st.markdown('<head><meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/></head>', unsafe_allow_html=True)

# 3. Hidden text for crawlers
st.write('<span style="display:none">7searchppc: 5b8d3e361b46def86de68b945a1f71cd</span>', unsafe_allow_html=True)


# --- 2. DATABASE CONNECTION SETUP ---
def check_secrets():
    """Verify that secrets are configured in Streamlit Cloud Settings."""
    try:
        return "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets
    except Exception:
        return False

# Page Configuration
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

if not check_secrets():
    st.error("⚠️ Secrets Configuration Error!")
    st.info("Log in to Streamlit Cloud, go to **App Settings > Secrets**, and paste your Supabase keys.")
    st.stop()

# Initialize Supabase Client
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)


# --- 3. STATE MANAGEMENT ---
if 'page' not in st.session_state: 
    st.session_state.page = "lobby"
if 'user_email' not in st.session_state: 
    st.session_state.user_email = ""


# --- 4. LOBBY INTERFACE ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    st.write("---")
    
    with st.container():
        st.subheader("Login to your Account")
        email = st.text_input("Enter Gmail Address", placeholder="example@gmail.com")
        
        if st.button("🚀 Enter Dashboard"):
            if email and "@" in email:
                try:
                    # Check if user exists, otherwise create them
                    user_query = supabase.table("users").select("*").eq("email", email).execute()
                    if not user_query.data:
                        supabase.table("users").insert({"email": email, "coins": 0}).execute()
                    
                    st.session_state.user_email = email
                    st.session_state.page = "dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Database Error: {e}")
            else:
                st.warning("Please enter a valid Gmail address.")
    
    st.write("---")
    st.caption("Site Verification Active: 5b8d3e361b46def86de68b945a1f71cd")


# --- 5. DASHBOARD INTERFACE ---
elif st.session_state.page == "dashboard":
    # Sidebar Navigation
    st.sidebar.title("💎 Queen Menu")
    
    # Live Coin Counter
    try:
        user_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = user_res.data[0]['coins'] if user_res.data else 0
        st.sidebar.metric("Your Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Failed")

    st.sidebar.write(f"User: **{st.session_state.user_email}**")
    
    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.user_email = ""
        st.rerun()

    # --- PAGE ROUTING ---
    if menu == "🔥 Guild Glory Pusher":
        # Using encoding='utf-8' to prevent UnicodeErrors with emojis
        try:
            with open("glory_push.py", "r", encoding="utf-8") as f:
                code = f.read()
                exec(code)
        except FileNotFoundError:
            st.error("❌ `glory_push.py` file missing from repository.")
        except Exception as e:
            st.error(f"❌ Error in Pusher Script: {e}")

    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        st.write("Watch ads or complete offers below to earn coins.")
        st.divider()
        # This is where your 7Search PPC Ad code will eventually go
        st.info("Integration with 7Search PPC Ads is currently being verified...")

    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Glory Pushers")
        try:
            leaders = supabase.table("users").select("email, coins").order("coins", desc=True).limit(10).execute()
            if leaders.data:
                for idx, entry in enumerate(leaders.data):
                    st.write(f"{idx+1}. **{entry['email']}** — {entry['coins']} Coins")
            else:
                st.write("Leaderboard is empty. Be the first to push!")
        except:
            st.write("Leaderboard currently offline.")
