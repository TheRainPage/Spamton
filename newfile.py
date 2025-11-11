import discord
from discord.ext import commands
from discord import app_commands 

# --- CONFIGURATION ---
YOUR_BOT_TOKEN = "MTQxNDQ1MTY0MDMzNzA0MzQ2Nw.GFq2Jn.ajl5JUfuBT4sOm3c5XgbHwns6y0feMP2a4K7sY" 
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

# Run the bot
bot.run(YOUR_BOT_TOKEN)