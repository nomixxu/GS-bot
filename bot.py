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
context_member = {}
last_context = {}

salutation = ['Slt', 'Salut', 'Bonjour', 'Bjr']
question_humeur = ['comment vas-tu ?', 'ca va ?', 'cv frrot ?']
melioratif = ['bien', 'ww', 'w', 'wep', 'oui']
pejoratif  = ['mal', 'pas', 'non']
deception = ['dommage', 'outch']
enthousiasme = ['super', 'genial', 'incroyable']
question_interet = ['pourquoi ?', 'que se passe-t-il ?', "tu veux m'en parler ?"]
recomfort = ['Je comprend', "Ne t'inquiete pas", 'Ne sois pas trist', "Ce n'est pas ta faute"]
insultes = ['salope', 'f2p', 'connard', 'enculer', 'slp']

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

    async def response(store):
        global last_context
        if message.author.id == store["author"]:

            if store["action"] == "humeur":
                words = message.content.lower()
                if any(word in words for word in melioratif) and not any(word in words for word in pejoratif):
                    response = await message.reply(f"{random.choice(["C'est ", ""])}{random.choice(enthousiasme)} !")
                    tons = "content"
                elif any(word in words for word in pejoratif):
                    response = await message.reply(f"{random.choice(deception)}... {random.choice(question_interet)}")
                    tons = "triste"
                else:
                    await message.reply(f"je ne saurais pas discerné ce qui est bien ou pas, recommence avec 'oui' ou 'pas bien' ou encore 'non' ?!")
                    return
                author_id = store["author"]
                context.pop(store["message_id"], None)
                last_context.pop(author_id, None)
                next_store = {"author": author_id, "action": "interet", "tons": tons, "message_id": response.id}
                context[response.id] = next_store
                last_context[author_id] = next_store
                print(context)

            elif store["action"] == "interet":
                if store["tons"] == "triste":
                    await message.reply(f"{random.choice(recomfort)}, [trouver context et repondre en rapport !]")
                elif store["tons"] == "content":
                    await message.reply(f"{random.choice(enthousiasme)}, [add more infos ?]")
                else:
                    await message.reply("bot context error !")
                context.pop(store["message_id"], None)
                last_context.pop(store["author"], None)
            else:
                await message.reply("bot context error !")
                return
    if not message.reference:
        if not message.content.startswith("!"):
            return
        store = last_context.get(message.author.id)
        if store is not None:
            await response(store)
    if message.reference:
        replied_id = message.reference.message_id
    
        if replied_id in context:
            await response(context[replied_id])
    if not message.content.startswith("!"):
        return
    if message.author.bot:
        return
    msg = message.content.lower().strip().replace(" ", "").replace("!", "")
    if any(word.lower() in msg for word in salutation): #comprend que l'action est une salutation !
        author = message.author
        author_id = message.author.id
        response = await message.reply(f"{random.choice(salutation)} `{author}` {random.choice(question_humeur)}")
        previous = last_context.get(author_id)
        if previous is not None:
            context.pop(previous["message_id"], None)
        store = {"author": author_id, "action": "humeur", "message_id": response.id}
        context[response.id] = store
        last_context[author_id] = store
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
