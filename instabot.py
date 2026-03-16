import streamlit.components.v1 as components

components.html("""
<head>
<meta name="7searchppc" content="5b8d3e361b46def86de68b945a1f71cd"/>
</head>
""", height=0)

import streamlit as st
from supabase import create_client

# -------------------------
# 1. 7SearchPPC verification
# -------------------------
st.markdown(
"""
<script>
var meta=document.createElement("meta");
meta.name="7searchppc";
meta.content="194331a7fabe56c358637d4c992dbb62";
document.getElementsByTagName("head")[0].appendChild(meta);
</script>
""",
unsafe_allow_html=True
)

# -------------------------
# 2. Page configuration
# -------------------------
st.set_page_config(
    page_title="Queen Arsenal Hub",
    page_icon="👑",
    layout="wide"
)

# -------------------------
# 3. Custom UI style
# -------------------------
st.markdown("""
<style>
.main { background-color:#0e1117; color:white; }

.stButton>button{
    width:100%;
    border-radius:8px;
    height:3em;
    background:#ff4b4b;
    color:white;
    font-weight:bold;
    border:none;
}

.stButton>button:hover{
    background:#ff2e2e;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 4. Database connection
# -------------------------
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

except Exception:
    st.error("⚠️ Supabase secrets missing. Add SUPABASE_URL and SUPABASE_KEY.")
    st.stop()

# -------------------------
# 5. Session state
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "lobby"

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# -------------------------
# 6. Lobby page
# -------------------------
if st.session_state.page == "lobby":

    st.title("👑 Queen Bot Lobby")
    st.write("Welcome to the Free Fire Glory Pushing Hub")

    email = st.text_input("Enter Gmail Address")

    if st.button("Enter Dashboard"):

        if email and "@" in email:

            try:
                user = supabase.table("users").select("*").eq("email", email).execute()

                if not user.data:
                    supabase.table("users").insert(
                        {"email": email, "coins": 0}
                    ).execute()

                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()

            except Exception as e:
                st.error(f"Database Error: {e}")

        else:
            st.warning("Enter a valid Gmail address.")

# -------------------------
# 7. Dashboard
# -------------------------
elif st.session_state.page == "dashboard":

    st.sidebar.title("💎 Queen Menu")
    st.sidebar.write(f"Logged in as: {st.session_state.user_email}")

    try:
        res = supabase.table("users").select("coins").eq(
            "email", st.session_state.user_email
        ).execute()

        balance = res.data[0]["coins"] if res.data else 0
        st.sidebar.metric("Coins", balance)

    except:
        balance = 0
        st.sidebar.error("Coin Sync Failed")

    menu = st.sidebar.radio(
        "Navigation",
        ["Guild Glory Pusher", "Earn Coins", "Leaderboard"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.page = "lobby"
        st.session_state.user_email = ""
        st.rerun()

    # ---------------------
    # Glory Pusher
    # ---------------------
    if menu == "Guild Glory Pusher":

        st.header("🔥 Guild Glory Pusher")

        try:
            with open("glory_push.py", "r", encoding="utf-8") as f:
                exec(f.read())

        except FileNotFoundError:
            st.error("❌ glory_push.py file not found.")

        except Exception as e:
            st.error(f"❌ Script Error: {e}")

    # ---------------------
    # Earn Coins
    # ---------------------
    elif menu == "Earn Coins":

        st.header("🤑 Earn Coins")

        if st.button("Claim 10 Coins"):

            try:
                new_balance = balance + 10

                supabase.table("users").update(
                    {"coins": new_balance}
                ).eq("email", st.session_state.user_email).execute()

                st.success("10 Coins Added!")
                st.rerun()

            except Exception as e:
                st.error(e)

    # ---------------------
    # Leaderboard
    # ---------------------
    elif menu == "Leaderboard":

        st.header("🏆 Top Users")

        try:
            leaders = supabase.table("users").select(
                "email, coins"
            ).order("coins", desc=True).limit(5).execute()

            if leaders.data:

                for i, user in enumerate(leaders.data):
                    st.write(
                        f"{i+1}. {user['email']} — {user['coins']} Coins"
                    )

            else:
                st.write("No leaderboard data yet.")

        except:
            st.write("Loading leaderboard...")
```
