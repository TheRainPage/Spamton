# Spamton Discord Bot

## Overview
A Discord bot built with discord.py that provides slash commands for sending messages in channels and DMs.

## Features
- `/replydm` - Sends a message back in the current channel or DM
- Works in guilds, DMs, and private channels
- Uses Discord slash commands (app_commands)

## Project Architecture
- **Language**: Python 3.12
- **Main Framework**: discord.py (v2.6.4)
- **Entry Point**: `main.py`

## Setup
1. Create a Discord bot at https://discord.com/developers/applications
2. Enable the required bot intents in the Discord Developer Portal
3. Add your bot token to the Replit Secrets as `DISCORD_BOT_TOKEN`
4. Click the Run button to start the bot

## Configuration
The bot requires the following environment variable:
- `DISCORD_BOT_TOKEN`: Your Discord bot token (stored in Replit Secrets)

## Recent Changes
- 2025-11-13: Initial setup in Replit environment
  - Migrated bot token to environment variable for security
  - Configured Python dependencies with uv
  - Set up proper .gitignore for Python projects
  - Created workflow to run the bot

## Development
The bot uses:
- Default Discord intents
- Command prefix: `!` (though slash commands are primary)
- Global command sync on startup
