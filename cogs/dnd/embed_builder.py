import discord

from discord.ext import commands
from discord import app_commands

from services.embed_manager import (
    load_embeds,
    save_embeds
)


class EmbedsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # CREAR EMBED
    # =========================

    @app_commands.command(
        name="crear_embed",
        description="Crear un nuevo embed editable"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre interno del embed"
    )

    async def crear_embed(
        self,
        interaction: discord.Interaction,
        nombre: str
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre in data:

            await interaction.response.send_message(
                "❌ Ese embed ya existe.",
                ephemeral=True
            )
            return

        data[nombre] = {

            "titulo": "",
            "descripcion": "",
            "color": 0x9b59b6,

            "campos": [],

            "imagen": "",
            "thumbnail": "",

            "footer": "",

            "message_id": None,
            "channel_id": None
        }

        save_embeds(data)

        await interaction.response.send_message(
            f"✅ Estructura del embed `{nombre}` creada.\n"
            f"🛠 Ahora podés editarlo y luego usar `/publicar_embed`. :3"
        )

    # =========================
    # EDITAR EMBED
    # =========================

    @app_commands.command(
        name="editar_embed",
        description="Editar contenido base de un embed"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre del embed",
        titulo="Título",
        descripcion="Descripción",
        footer="Footer"
    )

    async def editar_embed(
        self,
        interaction: discord.Interaction,
        nombre: str,
        titulo: str = None,
        descripcion: str = None,
        footer: str = None
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre not in data:

            await interaction.response.send_message(
                "❌ Embed no encontrado.",
                ephemeral=True
            )
            return

        embed_data = data[nombre]

        if titulo:
            embed_data["titulo"] = titulo

        if descripcion:
            embed_data["descripcion"] = descripcion

        if footer:
            embed_data["footer"] = footer

        save_embeds(data)

        await interaction.response.send_message(
            f"✅ Embed `{nombre}` actualizado."
        )

    # =========================
    # AGREGAR CAMPO
    # =========================

    @app_commands.command(
        name="agregar_campo",
        description="Agregar un campo a un embed"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre del embed",
        titulo="Título del campo",
        texto="Contenido",
        inline="¿Inline?"
    )

    async def agregar_campo(
        self,
        interaction: discord.Interaction,
        nombre: str,
        titulo: str,
        texto: str,
        inline: bool = False
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre not in data:

            await interaction.response.send_message(
                "❌ Embed no encontrado.",
                ephemeral=True
            )
            return

        data[nombre]["campos"].append({

            "name": titulo,
            "value": texto,
            "inline": inline

        })

        save_embeds(data)

        await interaction.response.send_message(
            f"✅ Campo agregado a `{nombre}`."
        )

    # =========================
    # AGREGAR IMAGEN
    # =========================

    @app_commands.command(
        name="agregar_imagen",
        description="Agregar imagen a un embed"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre del embed",
        url="URL de imagen"
    )

    async def agregar_imagen(
        self,
        interaction: discord.Interaction,
        nombre: str,
        url: str
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre not in data:

            await interaction.response.send_message(
                "❌ Embed no encontrado.",
                ephemeral=True
            )
            return

        data[nombre]["imagen"] = url

        save_embeds(data)

        await interaction.response.send_message(
            f"✅ Imagen agregada a `{nombre}`."
        )

    # =========================
    # PUBLICAR EMBED
    # =========================

    @app_commands.command(
        name="publicar_embed",
        description="Publicar embed"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre del embed"
    )

    async def publicar_embed(
        self,
        interaction: discord.Interaction,
        nombre: str
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre not in data:

            await interaction.response.send_message(
                "❌ Embed no encontrado.",
                ephemeral=True
            )
            return

        embed_data = data[nombre]

        embed = discord.Embed(
            title=embed_data["titulo"],
            description=embed_data["descripcion"],
            color=embed_data["color"]
        )

        # Campos
        for campo in embed_data["campos"]:

            embed.add_field(
                name=campo["name"],
                value=campo["value"],
                inline=campo["inline"]
            )

        # Imagen
        if embed_data["imagen"]:

            embed.set_image(
                url=embed_data["imagen"]
            )

        # Thumbnail
        if embed_data["thumbnail"]:

            embed.set_thumbnail(
                url=embed_data["thumbnail"]
            )

        # Footer
        if embed_data["footer"]:

            embed.set_footer(
                text=embed_data["footer"]
            )

        mensaje = await interaction.original_response()

        embed_data["message_id"] = mensaje.id
        embed_data["channel_id"] = interaction.channel.id

        save_embeds(data)

    # =========================
    # ACTUALIZAR EMBED
    # =========================

    @app_commands.command(
        name="actualizar_embed",
        description="Actualizar un embed ya publicado"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre del embed"
    )

    async def actualizar_embed(
        self,
        interaction: discord.Interaction,
        nombre: str
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre not in data:

            await interaction.response.send_message(
                "❌ Embed no encontrado.",
                ephemeral=True
            )
            return

        embed_data = data[nombre]

        # Verificar IDs
        if not embed_data["message_id"]:

            await interaction.response.send_message(
                "❌ Ese embed todavía no fue publicado.",
                ephemeral=True
            )
            return

        canal = self.bot.get_channel(
            embed_data["channel_id"]
        )

        if not canal:

            await interaction.response.send_message(
                "❌ Canal no encontrado.",
                ephemeral=True
            )
            return

        try:

            mensaje = await canal.fetch_message(
                embed_data["message_id"]
            )

        except:

            await interaction.response.send_message(
                "❌ Mensaje no encontrado.",
                ephemeral=True
            )
            return

        # =========================
        # CREAR EMBED
        # =========================

        embed = discord.Embed(
            title=embed_data["titulo"],
            description=embed_data["descripcion"],
            color=embed_data["color"]
        )

        # Campos
        for campo in embed_data["campos"]:

            embed.add_field(
                name=campo["name"],
                value=campo["value"],
                inline=campo["inline"]
            )

        # Imagen
        if embed_data["imagen"]:

            embed.set_image(
                url=embed_data["imagen"]
            )

        # Thumbnail
        if embed_data["thumbnail"]:

            embed.set_thumbnail(
                url=embed_data["thumbnail"]
            )

        # Footer
        if embed_data["footer"]:

            embed.set_footer(
                text=embed_data["footer"]
            )

        # =========================
        # EDITAR MENSAJE
        # =========================

        await mensaje.edit(embed=embed)

        await interaction.response.send_message(
            f"✅ Embed `{nombre}` actualizado."
        )
            # =========================
    # PREVIEW EMBED
    # =========================

    @app_commands.command(
        name="preview_embed",
        description="Previsualizar un embed"
    )

    @app_commands.checks.has_role("Staff")

    @app_commands.describe(
        nombre="Nombre del embed"
    )

    async def preview_embed(
        self,
        interaction: discord.Interaction,
        nombre: str
    ):

        data = load_embeds()

        nombre = nombre.lower()

        if nombre not in data:

            await interaction.response.send_message(
                "❌ Embed no encontrado.",
                ephemeral=True
            )
            return

        embed_data = data[nombre]

        # =========================
        # CREAR EMBED
        # =========================

        embed = discord.Embed(
            title=embed_data["titulo"],
            description=embed_data["descripcion"],
            color=embed_data["color"]
        )

        # Campos
        for campo in embed_data["campos"]:

            embed.add_field(
                name=campo["name"],
                value=campo["value"],
                inline=campo["inline"]
            )

        # Imagen
        if embed_data["imagen"]:

            embed.set_image(
                url=embed_data["imagen"]
            )

        # Thumbnail
        if embed_data["thumbnail"]:

            embed.set_thumbnail(
                url=embed_data["thumbnail"]
            )

        # Footer
        if embed_data["footer"]:

            embed.set_footer(
                text=embed_data["footer"]
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(EmbedsCog(bot))

    print("✅ EmbedsCog cargado")