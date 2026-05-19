import discord
from discord.ext import commands
from discord import app_commands

import os
import json

from datetime import datetime

from services.session_service import (
    load_sessions,
    save_sessions
)

from cogs.dnd.personajes import load_data, save_data


SESSION_DB = "data/sesiones.json"




class SessionsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # REGISTRAR SESIÓN
    # =========================

    @app_commands.command(
        name="registrar_sesion",
        description="Registrar resumen mecánico de una sesión"
    )

    @app_commands.describe(
        participantes="Jugadores participantes (@usuario @usuario)",
        dm="Dungeon Master de la sesión",
        downtime="Horas de downtime usadas (máx 8)",
        dias_viaje="Días recorridos (máx 2)",
        ubicacion_final="Ubicación final del grupo",
        xp="XP ganada",
        blines="Blines ganados",
        resumen="Resumen mecánico corto"
    )

    async def registrar_sesion(
        self,
        interaction: discord.Interaction,
        participantes: str,
        dm: discord.Member,
        downtime: int,
        dias_viaje: int,
        ubicacion_final: str,
        xp: int,
        blines: int,
        resumen: str
    ):

        if downtime > 8:
            await interaction.response.send_message(
                "❌ El downtime máximo es 8 horas.",
                ephemeral=True
            )
            return

        if dias_viaje > 2:
            await interaction.response.send_message(
                "❌ El máximo de viaje es 2 días.",
                ephemeral=True
            )
            return

        data = self.load_sessions()

        if data:
            sesion_id = data[-1]["id"] + 1
        else:
            sesion_id = 1

        sesion = {
            "id": sesion_id,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "registrado_por": interaction.user.name,
            "participantes": participantes,
            "dm": dm.id,
            "downtime": downtime,
            "dias_viaje": dias_viaje,
            "ubicacion_final": ubicacion_final,
            "xp": xp,
            "blines": blines,
            "resumen": resumen
        }

        data.append(sesion)

        self.save_sessions(data)

        embed = discord.Embed(
            title=f"📜 Registro de Sesión #{sesion_id}",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🎲 Dungeon Master",
            value=dm.mention,
            inline=False
        )

        embed.add_field(
            name="👥 Participantes",
            value=participantes,
            inline=False
        )

        embed.add_field(
            name="⏳ DownTime",
            value=f"{downtime}/8 horas",
            inline=True
        )

        embed.add_field(
            name="🗺️ Viaje",
            value=f"{dias_viaje}/2 días",
            inline=True
        )

        embed.add_field(
            name="📍 Ubicación Final",
            value=ubicacion_final,
            inline=False
        )

        embed.add_field(
            name="✨ XP",
            value=f"+{xp}",
            inline=True
        )

        embed.add_field(
            name="💰 Blines",
            value=f"+{blines}",
            inline=True
        )

        embed.add_field(
            name="📖 Resumen",
            value=resumen,
            inline=False
        )

        embed.set_footer(
            text=f"Registrado por {interaction.user.name}"
        )

        await interaction.response.send_message(embed=embed)

    # =========================
    # VER SESIONES
    # =========================

    @app_commands.command(
        name="sesiones",
        description="Ver registros de sesiones"
    )

    async def sesiones(self, interaction: discord.Interaction):

        data = self.load_sessions()

        if not data:
            await interaction.response.send_message(
                "❌ No hay sesiones registradas.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📚 Historial de Sesiones",
            color=discord.Color.dark_purple()
        )

        texto = ""

        for sesion in reversed(data[-10:]):

            texto += (
                f"**#{sesion['id']}** • "
                f"{sesion['ubicacion_final']} • "
                f"+{sesion['xp']} XP • "
                f"+{sesion['blines']} Blines\n"
            )

        embed.description = texto

        await interaction.response.send_message(embed=embed)

    # =========================
    # VER SESIÓN
    # =========================

    @app_commands.command(
        name="ver_sesion",
        description="Ver detalles de una sesión"
    )

    @app_commands.describe(
        dm="Dungeon Master",
        id_sesion="Número de sesión"
    )

    async def ver_sesion(
        self,
        interaction: discord.Interaction,
        dm: discord.Member,
        id_sesion: int
    ):

        data = self.load_sessions()

        # Buscar sesión del DM
        sesion = next(
            (
                s for s in data
                if s["id"] == id_sesion
                and s["dm"] == dm.id
            ),
            None
        )

        if not sesion:

            await interaction.response.send_message(
                "❌ Sesión no encontrada para ese DM.",
                ephemeral=True
            )
            return

        # =========================
        # EMBED
        # =========================

        embed = discord.Embed(
            title=f"📜 Sesión #{sesion['id']}",
            description="Registro mecánico oficial",
            color=discord.Color.dark_gold()
        )

        # =========================
        # INFORMACIÓN GENERAL
        # =========================

        embed.add_field(
            name="🎲 Dungeon Master",
            value=dm.mention,
            inline=True
        )

        embed.add_field(
            name="📍 Ubicación Final",
            value=f"`{sesion['ubicacion_final']}`",
            inline=True
        )

        embed.add_field(
            name="📅 Fecha",
            value=f"`{sesion['fecha']}`",
            inline=True
        )

        # =========================
        # PARTICIPANTES
        # =========================

        embed.add_field(
            name="👥 Participantes",
            value=sesion["participantes"],
            inline=False
        )

        # =========================
        # RECURSOS
        # =========================

        embed.add_field(
            name="⏳ Downtime",
            value=f"`{sesion['downtime']} horas`",
            inline=True
        )

        embed.add_field(
            name="🗺️ Viaje",
            value=f"`{sesion['dias_viaje']} días`",
            inline=True
        )

        embed.add_field(
            name="✨ XP",
            value=f"`+{sesion['xp']} XP`",
            inline=True
        )

        # =========================
        # ECONOMÍA
        # =========================

        embed.add_field(
            name="💰 Blines",
            value=f"`+{sesion['blines']}`",
            inline=True
        )

        # =========================
        # RESUMEN
        # =========================

        embed.add_field(
            name="📖 Resumen",
            value=f"> {sesion['resumen']}",
            inline=False
        )

        # =========================
        # FOOTER
        # =========================

        embed.set_footer(
            text=f"Registrado por {sesion['registrado_por']}"
        )

        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed)
        
    # =========================
    # LOAD SESSIONS
    # =========================

    def load_sessions(self):

        if not os.path.exists(SESSION_DB):
            return []

        try:
            with open(SESSION_DB, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:
            return []

    # =========================
    # SAVE SESSIONS
    # =========================

    def save_sessions(self, data):

        with open(SESSION_DB, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # =========================
    # REGISTRAR PARTIDA
    # =========================

    @app_commands.command(
        name="registrar_partida",
        description="Registrar una nueva partida para un DM"
    )

    @app_commands.describe(
        dm="Dungeon Master",
        nombre="Nombre de la partida"
    )

    @app_commands.checks.has_role("Staff")

    async def registrar_partida(
        self,
        interaction: discord.Interaction,
        dm: discord.Member,
        nombre: str
    ):

        users_data = load_data()

        dm_id = str(dm.id)

        # Crear usuario si no existe
        if dm_id not in users_data:

            users_data[dm_id] = {}

        # Crear dm_data
        users_data[dm_id].setdefault("dm_data", {})

        # Crear partidas
        users_data[dm_id]["dm_data"].setdefault("partidas", {})

        partidas = users_data[dm_id]["dm_data"]["partidas"]

        # Crear ID de partida
        partida_id = len(partidas) + 1

        # Crear partida
        partidas[str(partida_id)] = {

            "nombre": nombre,
            "sesiones": []

        }

        save_data(users_data)

        embed = discord.Embed(
            title="🎲 Partida Registrada",
            color=discord.Color.dark_purple()
        )

        embed.add_field(
            name="🎲 DM",
            value=dm.mention,
            inline=False
        )

        embed.add_field(
            name="🆔 ID Partida",
            value=f"`{partida_id}`",
            inline=True
        )

        embed.add_field(
            name="📜 Nombre",
            value=nombre,
            inline=True
        )

        embed.set_footer(
            text="Sistema de Partidas"
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SessionsCog(bot))

# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(SessionsCog(bot))

    print("✅ SessionsCog cargado")