from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import os

# ===== CONFIG =====
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
channel = "https://t.me/myreelsource"   # <-- YOUR CHANNEL
# ==================

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

    async with TelegramClient("bot_session", api_id=0, api_hash="", bot_token=BOT_TOKEN) as client:
        history = await client(GetHistoryRequest(
            peer=channel,
            limit=100,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        videos = [msg for msg in history.messages if msg.video]
        videos = list(reversed(videos))  # oldest → newest

        if index >= len(videos):
            print("No new videos available.")
            return

        message = videos[index]
        await message.download_media(file=OUTPUT_FILE)

        print(f"Downloaded video number: {index}")
        write_state(index + 1)

if __name__ == "__main__":
    asyncio.run(download_next_video())
