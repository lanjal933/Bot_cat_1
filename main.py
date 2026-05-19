import asyncio

import secret

from bot import DnDBot

from services.database import initialize_database
from services.matchmaking_db import init_matchmaking_db


print("MAIN INICIADO")


async def main():

    # =========================
    # DATABASES
    # =========================

    initialize_database()

    init_matchmaking_db()

    print("✅ Bases de datos iniciadas")

    # =========================
    # BOT
    # =========================

    bot = DnDBot()

    await bot.start(secret.TOKEN)


if __name__ == "__main__":

    asyncio.run(main())
