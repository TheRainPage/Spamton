import discord
from discord.ext import commands
from discord import app_commands
import os

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

@bot.tree.command(name="replydm", description="Sends a message back in the current channel/DM.")
@app_commands.describe(message="The content of the message to send.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def reply_dm(interaction: discord.Interaction, message: str):
    try:
        await interaction.response.send_message(message)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to respond here.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

@bot.tree.command(name="dm", description="Sends you a direct message.")
@app_commands.describe(message="The message to send to your DMs.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def dm_user(interaction: discord.Interaction, message: str):
    try:
        # Send a DM to the user
        await interaction.user.send(message)
        # Confirm in the channel (ephemeral so only the user sees it)
        await interaction.response.send_message("I've sent you a DM!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't send you a DM. Please check your privacy settings.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Run the bot
bot.run(YOUR_BOT_TOKEN)