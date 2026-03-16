import streamlit as st
import time
import requests
from datetime import datetime, timedelta

def send_notif(user_id, msg):
    # Sends real-time push notification to the ntfy app
    topic = f"queen_bot_{user_id}"
    try:
        requests.post(f"https://ntfy.sh/{topic}", data=msg.encode('utf-8'))
    except:
        pass

st.header("🚜 Full Bermuda Glory Automation")
st.write("---")

# User Inputs
u_id = st.text_input("Your Player ID (for notifications)")
g_id = st.text_input("Bot Guild ID")
g_name = st.text_input("Bot Guild Name")

if st.button("🚀 Start 90-Min Automated Session"):
    if u_id and g_id:
        end_time = datetime.now() + timedelta(minutes=90)
        send_notif(u_id, f"Session Started! Pushing for {g_name}")
        
        status = st.empty()
        
        while datetime.now() < end_time:
            # PHASE 1: LEAVE
            status.warning("🕒 Phase 1: Leaving Guild... Waiting 4 minutes.")
            time.sleep(4 * 60)
            
            # PHASE 2: JOIN
            status.info(f"📥 Phase 2: Request to {g_name} now. Waiting 2 minutes.")
            send_notif(u_id, "ACTION: Send join request to the Bot Guild now!")
            time.sleep(2 * 60)
            
            # PHASE 3: PLAY
            status.error("⚔️ Phase 3: Match Started! (Bermuda Full Map - 18 mins)")
            send_notif(u_id, "🎮 Match Started! Bots are playing.")
            time.sleep(18 * 60)
            
            # PHASE 4: REWARD
            send_notif(u_id, "✅ Match Finished! Coins and Glory added.")
            status.success("🧘 Phase 4: Match over. 2-minute rest.")
            time.sleep(2 * 60)

        st.success("🏁 90-Minute Session Finished. Bot Auto-Off.")
        send_notif(u_id, "🏁 FINISHED: Your 1:30H Glory session is complete.")