import os

import discord
from dotenv import load_dotenv

from main.bot import responses
from main.db.db_config import connect
from main.logic.exceptions.CustomExceptions import UserHasNoCharactersError, PaydayAlreadyClaimedError
from main.logic.logic_api import ClaimPaydayUseCase, ReportMissionUseCase

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.command(name="reportar_partida",
             description="Comando exclusivo de DMs que sirve para añadir ACPs y TCPs a un grupo de personajes.")
async def add_reward(ctx, mission_title: str, time_played_minutes: int, character_names: str, mission_report: str):
    character_names_list = character_names.split(" ")

    character_users = ReportMissionUseCase(character_names_list, time_played_minutes, 0, str(ctx.author)).execute(connect())
    msg = responses.get_report_mission(mission_title, character_users, time_played_minutes, mission_report)

    await ctx.respond(msg)


@bot.command(name="reclamar_paga", description="Reclama el salario semanal para todos tus personajes.")
async def claim_payday(ctx):
    author = str(ctx.author)
    try:
        character_users = ClaimPaydayUseCase(author, author).execute(connect())
        await ctx.respond(responses.get_payday_response(character_users, ctx.author.mention))
    except UserHasNoCharactersError:
        await ctx.respond(responses.get_payday_response_user_has_no_characters(ctx.author.mention))
    except PaydayAlreadyClaimedError:
        await ctx.respond(responses.get_payday_response_payday_already_claimed(ctx.author.mention))


@bot.command(name="registrar_usuario_y_personaje", description="Registra un personaje para un usario.")
async def register_user_and_character(ctx, user: discord.Option(discord.Member, "Select a user"), character_name: str,
                                      level: int):
    print("wip")
    # response = logic_api.assign_user_with_chracter(str(user), str(user.id), character_name, level, str(ctx.author))
    #
    # if response == "inserted_new_user":
    #     await ctx.respond(
    #         f"Se ha creado el nuevo usuario ***{str(user)}*** y se le ha añadido el personaje ***{character_name} [LvL {str(level)}]*** a la lista de personajes.")
    # elif response == "added_new_character":
    #     await ctx.respond(
    #         f"Se ha añadido a ***{character_name} [LvL {str(level)}]*** a la lista de personajes de {str(user)}.")
    # elif response == "character_already_exists":
    #     await ctx.respond(
    #         f"El personaje ***{character_name}*** ya está en la lista de personajes de ***{str(user)}***.")


def start_bot():
    load_dotenv()
    bot.run(os.getenv('DISCORD_TOKEN'))
