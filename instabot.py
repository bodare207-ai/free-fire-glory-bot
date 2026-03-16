import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. SITE VERIFICATION & STYLING ---
# Injects the meta tag at the top so 7Search can verify your site
st.markdown('<head><meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/></head>', unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE REAL AD ENGINE ---
def show_7search_ad():
    """Loads your specific 7Search PPC Banner into the app."""
    st.markdown("### 📺 Watch Ad to Unlock Bot")
    st.info("The Glory Pusher will unlock automatically after the timer ends.")
    
    # This is the iframe-safe container for your 7Search Ad
    ad_html = f"""
    <div style="display: flex; justify-content: center; background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333;">
        <script type="text/javascript">
            atags = {{ "id": "7SWB1069B7EB7EA18FF" }};
        </script>
        <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
        <p style="color: #555; font-family: sans-serif; font-size: 12px;">Ad Powered by 7Search PPC</p>
    </div>
    """
    components.html(ad_html, height=300)

# --- 3. CORE LOGIC & DATABASE ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

# Check for Supabase secrets
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except:
    st.error("⚠️ Secrets Missing! Add SUPABASE_URL and SUPABASE_KEY to your Streamlit Cloud Settings.")
    st.stop()

# Initialize Session States
if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'ad_timer_start' not in st.session_state: st.session_state.ad_timer_start = None
if 'ad_watched' not in st.session_state: st.session_state.ad_watched = False
if 'user_email' not in st.session_state: st.session_state.user_email = ""

# --- 4. NAVIGATION: LOBBY ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    st.write("Welcome to the most powerful Free Fire Glory Hub.")
    
    email = st.text_input("Enter Gmail Address", placeholder="example@gmail.com")
    if st.button("🚀 Enter Dashboard"):
        if email and "@" in email:
            try:
                # Sync with Supabase
                res = supabase.table("users").select("*").eq("email", email).execute()
                if not res.data:
                    supabase.table("users").insert({"email": email, "coins": 0}).execute()
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"Database Error: {e}")
        else:
            st.warning("Please enter a valid Gmail address.")

# --- 5. NAVIGATION: DASHBOARD ---
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Queen Menu")
    
    # Real-time Coin Tracker
    try:
        user_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = user_res.data[0]['coins'] if user_res.data else 0
        st.sidebar.metric("Your Balance", f"{balance} Coins")
    except:
        st.sidebar.error("Coin Sync Failed")

    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.ad_watched = False # Reset ad on logout
        st.rerun()

    # --- TAB: GLORY PUSHER (With Ad-Lock) ---
    if menu == "🔥 Guild Glory Pusher":
        st.header("🔥 Guild Glory Pusher")
        
        if not st.session_state.ad_watched:
            # Show the real 7Search Ad
            show_7search_ad()
            
            # Start the 30-second security timer
            if st.session_state.ad_timer_start is None:
                st.session_state.ad_timer_start = time.time()
            
            elapsed = time.time() - st.session_state.ad_timer_start
            remaining = int(max(0, 30 - elapsed))

            if remaining > 0:
                st.button(f"⏳ Verifying Ad View... ({remaining}s)", disabled=True)
                time.sleep(1) # Refresh for the timer effect
                st.rerun()
            else:
                if st.button("✅ Ad Watched! Unlock Bot"):
                    st.session_state.ad_watched = True
                    st.rerun()
        else:
            # BOT IS UNLOCKED HERE
            st.success(f"Welcome, {st.session_state.user_email}! Bot is Active.")
            try:
                with open("glory_push.py", "r", encoding="utf-8") as f:
                    exec(f.read())
            except Exception as e:
                st.error(f"Script Error: {e}")
            
            if st.button("🔒 Refresh Ad (Lock Bot)"):
                st.session_state.ad_watched = False
                st.session_state.ad_timer_start = None
                st.rerun()

    # --- TAB: EARN COINS ---
    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        st.write("Watch ads below to add coins to your account!")
        show_7search_ad()
        if st.button("Claim 10 Coins"):
            # Update database logic
            new_balance = balance + 10
            supabase.table("users").update({"coins": new_balance}).eq("email", st.session_state.user_email).execute()
            st.success("10 Coins Added! Refreshing balance...")
            time.sleep(1)
            st.rerun()

    # --- TAB: LEADERBOARD ---
    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Glory Pushers")
        try:
            leaders = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            for i, p in enumerate(leaders.data):
                st.write(f"{i+1}. **{p['email']}** — {p['coins']} Coins")
        except:
            st.write("Fetching leaderboard data...")
