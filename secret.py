from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

print(TOKEN)

MATCHMAKING_CHANNEL_ID = int(
    os.getenv("MATCHMAKING_CHANNEL_ID")
)