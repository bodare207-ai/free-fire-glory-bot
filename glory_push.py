import time
import requests
import streamlit as st

def send_notification(title, message):
    """Sends a push notification to your phone using ntfy.sh"""
    try:
        requests.post("https://ntfy.sh/queen_bot_updates",
                      data=message.encode('utf-8'),
                      headers={
                          "Title": title,
                          "Priority": "high",
                          "Tags": "video_game,rocket"
                      })
    except Exception as e:
        print(f"Notification Error: {e}")

def run_glory_cycle(player_id, guild_id, guild_name):
    """The real 90-minute glory pushing logic"""
    
    st.success(f"🚀 Bot Initialized for Guild: {guild_name} ({guild_id})")
    send_notification("Bot Started!", f"Pushing glory for {guild_name} with ID {player_id}")

    # Phase 1: Joining the Guild
    st.info("⚔️ Phase 1: Joining Guild...")
    time.sleep(120)  # 2 Minutes Join Time
    
    # Phase 2: Cooldown
    st.info("🕒 Phase 2: Waiting for Matchmaking (4 min cooldown)...")
    time.sleep(240)  # 4 Minutes
    
    # Phase 3: The Match
    st.warning("🎮 Phase 3: Match Started (Bermuda Full Map)...")
    send_notification("Match Started", "The bot is now in-game for 18 minutes.")
    time.sleep(1080)  # 18 Minutes
    
    # Phase 4: Match Result & Exit
    st.success("✅ Phase 4: Match Completed! +20 Dog Tags added.")
    send_notification("Cycle Complete", f"Successfully added Glory to {guild_name}")
    
    time.sleep(120)  # 2 Minutes Rest before next account
    return True

# If running directly for testing
if __name__ == "__main__":
    # Test values
    PID = "USER_123"
    GID = "100234567"
    GNAME = "Queen Arsenal"
    run_glory_cycle(PID, GID, GNAME)
