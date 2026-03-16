```python
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import time

# -------------------------------
# 1. 7SearchPPC META VERIFICATION
# -------------------------------
components.html(
"""
<meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd">
""",
height=0,
)

# -------------------------------
# 2. PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Queen Arsenal Hub", page_icon="👑", layout="wide")

# -------------------------------
# 3. CUSTOM UI STYLE
# -------------------------------
st.markdown("""
<style>
.main { background-color: #0e1117; color: white; }

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3.5em;
    background: linear-gradient(90deg,#ff4b2b 0%,#ff416c 100%);
    color: white;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.02);
    border: 1px solid white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 4. DATABASE CONNECTION
# -------------------------------
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception:
    st.error("⚠️ Database Secrets Error!")
    st.stop()

# -------------------------------
# 5. SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "lobby"

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "ad_watched" not in st.session_state:
    st.session_state.ad_watched = False

if "ad_timer_start" not in st.session_state:
    st.session_state.ad_timer_start = None


# -------------------------------
# 6. SHOW 7SEARCH AD
# -------------------------------
def show_7search_ad():

    st.markdown("### 📺 Sponsored Ad")

    ad_html = """
    <div style="display:flex;justify-content:center;">
        <script type="text/javascript">
        atags = { "id": "7SWB1069B7EB7EA18FF" };
        </script>
        <script type="text/javascript" src="https://7searchppc.com/js/ad_script.js"></script>
    </div>
    """

    components.html(ad_html, height=250)


# -------------------------------
# 7. LOGIN LOBBY
# -------------------------------
if st.session_state.page == "lobby":

    st.title("👑 Queen Bot Lobby")
    st.subheader("Login to Start")

    email = st.text_input("Enter Gmail")

    if st.button("🚀 Enter Dashboard"):

        if email and "@" in email:

            try:
                user = supabase.table("users").select("*").eq("email", email).execute()

                if not user.data:
                    supabase.table("users").insert({"email": email, "coins": 0}).execute()

                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()

            except Exception as e:
                st.error(e)

        else:
            st.warning("Enter valid Gmail")


# -------------------------------
# 8. DASHBOARD
# -------------------------------
elif st.session_state.page == "dashboard":

    st.sidebar.title("💎 Menu")
    st.sidebar.write(st.session_state.user_email)

    try:
        res = supabase.table("users").select("coins").eq("email", st.session_state.user_email).execute()
        balance = res.data[0]["coins"]
        st.sidebar.metric("Coins", balance)
    except:
        balance = 0

    menu = st.sidebar.radio("Navigation", ["🔥 Glory Pusher","🤑 Earn Coins","🏆 Leaderboard"])

    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.ad_watched = False
        st.session_state.ad_timer_start = None
        st.rerun()

    # -------------------------------
    # GLORY PUSHER
    # -------------------------------
    if menu == "🔥 Glory Pusher":

        st.header("🔥 Guild Glory Pusher")

        if not st.session_state.ad_watched:

            show_7search_ad()

            if st.session_state.ad_timer_start is None:
                st.session_state.ad_timer_start = time.time()

            elapsed = time.time() - st.session_state.ad_timer_start
            remain = int(30 - elapsed)

            if remain > 0:
                st.progress(min(1.0, elapsed/30))
                st.warning(f"⏳ Watch ad {remain} seconds")
                time.sleep(1)
                st.rerun()

            else:

                if st.button("Unlock Bot"):
                    st.session_state.ad_watched = True
                    st.rerun()

        else:

            st.success("Bot Activated")

            try:
                with open("glory_push.py","r") as f:
                    exec(f.read())
            except Exception as e:
                st.error(e)

            if st.button("Lock Bot"):
                st.session_state.ad_watched = False
                st.session_state.ad_timer_start = None
                st.rerun()


    # -------------------------------
    # EARN COINS
    # -------------------------------
    elif menu == "🤑 Earn Coins":

        st.header("Earn Coins")

        show_7search_ad()

        if st.button("Claim 10 Coins"):

            try:
                new_balance = balance + 10

                supabase.table("users").update(
                    {"coins": new_balance}
                ).eq("email", st.session_state.user_email).execute()

                st.success("10 Coins Added")
                time.sleep(1)
                st.rerun()

            except Exception as e:
                st.error(e)


    # -------------------------------
    # LEADERBOARD
    # -------------------------------
    elif menu == "🏆 Leaderboard":

        st.header("Top Users")

        try:
            data = supabase.table("users").select("email,coins").order("coins",desc=True).limit(5).execute()

            for i,user in enumerate(data.data):
                st.write(f"{i+1}. {user['email']} - {user['coins']} Coins")

        except:
            st.write("Loading leaderboard...")
```
