import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. THE VERIFICATION INJECTOR (7Search + Monetag) ---
# This forces the meta tags into the top-level <head> for ad networks to see.
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

# --- 2. CONFIG & STYLING ---
st.set_page_config(page_title="Queen Arsenal Bot", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%);
        color: white; border: none; border-radius: 8px;
        height: 3em; width: 100%; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except:
        return None

supabase = init_connection()

if not supabase:
    st.error("⚠️ Supabase Secrets Missing! Please check your Streamlit Cloud settings.")
    st.stop()

# --- 4. APP NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "login"

# --- PAGE: LOGIN ---
if st.session_state.page == "login":
    st.title("👑 Queen Arsenal Bot")
    st.write("Enter your Gmail to access the Cloud Glory Pusher.")
    
    email = st.text_input("Gmail Address", placeholder="example@gmail.com")
    
    if st.button("🚀 Enter Dashboard"):
        if email and "@" in email:
            try:
                # FIXED UPSERT LOGIC: We specify 'email' as the conflict target
                supabase.table("users").upsert(
                    {"email": email, "last_login": "now()"},
                    on_conflict="email"
                ).execute()
                
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Database Error: {e}")
                st.info("💡 Tip: Run the SQL command in Supabase to enable 'Allow public access'.")
        else:
            st.warning("Please enter a valid Gmail.")

# --- PAGE: DASHBOARD ---
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Bot Menu")
    menu = st.sidebar.radio("Navigate", ["🔥 Glory Pusher", "💰 Earn Coins", "🏆 Leaderboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    if menu == "🔥 Glory Pusher":
        st.header("🔥 Cloud Glory Pusher")
        st.write(f"Logged in as: **{st.session_state.user_email}**")
        
        # AD SECTION
        st.markdown("---")
        st.subheader("📺 Unlock Bot (30s Ad)")
        components.html("""
            <div style='text-align:center;'>
                <script type="text/javascript">
                    atags = { "id": "7SWB1069B7EB7EA18FF" };
                </script>
                <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
            </div>
        """, height=200)
        
        guild_id = st.text_input("Target Guild ID", placeholder="1002938475")
        
        if st.button("🚀 Start Cloud Pushing"):
            if len(guild_id) > 6:
                try:
                    # Send task to the cloud queue
                    supabase.table("bot_queue").insert({
                        "guild_id": guild_id,
                        "user_email": st.session_state.user_email,
                        "status": "pending"
                    }).execute()
                    st.success("✅ Added to Queue! Bot will join your guild soon.")
                except Exception as e:
                    st.error(f"Queue Error: {e}")
            else:
                st.error("Invalid Guild ID.")

    elif menu == "💰 Earn Coins":
        st.header("🤑 Earn Free Coins")
        st.write("Watching ads helps us keep the cloud servers running 24/7.")
        # Place your Monetag Banner script here
        st.button("💰 Claim Daily Reward (+10 Coins)")
