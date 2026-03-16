import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. 7SEARCH PPC VERIFICATION (CRITICAL: MUST BE AT THE TOP) ---
# This ensures the crawler sees the tag as soon as the page loads.
components.html(
    """
    <html>
        <head>
            <meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/>
        </head>
        <body></body>
    </html>
    """,
    height=0,
)
st.markdown('<head><meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/></head>', unsafe_allow_html=True)

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

# Custom CSS for a professional Gaming UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%); 
        color: white; 
        font-weight: bold; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception:
    st.error("⚠️ Database Secrets Error!")
    st.info("Go to Streamlit Cloud Settings > Secrets and add SUPABASE_URL and SUPABASE_KEY.")
    st.stop()

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'ad_watched' not in st.session_state: st.session_state.ad_watched = False
if 'ad_timer_start' not in st.session_state: st.session_state.ad_timer_start = None

# --- 5. AD COMPONENT ---
def show_7search_ad():
    """Displays your 7Search Banner Ad."""
    st.markdown("### 📺 Supporting Ad")
    st.caption("Verification Code: 5b8d3e361b46def86de68b945a1f71cd")
    
    ad_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333;">
        <script type="text/javascript">
            atags = {{ "id": "7SWB1069B7EB7EA18FF" }};
        </script>
        <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
        <p style="color: #444; font-family: sans-serif; font-size: 10px; margin-top: 10px;">Ad Unit ID: 7SWB1069B7EB7EA18FF</p>
    </div>
    """
    components.html(ad_html, height=300)

# --- 6. NAVIGATION: LOBBY ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    st.subheader("Login to start pushing Glory")
    
    with st.container():
        email = st.text_input("Gmail Address", placeholder="yourname@gmail.com")
        if st.button("🚀 Enter Dashboard"):
            if email and "@" in email:
                try:
                    # Sync with Supabase
                    user_data = supabase.table("users").select("*").eq("email", email).execute()
                    if not user_data.data:
                        supabase.table("users").insert({"email": email, "coins": 0}).execute()
                    st.session_state.user_email = email
                    st.session_state.page = "dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Sync Error: {e}")
            else:
                st.warning("Please enter a valid Gmail.")

# --- 7. NAVIGATION: DASHBOARD ---
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Queen Menu")
    st.sidebar.write(f"Logged as: **{st.session_state.user_email}**")
    
    # Coin Tracker
    try:
        res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = res.data[0]['coins'] if res.data else 0
        st.sidebar.metric("Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Offline")

    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.ad_watched = False
        st.session_state.ad_timer_start = None
        st.rerun()

    # --- TAB: GLORY PUSHER ---
    if menu == "🔥 Guild Glory Pusher":
        st.header("🔥 Guild Glory Pusher")
        
        if not st.session_state.ad_watched:
            show_7search_ad()
            
            if st.session_state.ad_timer_start is None:
                st.session_state.ad_timer_start = time.time()
            
            elapsed = time.time() - st.session_state.ad_timer_start
            remaining = int(30 - elapsed)
            
            if remaining > 0:
                st.progress(min(1.0, elapsed / 30))
                st.warning(f"⏳ Verifying ad view... Please wait {remaining} seconds.")
                time.sleep(1)
                st.rerun()
            else:
                st.success("✅ Ad Verified!")
                if st.button("🚀 UNLOCK BOT"):
                    st.session_state.ad_watched = True
                    st.rerun()
        else:
            st.success("🔓 Bot Active")
            try:
                # Running the external script
                with open("glory_push.py", "r", encoding="utf-8") as f:
                    exec(f.read())
            except Exception as e:
                st.error(f"File Error: {e}")
            
            if st.button("🔒 Lock Bot"):
                st.session_state.ad_watched = False
                st.session_state.ad_timer_start = None
                st.rerun()

    # --- TAB: EARN COINS ---
    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        show_7search_ad()
        if st.button("💰 Claim 10 Coins"):
            try:
                new_bal = balance + 10
                supabase.table("users").update({"coins": new_bal}).eq("email", st.session_state.user_email).execute()
                st.success("10 Coins Added!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- TAB: LEADERBOARD ---
    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Pushers")
        try:
            data = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            for i, p in enumerate(data.data):
                st.write(f"{i+1}. **{p['email']}** — {p['coins']} Coins")
        except:
            st.write("Loading leaderboard...")
