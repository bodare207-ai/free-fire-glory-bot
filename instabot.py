import streamlit as st
from supabase import create_client
import os

# 1. Verification Meta Tag for 7Search PPC
st.markdown('<script>var meta=document.createElement("meta");meta.name="7searchppc";meta.content="194331a7fabe56c358637d4c992dbb62";document.getElementsByTagName("head")[0].appendChild(meta);</script>', unsafe_allow_html=True)

# 2. Database Connection
# This looks for SUPABASE_URL and SUPABASE_KEY in your .streamlit/secrets.toml
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error("⚠️ Secrets Configuration Error!")
    st.info("Check that your .streamlit/secrets.toml file exists and has the correct keys.")
    st.stop()

# 3. Page Configuration
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

# 4. Custom CSS for Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 5. State Management
if 'page' not in st.session_state: 
    st.session_state.page = "lobby"
if 'user_email' not in st.session_state: 
    st.session_state.user_email = ""

# --- 6. LOBBY INTERFACE ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    st.write("Welcome to the ultimate Free Fire Glory Pushing Hub.")
    
    with st.container():
        email = st.text_input("Enter your Gmail Address", placeholder="example@gmail.com")
        
        if st.button("🚀 Enter Dashboard"):
            if email and "@" in email:
                try:
                    # Check if user exists in Supabase
                    user_query = supabase.table("users").select("*").eq("email", email).execute()
                    
                    if not user_query.data:
                        # Register new user if not found
                        supabase.table("users").insert({"email": email, "coins": 0}).execute()
                    
                    st.session_state.user_email = email
                    st.session_state.page = "dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Database Error: {e}")
                    st.info("Make sure you disabled RLS or added a policy in Supabase.")
            else:
                st.warning("Please enter a valid Gmail address.")

# --- 7. MAIN DASHBOARD ---
elif st.session_state.page == "dashboard":
    # Sidebar Info
    st.sidebar.title("💎 Queen Menu")
    
    # Real-time Coin Fetching
    try:
        user_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = user_res.data[0]['coins'] if user_res.data else 0
        st.sidebar.metric("Your Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Failed")

    st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
    
    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.user_email = ""
        st.rerun()

    # --- CONTENT ROUTING ---
    if menu == "🔥 Guild Glory Pusher":
        # Fixed: Using utf-8 encoding to prevent 'charmap' errors with emojis
        try:
            with open("glory_push.py", "r", encoding="utf-8") as f:
                code = f.read()
                exec(code)
        except FileNotFoundError:
            st.error("❌ glory_push.py not found in your folder.")
        except Exception as e:
            st.error(f"❌ Script Error: {e}")

    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        st.write("Watch ads or complete tasks to earn coins for glory pushing.")
        # You can place the contents of earn.py here or exec() it
        st.warning("Earning module is being updated with the ad-network.")

    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Glory Pushers")
        try:
            leaders = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            if leaders.data:
                for idx, person in enumerate(leaders.data):
                    st.write(f"**{idx+1}. {person['email']}** — {person['coins']} Coins")
            else:
                st.write("No data available yet.")
        except:
            st.write("Leaderboard syncing...")