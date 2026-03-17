import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time
import os

# --- 1. AD NETWORK "ROOT BRIDGE" & VERIFICATION ---
# This part makes your Monetag file visible even on Streamlit.
def handle_ad_verification():
    # REPLACE this with your actual filename from Monetag
    v_file = "monetag_39e4b7e52020ed41676ee541cdfd2fb2.html" 
    
    # Check if the network is visiting your site to verify
    if st.query_params.get("verify") == "true":
        filepath = os.path.join("static", v_file)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                st.write(f.read(), unsafe_allow_html=True)
                st.stop()

handle_ad_verification()

# --- 2. META TAG INJECTION (FOR HEADERS) ---
components.html(
    """
    <script>
    const head = window.parent.document.getElementsByTagName('head')[0];
    const tags = [
        {name: "7searchppc", content: "5b8d3e361b46def86de68b945a1f71cd"},
        {name: "monetag", content: "39e4b7e52020ed41676ee541cdfd2fb2"}
    ];
    tags.forEach(t => {
        if (!window.parent.document.querySelector(`meta[name="${t.name}"]`)) {
            const m = window.parent.document.createElement('meta');
            m.name = t.name; m.content = t.content;
            head.appendChild(m);
        }
    });
    </script>
    """,
    height=0,
)

# --- 3. PAGE UI & STYLING ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%);
        color: white; border: none; border-radius: 8px;
        height: 3.5em; width: 100%; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATABASE CONNECTION ---
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except:
        return None

supabase = init_supabase()

if not supabase:
    st.error("⚠️ Database Configuration Missing! Add SUPABASE_URL and KEY to Secrets.")
    st.stop()

# --- 5. APP NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "login"

# PAGE: LOGIN
if st.session_state.page == "login":
    st.title("👑 Queen Arsenal Bot")
    st.write("Enter your Gmail to access the Cloud Glory Pusher.")
    
    email = st.text_input("Gmail Address", placeholder="example@gmail.com")
    
    if st.button("🚀 Access Dashboard"):
        if email and "@" in email:
            try:
                # Upsert user into Supabase
                supabase.table("users").upsert({"email": email}, on_conflict="email").execute()
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Database Error: {e}")
        else:
            st.warning("Please enter a valid Gmail.")

# PAGE: DASHBOARD
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Bot Menu")
    menu = st.sidebar.radio("Navigate", ["🔥 Glory Pusher", "💰 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    if menu == "🔥 Glory Pusher":
        st.header("🔥 Cloud Glory Pusher")
        st.write(f"Logged in as: **{st.session_state.user_email}**")
        
        # 7Search PPC Ad Unit
        components.html("""
            <div style='text-align:center;'>
                <script type="text/javascript">
                    atags = { "id": "7SWB1069B7EB7EA18FF" };
                </script>
                <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
            </div>
        """, height=220)

        guild_id = st.text_input("Target Guild ID", placeholder="1002938475")
        
        if st.button("🚀 Start Cloud Automation"):
            if len(guild_id) > 6:
                try:
                    # Insert job into queue
                    supabase.table("bot_queue").insert({
                        "guild_id": guild_id,
                        "user_email": st.session_state.user_email,
                        "status": "pending"
                    }).execute()
                    st.success("✅ Added to Cloud Queue! Bots will join your guild soon.")
                except Exception as e:
                    st.error(f"Queue Error: {e}")
            else:
                st.error("Invalid Guild ID.")

    elif menu == "💰 Earn Coins":
        st.header("🤑 Earn Free Coins")
        st.write("Watching ads keeps the bot servers free for everyone!")
        # Monetag Banner or MultiTag can be placed here
        st.button("Claim Daily Reward (+10 Coins)")
