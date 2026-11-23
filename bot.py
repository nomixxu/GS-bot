import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

print("lancement du bot ...")
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

salutation = ['Slt', 'Salut', 'Bonjour', 'Bjr']
question = ['comment vas-tu ?', 'ca va ?', 'cv frrot ?']

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
    if message.author.bot:
        return
    if message.content.lower().strip().replace(" ", "") == 'bonjourgs':
        channel = message.channel
        author = message.author
        await channel.send(f"{random.choice(salutation)} `{author}` {random.choice(question)")

@bot.tree.command(name="youtube", description="envoie le liens vers la chaine @Nomix")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message("Rejoins Nomix 👉 [ici](https://www.youtube.com/@NomixMC)")

@bot.tree.command(name="warn", description="⚠️ warn un utilisateur")
async def warn(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("alerte envoyée colonel 🫡")
    await member.warn()
    await member.send(f"Vous avez reçu un **⚠️avertissement⚠️** sur le serveur discord **{interaction.guild.name}** !")

bot.run(os.getenv('TOKEN'))
