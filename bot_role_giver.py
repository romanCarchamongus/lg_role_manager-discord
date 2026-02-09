import discord
from discord.ext import commands
import roleGiver as rg
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("TOKEN_LG")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.slash_command(description="attribuer des rôles")
async def give_roles(ctx, players: str, roles: str, create_channel:bool):
     list_players = [p for p in players.split(",")]
     list_roles = [r.strip() for r in roles.split(",")]
     if len(list_players) != len(list_roles):
         await ctx.respond("❌ Nombre de rôles et nombre de joueurs non correspondant", ephemeral=True)
         return
     dict_player = rg.assignRoles(list_roles, list_players)
    
     overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True),
        ctx.guild.me: discord.PermissionOverwrite(view_channel=True,send_messages=True, read_message_history=True)
     }
     channel_name = "tmp-compo"+ datetime.now().strftime("%d%m%Y%H%M")
     channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites, category=ctx.channel.category)
     
     response=""
     for k in dict_player.keys():
        if(create_channel):
            await createChannelForRoles(ctx, dict_player[k], member_from_mention(ctx.guild, k))
        response+=f"Joueur {k} => {dict_player[k]}\n"

    
     #channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
     await channel.send(response)
     await ctx.respond("roles distribués")
     #await ctx.respond(response)

@bot.slash_command(description="créer un salon pour un joueur")
async def create_role_channel(ctx,nom_role:str, joueur: discord.Member):
    await createChannelForRoles(ctx, nom_role, joueur)

async def createChannelForRoles(ctx, nom_role:str, joueur: discord.Member):
    if joueur is None:
        await ctx.respond("❌ Joueur introuvable", ephemeral=True)
    else:
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True),
        ctx.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
        }

        overwrites[joueur] = discord.PermissionOverwrite(view_channel=True)
        channel = await ctx.guild.create_text_channel("tmp-"+nom_role+"-"+joueur.name, overwrites=overwrites, category=ctx.channel.category)
        await channel.send('Ton rôle est : '+nom_role)
        await ctx.respond(f"Channel pour {joueur} créé")


def member_from_mention(guild: discord.Guild, mention: str) -> discord.Member | None:
    if mention.startswith("<@") and mention.endswith(">"):
        member_id = int(mention.replace("<@", "").replace("!", "").replace(">", ""))
        return guild.get_member(member_id)
    return None

@bot.slash_command(description="Supprimer les salons temporaires après la partie")
async def finish_game_channels(ctx):
    for channel in ctx.guild.text_channels:
        if channel.name.startswith("tmp-"):
            await channel.delete()
    await ctx.respond("Suppression des salons temporaires effectuée")


bot.run(TOKEN)