import discord
import secret

from discord.ext import commands
from discord import app_commands
from views.matchmaking_views import RoleSelectView
from services.matchmaking_service import register_user
from discord.ext import tasks

from services.matchmaking_service import (

    register_user,
    save_availability,

    join_queue,
    leave_queue,
    is_in_queue,

    get_queue_users,
    get_user_availability,
    get_user_roles,

    remove_users_from_queue,

    are_users_compatible,
    compatibility_score    

)

WEEKDAYS = [

    "Lunes",
    "Martes",
    "Miercoles",
    "Jueves",
    "Viernes",
    "Sabado",
    "Domingo"

]


class MatchmakingCog(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

        self.matchmaking_loop.start()

    @app_commands.command(
        name="matchmaking",
        description="Entrar al sistema de matchmaking"
    )

    async def matchmaking(
        self,
        interaction: discord.Interaction
    ):

        try:
            user_id = str(interaction.user.id)

            if is_in_queue(user_id):

                await interaction.response.send_message(

                    "❌ Ya estás en matchmaking.\n"
                    "Usa `/salir_cola` primero.",

                    ephemeral=True
                )

                return

            dm = await interaction.user.create_dm()

            embed = discord.Embed(

                title="🎲 Matchmaking __***INICIADO***__",

                description=(

                    "¿Qué deseas ser?\n\n"

                    "### 1️⃣ *Player*\n"
                    "### 2️⃣ *DM*\n"
                    "### 3️⃣ *Ambos*\n\n"

                    "Escribe el número en este MD :3."

                ),

                color=discord.Color.blurple()
            )

            await dm.send(embed=embed)

            await interaction.response.send_message(

                "📨 Te envié un DM.",

                ephemeral=True
            )

            def check(m):
                return (

                    m.author.id == interaction.user.id
                    and isinstance(
                        m.channel,
                        discord.DMChannel
                    )

                )



            respuesta = await self.bot.wait_for(

                "message",

                check=check,

                timeout=300

            )

            contenido = respuesta.content.strip()

            is_player = False
            is_dm = False

            if contenido == "1":

                is_player = True

            elif contenido == "2":

                is_dm = True

            elif contenido == "3":

                is_player = True
                is_dm = True
            # =========================
            # TIMEZONE
            # =========================

            await dm.send(

                "🌍 Ingresa tu UTC.\n\n"

                "Ejemplos:\n"
                "`-3`\n"
                "`+1`\n"
                "`-5`"
            )

            respuesta_utc = await self.bot.wait_for(

                "message",

                check=check,

                timeout=300
            )

            timezone = respuesta_utc.content.strip()
            # =========================
            # REGISTER USER
            # =========================

            register_user(

                user_id=interaction.user.id,

                is_player=is_player,
                is_dm=is_dm,

                timezone=timezone

            )
            await dm.send(

                "✅ Registro completado.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "📅 Ahora configuraremos tu disponibilidad semanal.\n"
            )

            # =========================
            # WEEKLY AVAILABILITY
            # =========================

            for weekday in WEEKDAYS:

                await dm.send(

                    f"# 📅 {weekday}\n\n"
                    
                    "*Este dia para ti es*:\n"
                    "1️⃣ 💚Día **Ideal**\n"
                    "2️⃣ 💛Seguro Puedo Pero **Prefiero otro dia**\n"
                    "3️⃣ ♥️Preferentemente **no**\n\n"

                    "**Escribe un número segun las opciones** *(1, 2, 3)*."
                )

                respuesta_dia = await self.bot.wait_for(

                    "message",

                    check=check,

                    timeout=300
                )

                opcion = respuesta_dia.content.strip()

                estado = None

                if opcion == "1":

                    estado = "ideal"

                elif opcion == "2":

                    estado = "flexible"

                # elegir estado del día
                if opcion == "3":
                    estado = "avoid"

                    if estado == "avoid":

                        await dm.send(

                            f"⏭️ {weekday} omitido."
                        )

                        continue

                    continue  # 🔥 salta al siguiente día

                else:

                    await dm.send(

                        "❌ Opción inválida. Día omitido."
                    )

                    continue

                # =========================
                # START TIME
                # =========================

                await dm.send(
                    "\n━━━━━━━━━━━━━━━━━━\n"
                    "### __***DIA***__ – ✅\n"
                    "⏰ Dime la **hora de inicio** :3\n"
                    "**Formato**: HH:MM\n"
                    "**Ejemplo**: 21:00\n"
                    "━━━━━━━━━━━━━━━━━━"
                )

                respuesta_hora = await self.bot.wait_for(

                    "message",

                    check=check,

                    timeout=300
                )

                hora_inicio = respuesta_hora.content.strip()

                # =========================
                # DURATION
                # =========================

                await dm.send(
                    "====================\n"
                    "🕓 **Duración estimada en horas**.\n"
                    "Ejemplo: 4 🕓\n"
                    "====================\n\n"
                )

                respuesta_duracion = await self.bot.wait_for(

                    "message",

                    check=check,

                    timeout=300
                )
                try:

                    duracion = int(

                        respuesta_duracion.content.strip()
                    )

                except:

                    await dm.send(

                        "❌ Duración inválida.\n"
                        "Ejemplo válido: `4`"
                    )

                    continue

                # =========================
                # SAVE
                # =========================

                save_availability(

                    user_id=interaction.user.id,

                    weekday=weekday,

                    status=estado,

                    start_time=hora_inicio,

                    duration=duracion
                )

                await dm.send(

                        f"✅ {weekday} guardado como {estado}."
                    )
                join_queue(

                    interaction.user.id
                )
                await dm.send(

                    "# 🎉 Configuración semanal **completada**.\n\n"
                    "🐢Gracias por ayudar a este servidor buscando grupo... esperamos que tengas la mejor experiencia y de parte de todo el satff y roko te mandamos la mejor de las suertes **GRACIAS!! ;3**\n"
                )

            pass
        
        except Exception as e:

            print(e)

    # =========================
    # LEAVE QUEUE
    # =========================

    @app_commands.command(
        name="salir_cola",
        description="Salir del matchmaking"
    )
    async def salir_cola(
        self,
        interaction: discord.Interaction
    ):

        user_id = str(interaction.user.id)

        if not is_in_queue(user_id):

            await interaction.response.send_message(

                "❌ No estás en matchmaking.",

                ephemeral=True
            )

            return

        leave_queue(user_id)

        await interaction.response.send_message(

            "✅ Saliste del matchmaking correctamente.",

            ephemeral=True
        )

    # =========================
    # MATCHMAKING STATUS
    # =========================

    @app_commands.command(
        name="cola",
        description="Ver estado de matchmaking"
    )
    async def cola(
        self,
        interaction: discord.Interaction
    ):

        queue_users = get_queue_users()

        players = 0
        dms = 0

        for usuario in queue_users:

            roles = get_user_roles(usuario["user_id"])

            if roles["role_player"] == 1:
                players += 1

            if roles["role_dm"] == 1:
                dms += 1

        user_id = str(interaction.user.id)

        estado = "🔴 No estás en cola"

        if is_in_queue(user_id):

            estado = "🟢 Estás en matchmaking"

        await interaction.response.send_message(

            f"""
# 🎲 Estado Matchmaking

{estado}

## 👥 Players
{players}

## 🧙 DMs
{dms}
""",

            ephemeral=True
        )

    @tasks.loop(seconds=30)
    async def matchmaking_loop(self):

        print("🔄 Matchmaking corriendo...")
        queue_users = get_queue_users()

        players = []
        dms = []

        for usuario in queue_users:

            user_id = usuario["user_id"]

            roles = get_user_roles(user_id)

            if roles["role_player"] == 1:

                players.append(user_id)

            if roles["role_dm"] == 1:

                dms.append(user_id)

        print(f"🎮 Players: {len(players)}")
        print(f"🧙 DMs: {len(dms)}")

        # =========================
        # FIND COMPATIBLE PLAYERS
        # =========================

        grupo_players = []

        for player_id in players:

            availability_1 = get_user_availability(player_id)

            compatibles = [player_id]

            for other_player in players:

                if other_player == player_id:

                    continue

                availability_2 = get_user_availability(other_player)

                compatible = are_users_compatible(

                    availability_1,
                    availability_2
                )

                if compatible:

                    other_user_data = get_user_roles(other_player)

            score = compatibility_score(

                usuario,
                {
                    "user_id": other_player,
                    "timezone": other_user_data["timezone"]
                }
            )

            if score >= 15:

                compatibles.append(other_player)

                print(f"✅ Compatible {player_id} ↔ {other_player} | Score: {score}")

            # grupo encontrado
            if len(compatibles) >= 4:

                grupo_players = compatibles[:4]

                break

        # =========================
        # NO GROUP FOUND
        # =========================

        if len(grupo_players) < 4:

            print("❌ No hay grupo compatible")

            return

        print(f"✅ Grupo compatible encontrado: {grupo_players}")

        # =========================
        # FIND DM
        # =========================

        grupo_dm = None

        for dm_id in dms:

            dm_availability = get_user_availability(dm_id)

            compatible_count = 0

            for player_id in grupo_players:

                player_availability = get_user_availability(player_id)

                compatible = are_users_compatible(

                    dm_availability,
                    player_availability
                )

                if compatible:

                    compatible_count += 1

            if compatible_count >= 4:

                grupo_dm = dm_id

                break
async def setup(bot):

    await bot.add_cog(MatchmakingCog(bot))

    print("✅ MatchmakingCog cargado")