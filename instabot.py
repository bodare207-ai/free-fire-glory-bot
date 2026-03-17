import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. AD NETWORK VERIFICATION (7SEARCH + MONETAG) ---
# This invisible block puts both your meta tags in the HTML for crawlers to find.
components.html(
    """
    <head>
        <meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/>
        <meta name="monetag" content="39e4b7e52020ed41676ee541cdfd2fb2">
    </head>
    """,
    height=0,
)

# Backup injection (forces tags into the main container)
st.markdown(
    '<head>'
    '<meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/>'
    '<meta name="monetag" content="39e4b7e52020ed41676ee541cdfd2fb2">'
    '</head>', 
    unsafe_allow_html=True
)

# --- 2. PAGE CONFIG & UI ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%); 
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 15px #ff416c; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
try:
    # Get your secrets from Streamlit Cloud Settings
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception:
    st.error("⚠️ Database Setup Required!")
    st.info("Please add SUPABASE_URL and SUPABASE_KEY to your Streamlit Secrets.")
    st.stop()

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'ad_watched' not in st.session_state: st.session_state.ad_watched = False
if 'ad_timer_start' not in st.session_state: st.session_state.ad_timer_start = None

# --- 5. AD UNIT COMPONENT ---
def show_monetag_ad():
    """Displays your ad unit and helps with verification."""
    st.markdown("### 📺 Supporting Ad")
    # This is the 7Search Banner code from your earlier request
    ad_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333;">
        <script type="text/javascript">
            atags = {{ "id": "7SWB1069B7EB7EA18FF" }};
        </script>
        <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
        <p style="color: #444; font-size: 10px; margin-top: 10px;">Network: 7Search & Monetag Verified</p>
    </div>
    """
    components.html(ad_html, height=320)

# --- 6. NAVIGATION: LOBBY ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    email = st.text_input("Enter Gmail Address", placeholder="yourname@gmail.com")
    if st.button("🚀 Enter Dashboard"):
        if email and "@" in email:
            try:
                # Sync user with Supabase
                user_res = supabase.table("users").select("*").eq("email", email).execute()
                if not user_res.data:
                    supabase.table("users").insert({"email": email, "coins": 0}).execute()
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"Sync Error: {e}")

# --- 7. NAVIGATION: DASHBOARD ---
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Queen Menu")
    
    # Coin Balance Meter
    try:
        bal_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = bal_res.data[0]['coins'] if bal_res.data else 0
        st.sidebar.metric("Your Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Offline")

    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.ad_watched = False
        st.rerun()

    # --- TAB: GLORY PUSHER ---
    if menu == "🔥 Guild Glory Pusher":
        st.header("🔥 Guild Glory Pusher")
        
        if not st.session_state.ad_watched:
            show_monetag_ad()
            
            # 30-Second Ad Timer
            if st.session_state.ad_timer_start is None:
                st.session_state.ad_timer_start = time.time()
            
            elapsed = time.time() - st.session_state.ad_timer_start
            remaining = int(30 - elapsed)
            
            if remaining > 0:
                st.progress(min(1.0, elapsed / 30))
                st.warning(f"⏳ Verifying ad view... {remaining}s remaining.")
                time.sleep(1)
                st.rerun()
            else:
                st.success("✅ Ad Verified! Bot is ready.")
                if st.button("🚀 UNLOCK NOW"):
                    st.session_state.ad_watched = True
                    st.rerun()
        else:
            # THIS IS WHERE YOUR CLOUD QUEUE LOGIC LIVES
            guild_id = st.text_input("Enter Guild ID", placeholder="e.g. 1002345678")
            if st.button("🚀 Start Cloud Bot"):
                if len(guild_id) > 5:
                    # Save the job to Supabase so your cloud server sees it
                    data = {"guild_id": guild_id, "status": "pending", "user": st.session_state.user_email}
                    supabase.table("bot_queue").insert(data).execute()
                    st.success(f"✅ Guild {guild_id} added to Cloud Queue! Bots will join soon.")
                else:
                    st.error("Invalid Guild ID.")

    # --- TAB: EARN COINS ---
    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Extra Coins")
        show_monetag_ad()
        if st.button("💰 Claim 10 Coins"):
            new_val = balance + 10
            supabase.table("users").update({"coins": new_val}).eq("email", st.session_state.user_email).execute()
            st.success("10 Coins added to your account!")
            time.sleep(1)
            st.rerun()

    # --- TAB: LEADERBOARD ---
    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Glory Pushers")
        try:
            top_users = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            for i, u in enumerate(top_users.data):
                st.write(f"{i+1}. **{u['email']}** — {u['coins']} Coins")
        except:
            st.write("Loading leaderboard...")
