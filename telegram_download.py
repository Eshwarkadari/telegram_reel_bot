from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import os

# ===== EDIT THESE =====
API_ID = 31096846# your api_id
API_HASH = "b1f3f282dc47585fd5c62eeaed59f142"        # your api_hash
CHANNEL = "https://t.me/myreelsource"
# =====================

SESSION = os.getenv("TG_STRING_SESSION")

if not SESSION:
    raise RuntimeError("TG_STRING_SESSION is NOT set")

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

    async with TelegramClient(
        StringSession(SESSION),
        API_ID,
        API_HASH
    ) as client:

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

        videos = [m for m in history.messages if m.video]
        videos.reverse()  # oldest → newest

        if index >= len(videos):
            print("No new videos.")
            return

        msg = videos[index]
        await msg.download_media(file=OUTPUT_FILE)

        print(f"Downloaded video index: {index}")
        write_state(index + 1)

if __name__ == "__main__":
    asyncio.run(download_next_video())
