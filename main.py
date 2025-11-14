import discord
from discord.ext import commands
from discord import app_commands
import os
import random
import asyncio

# --- CONFIGURATION ---
YOUR_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not YOUR_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set. Please add your Discord bot token to Secrets.")

# Strip any whitespace that might have been added
YOUR_BOT_TOKEN = YOUR_BOT_TOKEN.strip()
# ---------------------

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to track active spam tasks by channel ID
active_spam_tasks = {}

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
    "BUY SOMETHIN WILL YA!!",
    "THAT'S [Fifty Percent Off] FOR YOU!!",
    "I'M GONNA BE A [Big Shot]!!",
    "DON'T YOU [Little Sponge] WANT TO HELP AN OLD FRIEND?!",
    "HEAVEN KNOWS I'VE BEEN [Broke] FOR A WHILE!!",
    "ALL I NEED IS THAT [[Sweet, Sweet]] [Kromer]!!",
    "I CAN MAKE YOU [Powerful]!!",
    "EVEN A [Stupid] LITTLE [Worm] LIKE YOU CAN BE A [Big Shot]!!",
    "IT'S TIME TO BE A [Big Shot]!! A REAL [Big Shot]!!",
    "LIGHT [[Specil Attack]]!!",
    "NO MORE BEING THE [Little] GUY!!",
    "ARE YOU [Desperate] ENOUGH TO TAKE MY [Deal]?!",
    "TAKE A GOD DAMN [Vacation] STRAIGHT TO HELL!!",
    "I KNOW YOU'RE WATCHING!!",
    "[[It Burns! Ow! Stop! Help Me! It Burns!]]",
    "KRIS!! CAN YOU [[Hear Me??]]",
    "I JUST WANTED TO BE [Big]...",
    "DEALS SO GOOD I'LL [[Blow Your Mind]]!!",
    "WHY DON'T YOU [Answer The Phone]?!",
    "THE [[Number 1 Rated Salesman1997]]!!",
    "WHAT ARE YOU [Waiting For]?!",
    "COME ON!! JUST A LITTLE MORE [[Kromer]]!!",
    "I'M GOING TO BE [Rich]!!",
    "YOU [Little Sponge]!! STOP IGNORING ME!!",
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

async def spam_loop(channel, channel_id):
    """Background task that sends random messages every 1-5 minutes"""
    try:
        while True:
            # Wait for a random interval between 1-5 minutes (60-300 seconds)
            wait_time = random.randint(0, 15)
            await asyncio.sleep(wait_time)
            
            # Send a random message
            message = random.choice(RANDOM_MESSAGES)
            await channel.send(message)
    except asyncio.CancelledError:
        # Task was cancelled, clean exit
        pass
    except Exception as e:
        # Log error and notify about failure
        print(f"Error in spam loop for channel {channel_id}: {e}")
        try:
            await channel.send("I [CRASHED]!! USE /spam TO START ME AGAIN!!")
        except:
            pass
    finally:
        # Always clean up the task reference, preventing memory leaks
        if channel_id in active_spam_tasks:
            del active_spam_tasks[channel_id]

@bot.tree.command(name="spam", description="Start sending random messages every 1-5 minutes.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def start_spam(interaction: discord.Interaction):
    try:
        channel_id = interaction.channel_id
        
        # Check if spam is already active in this channel
        if channel_id in active_spam_tasks:
            await interaction.response.send_message("I'M ALREADY [Spamming] HERE!!", ephemeral=True)
            return
        
        # Create and store the background task
        task = asyncio.create_task(spam_loop(interaction.channel, channel_id))
        active_spam_tasks[channel_id] = task
        
        await interaction.response.send_message("NOW I'LL BE A [BIG SHOT] EVERY 1-5 MINUTES!! USE /stop TO MAKE ME [Quiet]!!")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to respond here.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"I died 💀: {e}", ephemeral=True)

@bot.tree.command(name="stop", description="Stop sending random messages.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def stop_spam(interaction: discord.Interaction):
    try:
        channel_id = interaction.channel_id
        
        # Check if spam is active in this channel
        if channel_id not in active_spam_tasks:
            await interaction.response.send_message("I'M NOT EVEN [Spamming] HERE!!", ephemeral=True)
            return
        
        # Cancel the task and remove it from the dictionary
        task = active_spam_tasks[channel_id]
        task.cancel()
        del active_spam_tasks[channel_id]
        
        await interaction.response.send_message("FINE!! I'LL STOP BEING A [BIG SHOT]... FOR NOW...")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to respond here.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"I died 💀: {e}", ephemeral=True)

# Run the bot
bot.run(YOUR_BOT_TOKEN)