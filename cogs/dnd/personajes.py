import discord
from discord.ext import commands
from discord import app_commands

import json
import os

DB_FILE = "data/users.json"


# =========================
# DATABASE
# =========================

def load_data():

    if not os.path.exists(DB_FILE):

        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

        return {}

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return {}


def save_data(data):

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# COG
# =========================

class PersonajesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # REGISTRAR PJ
    # =========================

    @app_commands.command(
        name="registrar_pj",
        description="Registrar un personaje"
    )

    @app_commands.checks.has_role("Staff")
    @app_commands.describe(
        usuario="Dueño del personaje",
        nick_pj="Nick único",
        nombre="Nombre del personaje",
        raza="Raza del personaje",
        clase="Clase",
        nivel="Nivel inicial",
        edad="Edad del personaje",
        estatura="Estatura",
        frase="Frase característica",
        link="Link de hoja, imagen o referencia"
    )

    async def registrar_pj(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member,
        nick_pj: str,
        nombre: str,
        clase: str,
        raza: str,
        nivel: int,
        edad: str,
        estatura: str,
        frase: str,
        link: str
    ):

        data = load_data()

        user_id = str(usuario.id)

        nick_pj = nick_pj.lower()

        # Crear usuario
        if user_id not in data:

            data[user_id] = {
                "personajes": {}
            }

        personajes = data[user_id]["personajes"]

        # Verificar duplicado
        if nick_pj in personajes:

            await interaction.response.send_message(
                "❌ Ese nick ya existe.",
                ephemeral=True
            )
            return

        # Crear personaje
        personajes[nick_pj] = {

            "nombre": nombre,
            "clase": clase,
            "raza": raza,
            "nivel": nivel,

            "xp": 0,
            "blines": 0,

            "edad": edad,
            "estatura": estatura,
            "frase": frase,
            "link": link,


            "inventario": []
        }

        save_data(data)

        embed = discord.Embed(
            title="✅ Personaje Registrado",
            color=discord.Color.green()
        )

        embed.add_field(name="👤 Dueño", value=usuario.mention)
        embed.add_field(name="🆔 Nick", value=nick_pj)
        embed.add_field(name="📜 Nombre", value=nombre)
        embed.add_field(name="⚔ Clase", value=clase)
        embed.add_field(name="⬆ Nivel", value=nivel)

        await interaction.response.send_message(embed=embed)

        # =========================
        # VER PJ
        # =========================

    @app_commands.command(
            name="ver_pj",
            description="Ver ficha técnica del personaje"
        )
    @app_commands.describe(
            usuario="Dueño del personaje",
            nick_pj="Nick del personaje"
        )
    async def ver_pj(
            self,
            interaction: discord.Interaction,
            usuario: discord.Member,
            nick_pj: str
        ):
            data = load_data()
            user_id = str(usuario.id)
            nick_pj = nick_pj.lower()

            # Verificar usuario
            if user_id not in data:
                await interaction.response.send_message(
                    "❌ **Error:** El usuario no tiene datos registrados.",
                    ephemeral=True
                )
                return

            personajes = data[user_id].get("personajes", {})

            # Verificar personaje
            if nick_pj not in personajes:
                await interaction.response.send_message(
                    "❌ **Error:** El personaje no existe.",
                    ephemeral=True
                )
                return

            pj = personajes[nick_pj]

            # EMBED MEJORADO: Ficha de Personaje Estilo RPG
            embed = discord.Embed(
                title=f"📜 {pj['nombre'].upper()}",
                description=f"Ficha oficial de personaje perteneciente a {usuario.mention}.",
                color=0x9b59b6  # Violeta Amatista Profundo
            )

            # Fila 1: Estadísticas principales (3 columnas)
            embed.add_field(name="⚔️ Clase", value=f"`{pj['clase']}`", inline=True)
            embed.add_field(name="🧬 Raza", value=f"`{pj['raza']}`", inline=True)
            embed.add_field(name="🆙 Nivel", value=f"`{pj['nivel']}`", inline=True)
            embed.add_field(name="✨ Experiencia", value=f"`{pj.get('xp', 0)} XP`", inline=True)

            # Fila 2: Datos Físicos y Economía (3 columnas)
            embed.add_field(name="💰 Blines", value=f"`{pj.get('blines', 0)}`", inline=True)
            embed.add_field(name="📏 Estatura", value=f"`{pj.get('estatura', 'No definida')}`", inline=True)
            embed.add_field(name="🎂 Edad", value=f"`{pj.get('edad', 'No definida')}`", inline=True)

            # Fila 3: Bloques de texto completo (Ancho completo)
            frase = pj.get('frase', 'Sin frase registrada.')
            embed.add_field(name="🗣️ Frase Representativa", value=f"> *\"{frase}\"*", inline=False)

            # Gestión limpia del Link / Imagen
            link_img = pj.get('link')
            if link_img and link_img.startswith("http"):
                embed.add_field(name="🔗 Documentación", value=f"[Visualizar Hoja de Personaje]({link_img})", inline=False)
                # Si 'link' es un enlace directo a una imagen (ej. imgur, discordapp), podés activar la línea de abajo:
                # embed.set_image(url=link_img)

            embed.add_field(
                name="🔗 Hoja / Nivel20",
                value='link',
                inline=False
            )

            # Elementos estéticos de cierre
            embed.set_thumbnail(url=usuario.display_avatar.url)
            embed.set_footer(text=f"ID Único: {nick_pj} • Sistema RPG", icon_url=self.bot.user.display_avatar.url)
            embed.timestamp = discord.utils.utcnow()

            await interaction.response.send_message(embed=embed)

    # =========================
    # DAR BLINES
    # =========================

    @app_commands.command(
        name="dar_blines",
        description="Dar blines a un personaje"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        usuario="Dueño del personaje",
        nick_pj="Nick del personaje",
        cantidad="Cantidad de blines"
    )

    async def dar_blines(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member,
        nick_pj: str,
        cantidad: int
    ):

        data = load_data()

        user_id = str(usuario.id)

        nick_pj = nick_pj.lower()

        if user_id not in data:

            await interaction.response.send_message(
                "❌ Usuario no encontrado.",
                ephemeral=True
            )
            return

        personajes = data[user_id].get("personajes", {})

        if nick_pj not in personajes:

            await interaction.response.send_message(
                "❌ Personaje no encontrado.",
                ephemeral=True
            )
            return

        pj = personajes[nick_pj]

        pj["blines"] += cantidad

        save_data(data)

        await interaction.response.send_message(
            f"💰 `{nick_pj}` recibió {cantidad} Blines."
        )

    # =========================
    # VER BLINES
    # =========================

    @app_commands.command(
        name="ver_blines",
        description="Ver blines de un personaje"
    )

    @app_commands.describe(
        usuario="Dueño del personaje",
        nick_pj="Nick del personaje"
    )

    async def ver_blines(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member,
        nick_pj: str
        ):

        data = load_data()

        user_id = str(usuario.id)

        nick_pj = nick_pj.lower()

        if user_id not in data:

            await interaction.response.send_message(
                "❌ Usuario no encontrado.",
                ephemeral=True
            )
            return

        personajes = data[user_id].get("personajes", {})

        if nick_pj not in personajes:

            await interaction.response.send_message(
                "❌ Personaje no encontrado.",
                ephemeral=True
            )
            return

        pj = personajes[nick_pj]

        embed = discord.Embed(
            title="💰 Blines",
            description=f"{pj['nombre']} tiene **{pj['blines']}** Blines.",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed)


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(PersonajesCog(bot))

    print("✅ PersonajesCog cargado")

# -

