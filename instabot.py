import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# --- 1. AD NETWORK VERIFICATION INJECTOR ---
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

# --- 2. CONFIG & UI ---
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%);
        color: white; border: none; border-radius: 8px;
        height: 3.5em; width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
@st.cache_resource
def init_supabase():
    try:
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except:
        return None

supabase = init_supabase()

if not supabase:
    st.error("⚠️ Database configuration missing in Secrets!")
    st.stop()

# --- 4. APP LOGIC ---
if 'page' not in st.session_state: st.session_state.page = "login"

# LOGIN PAGE
if st.session_state.page == "login":
    st.title("👑 Queen Arsenal Bot")
    st.write("Enter your Gmail to start the Cloud Glory Pusher.")
    
    email = st.text_input("Gmail Address", placeholder="example@gmail.com")
    
    if st.button("🚀 Access Dashboard"):
        if "@" in email:
            try:
                # Upsert user record
                supabase.table("users").upsert(
                    {"email": email}, 
                    on_conflict="email"
                ).execute()
                
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("Please enter a valid email.")

# DASHBOARD PAGE
elif st.session_state.page == "dashboard":
    st.sidebar.title("💎 Bot Control")
    st.sidebar.write(f"User: {st.session_state.user_email}")
    
    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    st.header("🔥 Cloud Glory Pushing")
    
    # 7Search Ad Banner
    components.html("""
        <div style='text-align:center;'>
            <script type="text/javascript">
                atags = { "id": "7SWB1069B7EB7EA18FF" };
            </script>
            <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
        </div>
    """, height=220)

    guild_id = st.text_input("Target Guild ID", placeholder="Enter Free Fire Guild ID...")

    if st.button("🚀 Start Cloud Automation"):
        if len(guild_id) > 6:
            try:
                supabase.table("bot_queue").insert({
                    "guild_id": guild_id,
                    "user_email": st.session_state.user_email,
                    "status": "pending"
                }).execute()
                st.success("✅ Added to Cloud Queue! Our bots will start soon.")
            except Exception as e:
                st.error(f"Queue Error: {e}")
        else:
            st.error("Invalid Guild ID.")
