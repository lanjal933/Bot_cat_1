import discord
from discord.ui import View, button, Select
from discord.ui import View, button

from services.matchmaking_service import register_user
from discord.ui import Select

from services.matchmaking_service import (
    register_user,
    save_availability
)

# =========================
# ROLE SELECT VIEW
# =========================

class RoleSelectView(View):

    def __init__(self):

        super().__init__(timeout=300)

# =========================
# PLAYER
# =========================

@button(
    label="🎲 Player",
    style=discord.ButtonStyle.primary
)

async def player_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):

    register_user(

        user_id=str(interaction.user.id),

        is_player=True,
        is_dm=False,

        timezone="UTC"

    )

    embed = discord.Embed(

        title="📅 Disponibilidad",

        description=(
            "Selecciona tu disponibilidad para:\n\n"
            "## Monday"
        ),

        color=discord.Color.blurple()
    )

    await interaction.response.edit_message(

        embed=embed,

        view=AvailabilityView(0)
    )


# =========================
# DM
# =========================

@button(
    label="🧙 DM",
    style=discord.ButtonStyle.secondary
)

async def dm_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):

    register_user(

        user_id=str(interaction.user.id),

        is_player=False,
        is_dm=True,

        timezone="UTC"

    )

    embed = discord.Embed(

        title="📅 Disponibilidad",

        description=(
            "Selecciona tu disponibilidad para:\n\n"
            "## Monday"
        ),

        color=discord.Color.blurple()
    )

    await interaction.response.edit_message(

        embed=embed,

        view=AvailabilityView(0)
    )

# =========================
# BOTH
# =========================

@button(
    label="⚔ Both",
    style=discord.ButtonStyle.success
)

async def both_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):

    register_user(

        user_id=str(interaction.user.id),

        is_player=True,
        is_dm=True,

        timezone="UTC"

    )

    embed = discord.Embed(

        title="📅 Disponibilidad",

        description=(
            "Selecciona tu disponibilidad para:\n\n"
            "## Monday"
        ),

        color=discord.Color.blurple()
    )

    await interaction.response.edit_message(

        embed=embed,

        view=AvailabilityView(0)
    )

# =========================
# AVAILABILITY VIEW
# =========================

class AvailabilityView(View):

    def __init__(

        self,
        weekday_index=0

    ):

        super().__init__(timeout=300)

        self.weekday_index = weekday_index

        self.add_item(

            AvailabilitySelect(
                weekday_index
            )
        )
# =========================
# MODAL HORARIO
# =========================

class TimeModal(discord.ui.Modal, title="Configurar Horario"):

    hora_inicio = discord.ui.TextInput(

        label="Hora de inicio",
        placeholder="Ejemplo: 21:00",
        required=True,
        max_length=5

    )

    duracion = discord.ui.TextInput(

        label="Duración estimada",
        placeholder="Ejemplo: 4",
        required=True,
        max_length=2

    )

    def __init__(

        self,
        user_id,
        dia,
        estado,
        weekday_index

    ):

        super().__init__()

        self.user_id = user_id
        self.dia = dia
        self.estado = estado
        self.weekday_index = weekday_index

    async def on_submit(self, interaction: discord.Interaction):

        from services.matchmaking_db import save_availability

        save_availability(

            user_id=self.user_id,
            day=self.dia,
            status=self.estado,
            start_time=self.hora_inicio.value,
            duration=int(self.duracion.value)

        )

        embed = discord.Embed(

            title="✅ Horario Guardado",
            color=discord.Color.green()

        )

        embed.add_field(
            name="📅 Día",
            value=self.dia.capitalize(),
            inline=True
        )

        embed.add_field(
                name="⏰ Inicio",
            value=self.hora_inicio.value,
            inline=True
        )

        embed.add_field(
            name="🕓 Duración",
            value=f"{self.duracion.value} horas",
            inline=True
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
        next_day = self.weekday_index + 1

        # Terminó toda la semana
        if next_day >= len(WEEKDAYS):

            embed = discord.Embed(

                title="✅ Matchmaking Configurado",

                description=(
                    "Tu disponibilidad semanal fue guardada.\n\n"
                    "Ya puedes entrar en cola."
                ),

                color=discord.Color.green()

            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

            return

        # Mostrar siguiente día
        next_weekday = WEEKDAYS[next_day]

        embed = discord.Embed(

            title="📅 Disponibilidad",

            description=(
                f"Selecciona tu disponibilidad para:\n\n"
                f"## {next_weekday}"
            ),

            color=discord.Color.blurple()

        )

        await interaction.channel.send(

            embed=embed,

            view=AvailabilityView(next_day)

        )
# =========================
# AVAILABILITY SELECT
# =========================

class AvailabilitySelect(Select):

    def __init__(

        self,
        weekday_index

    ):

        self.weekday_index = weekday_index

        weekday = WEEKDAYS[weekday_index]

        options = [

            discord.SelectOption(
                label="Ideal",
                description=f"{weekday} funciona perfecto",
                emoji="✅"
            ),

            discord.SelectOption(
                label="Flexible",
                description=f"{weekday} podría funcionar",
                emoji="🟡"
            ),

            discord.SelectOption(
                label="Prefer Not",
                description=f"Evitar este día",
                emoji="❌"
            )

        ]

        super().__init__(

            placeholder=f"{weekday}...",

            min_values=1,
            max_values=1,

            options=options
        )
        async def callback(self, interaction: discord.Interaction):

            valor = self.values[0]

            dia = "viernes"

            await interaction.response.send_modal(

                TimeModal(
                    user_id=interaction.user.id,
                    dia=dia,
                    estado=valor,
                    weekday_index=self.weekday_index
                )
            )