import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. VERIFICATION ---
st.markdown('<head><meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/></head>', unsafe_allow_html=True)

# --- 2. THE REAL AD SYSTEM ---
def show_7search_ad():
    st.subheader("📺 Watch this Ad to Unlock the Bot")
    
    # This is the real 7Search Script using your ID
    # Note: If 7Search gave you a different script, paste it here inside the triple quotes
    ad_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; background: #1a1a1a; padding: 20px; border-radius: 10px;">
        <script type="text/javascript">
            var ad_id = "7SWB1069B7EB7EA18FF";
            var ad_type = "banner";
        </script>
        <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
        <p style="color: #666; font-family: sans-serif;">(Real 7Search Ad Loading...)</p>
    </div>
    """
    components.html(ad_html, height=300)

# --- 3. DATABASE & CONFIG ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'ad_timer_start' not in st.session_state: st.session_state.ad_timer_start = None
if 'ad_watched' not in st.session_state: st.session_state.ad_watched = False

# --- 4. LOBBY ---
if st.session_state.page == "lobby":
    st.title("👑 Queen Bot Lobby")
    email = st.text_input("Gmail Address", placeholder="Enter your email to login")
    if st.button("🚀 Enter Dashboard"):
        if email and "@" in email:
            st.session_state.user_email = email
            st.session_state.page = "dashboard"
            st.rerun()

# --- 5. DASHBOARD ---
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Queen Menu")
    menu = st.sidebar.radio("Navigate", ["🔥 Guild Glory Pusher", "🤑 Earn Coins"])

    if menu == "🔥 Guild Glory Pusher":
        st.header("🔥 Guild Glory Pusher")

        if not st.session_state.ad_watched:
            show_7search_ad()
            
            # Start the timer when they first see the ad page
            if st.session_state.ad_timer_start is None:
                st.session_state.ad_timer_start = time.time()
            
            elapsed = time.time() - st.session_state.ad_timer_start
            remaining = int(max(0, 30 - elapsed))

            if remaining > 0:
                st.button(f"⏳ Please wait {remaining}s to verify ad view...", disabled=True)
                time.sleep(1) # Refresh the loop every second
                st.rerun()
            else:
                if st.button("✅ Ad Verified! Start Bot Now"):
                    st.session_state.ad_watched = True
                    st.rerun()
        else:
            # THE BOT RUNS HERE
            st.success("Access Granted! Bot is Active.")
            try:
                with open("glory_push.py", "r", encoding="utf-8") as f:
                    exec(f.read())
            except Exception as e:
                st.error(f"Script Error: {e}")
            
            if st.button("🔒 Lock Bot & Watch Ad Again"):
                st.session_state.ad_watched = False
                st.session_state.ad_timer_start = None
                st.rerun()

    elif menu == "🤑 Earn Coins":
        st.header("🤑 Watch Ads for Extra Coins")
        show_7search_ad()
        if st.button("Claim 5 Coins"):
            st.success("Coins added! (Ensure you stay on the page for the ad to count)")
