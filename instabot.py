import streamlit as st
from supabase import create_client
import os

# --- 1. DEBUGGER (Only shows if there is an error) ---
def check_secrets():
    """Checks if secrets are loaded correctly."""
    try:
        test_url = st.secrets["SUPABASE_URL"]
        return True
    except Exception:
        return False

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

# Verification Meta Tag for 7Search PPC
st.markdown('<script>var meta=document.createElement("meta");meta.name="7searchppc";meta.content="194331a7fabe56c358637d4c992dbb62";document.getElementsByTagName("head")[0].appendChild(meta);</script>', unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
if not check_secrets():
    st.error("⚠️ Secrets Configuration Error!")
    st.write(f"I am looking for a file at: `{os.path.join(os.getcwd(), '.streamlit', 'secrets.toml')}`")
    st.info("💡 **Quick Fix:** Make sure your folder is named `.streamlit` and your file is `secrets.toml` (not `secrets.toml.txt`).")
    st.stop()

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- 4. STATE MANAGEMENT ---
if 'page' not in st.session_state: 
    st.session_state.page = "lobby"
if 'user_email' not in st.session_state: 
    st.session_state.user_email = ""

# --- 5. LOBBY INTERFACE ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        email = st.text_input("Enter Gmail", placeholder="yourname@gmail.com")
        if st.button("🚀 Enter Dashboard"):
            if email and "@" in email:
                try:
                    # Check/Create user in Supabase
                    user_query = supabase.table("users").select("*").eq("email", email).execute()
                    if not user_query.data:
                        supabase.table("users").insert({"email": email, "coins": 0}).execute()
                    
                    st.session_state.user_email = email
                    st.session_state.page = "dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Database Error: {e}")
                    st.info("Hint: Did you disable RLS in the Supabase Table Editor?")
            else:
                st.warning("Please enter a valid Gmail.")

# --- 6. DASHBOARD INTERFACE ---
elif st.session_state.page == "dashboard":
    # Sidebar
    st.sidebar.title("💎 Queen Menu")
    
    # Live Coin Count
    try:
        user_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = user_res.data[0]['coins'] if user_res.data else 0
        st.sidebar.metric("Your Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Failed")

    st.sidebar.write(f"Logged in: **{st.session_state.user_email}**")
    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.rerun()

    # --- ROUTING ---
    if menu == "🔥 Guild Glory Pusher":
        # Fixed: utf-8 encoding for emojis
        try:
            with open("glory_push.py", "r", encoding="utf-8") as f:
                exec(f.read())
        except FileNotFoundError:
            st.error("❌ `glory_push.py` not found in folder.")
        except Exception as e:
            st.error(f"❌ Script Error: {e}")

    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        st.write("Complete the tasks below to fuel your Glory Pushing.")
        # Place earn.py logic here or use:
        # with open("earn.py", "r", encoding="utf-8") as f: exec(f.read())
        st.info("Task list updating...")

    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Glory Pushers")
        try:
            leaders = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            for i, p in enumerate(leaders.data):
                st.write(f"{i+1}. **{p['email']}** — {p['coins']} Coins")
        except:
            st.write("Syncing leaderboard...")
