import discord
from discord.ext import commands


class DnDBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        print("🔄 Cargando Cogs...")

        await self.load_extension("cogs.dnd.personajes")
        await self.load_extension("cogs.dnd.sessions")
        await self.load_extension("cogs.dnd.embed_builder")
        await self.load_extension("cogs.dnd.matchmaking")

        print("✅ Cogs cargados")

    async def on_ready(self):
        
        print("ON_READY FUNCIONA")

        print(f"✅ Conectado como {self.user}")

        synced = await self.tree.sync()

        print(f"🌍 Slash Commands sincronizados: {len(synced)}")
