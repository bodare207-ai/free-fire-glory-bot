import streamlit as st
from supabase import create_client
import os

# --- 1. VERIFICATION (7Search PPC) ---
# This injects your new meta tag into the website's head
st.markdown(
    f"""
    <script>
        var meta = document.createElement('meta');
        meta.name = "7searchppc";
        meta.content = "5b8d3e361b46def86de68b945a1f71cd";
        document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """, 
    unsafe_allow_html=True
)

# --- 2. DATABASE CONNECTION ---
def check_secrets():
    try:
        return "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets
    except Exception:
        return False

# Page Config
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

if not check_secrets():
    st.error("⚠️ Secrets Configuration Error!")
    st.info("On Streamlit Cloud, go to **Settings > Secrets** and paste your Supabase keys there.")
    st.stop()

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
    
    email = st.text_input("Enter Gmail to Login", placeholder="example@gmail.com")
    if st.button("🚀 Enter Dashboard"):
        if email and "@" in email:
            try:
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

# --- 5. DASHBOARD INTERFACE ---
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Queen Menu")
    
    # Coin Balance
    try:
        user_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = user_res.data[0]['coins'] if user_res.data else 0
        st.sidebar.metric("Your Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Failed")

    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.rerun()

    # Routing
    if menu == "🔥 Guild Glory Pusher":
        try:
            with open("glory_push.py", "r", encoding="utf-8") as f:
                exec(f.read())
        except Exception as e:
            st.error(f"Error loading Pusher: {e}")

    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        st.write("Watch ads to earn glory coins!")
        st.info("Earning module is being integrated with 7Search PPC Ads.")

    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Pushers")
        try:
            leaders = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            for i, p in enumerate(leaders.data):
                st.write(f"{i+1}. **{p['email']}** — {p['coins']} Coins")
        except:
            st.write("Updating...")
