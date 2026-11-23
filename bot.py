import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()

print("lancement du bot ...")
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

#context = {message_id: {author: auteur, context: "jouer"}}
context = {}

salutation = ['Slt', 'Salut', 'Bonjour', 'Bjr']
question = ['comment vas-tu ?', 'ca va ?', 'cv frrot ?']
melioratif = ['bien', 'ww', 'w', 'wep', 'oui']
pejoratif  = ['mal', 'pas']
deception = ['dommage', 'outch']
enthousiasme = ['super', 'genial', 'incroyable']

@bot.event
async def on_ready():
    print("bot allumé")
    try:
        synced = await bot.tree.sync()
        print(f"commandes syncronisées : {len(synced)}")
    except Exception as error:
        print(error)

@bot.event
async def on_message(message: discord.Message):
    if message.reference:
        replied_id = message.reference.message_id
    
        if replied_id in context:

            if message.author.id == context[replied_id]["author"]:

                if context[replied_id]["action"] == "humeur":
                    words = message.content.lower()
                    if any(word in words for word in melioratif) and not any(word in words for word in pejoratif):
                        await message.reply(f"{random.choice(["C'est ", ""])}{random.choice(enthousiasme)} !")
                    elif any(word in words for word in pejoratif):
                        await message.reply(f"{random.choice(deception)}... [remontage de moral ?]")
                    else:
                        await message.reply(f"je ne saurais pas discerné ce qui est bien ou pas, recommence avec 'oui' ou 'pas bien' ou encore 'non' ?!")
                        return
                    del context[replied_id]
                    print(context)
    if not message.content.startswith("!"):
        return
    if message.author.bot:
        return
    if message.content.lower().strip().replace(" ", "").replace("!", "") == 'bonjourgs':
        author = message.author
        author_id = message.author.id
        response = await message.reply(f"{random.choice(salutation)} `{author}` {random.choice(question)}")
        context[response.id] = {"author": author_id, "action": "humeur"}
        print(context)

@bot.tree.command(name="youtube", description="envoie le liens vers la chaine @Nomix")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message("Rejoins Nomix 👉 [ici](https://www.youtube.com/@NomixMC)")

@bot.tree.command(name="warn", description="⚠️ warn un utilisateur")
async def warn(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("alerte envoyée colonel 🫡")
    await member.warn()
    await member.send(f"Vous avez reçu un **⚠️avertissement⚠️** sur le serveur discord **{interaction.guild.name}** !")

@bot.tree.command(name="clear", description="🧹 nettoyer un salon")
async def clear(interaction: discord.Interaction, channel: discord.TextChannel, number: app_commands.Range[int, 1, 50]):
    await interaction.response.defer(ephemeral=True)
    deleted = await channel.purge(limit=number)
    author = interaction.user
    await author.send(f"🧹 Le salon **{channel}** a bien été nettoyé dans le serveur **{interaction.guild.name}** ! (__{number} messages ont été supprimés)__")
    await interaction.followup.send(f"{len(deleted)} messages supprimés.")
    
bot.run(os.getenv('TOKEN'))
