import discord
from discord.ext import commands
from discord import app_commands
import os
import random

# --- CONFIGURATION ---
YOUR_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not YOUR_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set. Please add your Discord bot token to Secrets.")

# Strip any whitespace that might have been added
YOUR_BOT_TOKEN = YOUR_BOT_TOKEN.strip()
print(f"Token loaded: {len(YOUR_BOT_TOKEN)} characters")
# ---------------------

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() # Global sync
    print(f'Logged in as {bot.user} and commands synced globally!')

@bot.tree.command(name="reply", description="Sends a message back in the current channel/DM.")
@app_commands.describe(message="The content of the message to send.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def reply_dm(interaction: discord.Interaction, message: str):
    try:
        await interaction.response.send_message(message)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to respond here.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"I died 💀: {e}", ephemeral=True)

# Random messages for the random command
RANDOM_MESSAGES = [
    "HEY EVERY      !! IT'S ME!!!",
    "HOCHI MAMA!!",
    "NOW'S YOUR CHANCE TO BE A [BIG SHOT]!!!",
    "KRIS!! I NEED YOUR [Hyperlink Blocked]!!",
    "NOWS YOUR CHANCE TO [Become a Big Shot]!!",
    "I'M A [Big Shot]!! A [Big Shot]!!",
    "PLEASE!! I JUST WANT TO BE [BIG]!!",
    "[[Hyperlink Blocked]]",
    "GET YOUR OWN [[HeartShapedObject]]!!",
    "I'M LIVING IN A [Dumpster]!!",
    "LOOKS LIKE YOU'RE [Desperate]!!",
    "DON'T YOU WANNA BE A [Big Shot]?!",
    "I USED TO BE NOTHING BUT THE E_MAIL GUY...",
    "PIPIS",
    "WELCOME TO THE CITY OF [Burning Acid]!!",
    "YOU WANT [Kromer]?!",
]

@bot.tree.command(name="random", description="Sends a random message in the current channel.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def random_message(interaction: discord.Interaction):
    try:
        message = random.choice(RANDOM_MESSAGES)
        await interaction.response.send_message(message)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to respond here.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"I died 💀: {e}", ephemeral=True)

# Run the bot
bot.run(YOUR_BOT_TOKEN)