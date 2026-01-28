from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import os
import sys

# ========== EDIT THESE ==========
API_ID = 31096846                   # <-- your api_id (NUMBER)
API_HASH = "b1f3f282dc47585fd5c62eeaed59f142"        # <-- your api_hash (STRING)
CHANNEL = "https://t.me/myreelsource"  # <-- your Telegram channel
# ================================

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ERROR: TG_BOT_TOKEN is NOT set in GitHub Secrets")
    sys.exit(1)

STATE_FILE = "state.txt"
OUTPUT_FILE = "video.mp4"

def read_state():
    if not os.path.exists(STATE_FILE):
        return 0
    with open(STATE_FILE, "r") as f:
        return int(f.read().strip())

def write_state(value):
    with open(STATE_FILE, "w") as f:
        f.write(str(value))

async def download_next_video():
    index = read_state()
    print("Current index:", index)

    client = TelegramClient("bot_session", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    history = await client(GetHistoryRequest(
        peer=CHANNEL,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    videos = [msg for msg in history.messages if msg.video]
    videos.reverse()  # oldest → newest

    if index >= len(videos):
        print("No new videos available.")
        await client.disconnect()
        return

    message = videos[index]
    await message.download_media(file=OUTPUT_FILE)

    print(f"Downloaded video index: {index}")
    write_state(index + 1)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(download_next_video())
