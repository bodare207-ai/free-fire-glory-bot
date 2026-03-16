import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. 7SEARCH PPC VERIFICATION (MUST BE FIRST) ---
st.markdown('<head><meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/></head>', unsafe_allow_html=True)

# --- 2. PAGE STYLING ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #ff4b4b; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3333; border: 1px solid white; }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception:
    st.error("⚠️ Database Secrets Not Found!")
    st.info("Please add SUPABASE_URL and SUPABASE_KEY in Streamlit Cloud Settings > Secrets.")
    st.stop()

# --- 4. SESSION STATE MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'ad_watched' not in st.session_state: st.session_state.ad_watched = False
if 'ad_timer_start' not in st.session_state: st.session_state.ad_timer_start = None

# --- 5. AD UNIT COMPONENT ---
def show_7search_ad():
    """Displays the 7Search PPC Banner using your Ad ID."""
    ad_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #1a1a1a; padding: 20px; border-radius: 15px; border: 2px solid #333;">
        <p style="color: #ff4b4b; font-family: sans-serif; font-size: 14px; margin-bottom: 10px;"><b>Ads help keep this bot free!</b></p>
        <script type="text/javascript">
            atags = {{ "id": "7SWB1069B7EB7EA18FF" }};
        </script>
        <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
        <p style="color: #555; font-family: sans-serif; font-size: 10px; margin-top: 10px;">Verification ID: 5b8d3e361b46def86de68b945a1f71cd</p>
    </div>
    """
    components.html(ad_html, height=320)

# --- 6. NAVIGATION: LOBBY ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    st.markdown("### Login to Access the Glory Hub")
    
    with st.form("login_form"):
        email = st.text_input("Enter your Gmail Address", placeholder="e.g. viraj@gmail.com")
        submit = st.form_submit_button("🚀 Enter Dashboard")
        
        if submit:
            if email and "@" in email:
                try:
                    # Check/Register user in Supabase
                    user_check = supabase.table("users").select("*").eq("email", email).execute()
                    if not user_check.data:
                        supabase.table("users").insert({"email": email, "coins": 0}).execute()
                    
                    st.session_state.user_email = email
                    st.session_state.page = "dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Database Error: {e}")
            else:
                st.warning("Please enter a valid Gmail address.")

# --- 7. NAVIGATION: DASHBOARD ---
elif st.session_state.page == "dashboard":
    # Sidebar
    st.sidebar.title("💎 Queen Menu")
    st.sidebar.write(f"Logged in: **{st.session_state.user_email}**")
    
    # Live Balance
    try:
        user_res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        current_coins = user_res.data[0]['coins'] if user_res.data else 0
        st.sidebar.metric("Your Balance", f"{current_coins} Coins")
    except:
        st.sidebar.error("Sync Error")

    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.ad_watched = False
        st.session_state.ad_timer_start = None
        st.rerun()

    # --- CONTENT: GLORY PUSHER ---
    if menu == "🔥 Guild Glory Pusher":
        st.header("🔥 Guild Glory Pusher")
        
        if not st.session_state.ad_watched:
            show_7search_ad()
            
            # Timer Logic
            if st.session_state.ad_timer_start is None:
                st.session_state.ad_timer_start = time.time()
            
            elapsed = time.time() - st.session_state.ad_timer_start
            remaining = int(30 - elapsed)
            
            if remaining > 0:
                progress_val = min(1.0, elapsed / 30)
                st.progress(progress_val)
                st.warning(f"⏳ Verifying ad view... {remaining} seconds remaining.")
                time.sleep(1) # Re-run for smooth timer
                st.rerun()
            else:
                st.success("✅ Ad Verified! You can now start the bot.")
                if st.button("🚀 UNLOCK BOT NOW"):
                    st.session_state.ad_watched = True
                    st.rerun()
        else:
            # RUN THE PUSHER SCRIPT
            st.success("🔓 Access Granted. Bot is Active.")
            try:
                with open("glory_push.py", "r", encoding="utf-8") as f:
                    exec(f.read())
            except FileNotFoundError:
                st.error("Error: glory_push.py not found.")
            except Exception as e:
                st.error(f"Pusher Error: {e}")
            
            if st.button("🔄 Lock & Watch Ad Again"):
                st.session_state.ad_watched = False
                st.session_state.ad_timer_start = None
                st.rerun()

    # --- CONTENT: EARN COINS ---
    elif menu == "🤑 Earn Coins":
        st.header("🤑 Earn Coins")
        st.write("Watch the ad below to claim 10 Coins!")
        show_7search_ad()
        if st.button("💰 Claim 10 Coins"):
            try:
                new_balance = current_coins + 10
                supabase.table("users").update({"coins": new_balance}).eq("email", st.session_state.user_email).execute()
                st.success("Successfully added 10 coins!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Update failed: {e}")

    # --- CONTENT: LEADERBOARD ---
    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Glory Pushers")
        try:
            leaders = supabase.table("users").select("email, coins").order("coins", desc=True).limit(5).execute()
            for i, p in enumerate(leaders.data):
                st.write(f"{i+1}. **{p['email']}** — {p['coins']} Coins")
        except:
            st.write("Fetching top users...")
