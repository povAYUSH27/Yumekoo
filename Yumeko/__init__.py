import uvloop
import time
import pytz
import logging
from datetime import datetime
from cachetools import TTLCache
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pyrogram import Client
from telethon import TelegramClient
from telegram.ext import ApplicationBuilder

from config import config  # <-- Apna config import kar

# Install uvloop (faster event loop)
uvloop.install()

# Time setup
start_time = time.time()
ist = pytz.timezone("Asia/Kolkata")
start_time_str = datetime.now(ist).strftime("%d-%b-%Y %I:%M:%S %p")

# Scheduler
scheduler = AsyncIOScheduler()

# Clear old logs
open("log.txt", "w").close()

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - Yumeko - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

# Reduce noise logs
for noisy_logger in ("httpx", "pyrogram", "telethon", "telegram"):
    logging.getLogger(noisy_logger).setLevel(logging.ERROR)

log = logging.getLogger(name)

# Pyrogram Client
class App(Client):
    def init(self):
        super().init(
            name=config.BOT_NAME,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            workers=config.WORKERS,
            max_concurrent_transmissions=config.MAX_CONCURRENT_TRANSMISSIONS,
        )

app = App()

# Python-Telegram-Bot Client (PTB v20+)
ptb = ApplicationBuilder().token(config.BOT_TOKEN).build()

# Telethon Client
telebot = TelegramClient(
    f"{config.BOT_NAME}_telethon",
    config.API_ID,
    config.API_HASH,
    timeout=30,
    connection_retries=5,
)

# Caches
admin_cache = TTLCache(maxsize=1_000_000, ttl=300)
admin_cache_ptb = TTLCache(maxsize=100_000, ttl=300)
admin_cache_reload = {}

# Backup file
BACKUP_FILE_JSON = "last_backup.json"

# Handler Groups
WATCHER_GROUP = 17
COMMON_CHAT_WATCHER_GROUP = 100
GLOBAL_ACTION_WATCHER_GROUP = 1
LOCK_GROUP = 2
ANTI_FLOOD_GROUP = 3
BLACKLIST_GROUP = 4
IMPOSTER_GROUP = 5
FILTERS_GROUP = 6
CHATBOT_GROUP = 7
ANTICHANNEL_GROUP = 8
AFK_RETURN_GROUP = 9
AFK_REPLY_GROUP = 10
LOG_GROUP = 11
CHAT_MEMBER_LOG_GROUP = 12
SERVICE_CLEANER_GROUP = 13
KARMA_NEGATIVE_GROUP = 14
KARMA_POSITIVE_GROUP = 15
JOIN_UPDATE_GROUP = 16
