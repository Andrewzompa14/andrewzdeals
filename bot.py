import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# URL for the image you want to use in the embed footer and as avatar
embed_footer_image_url = "https://imgur.com/a/15KBf8T"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

def read_webhooks():
    with open('webhooks.txt', 'r') as file:
        webhooks = [line.strip() for line in file]
        print(f"Read webhooks: {webhooks}")  # Debugging log
        return webhooks

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is from a specific channel
    if message.channel.id == 1269073024510853270:  # Replace with your channel ID
        # Create an embed from the message
        embed = discord.Embed(description=message.content, color=0x1E90FF)
        embed.set_footer(text="Andrew Z Deals", icon_url=embed_footer_image_url)

        # Check if there's an image attachment
        for attachment in message.attachments:
            # Fetch the attachment to determine its content type
            response = requests.head(attachment.url)
            content_type = response.headers.get('content-type')
            if content_type and content_type.startswith('image/'):
                embed.set_image(url=attachment.url)
                print(f"Image URL: {attachment.url}")
            else:
                print(f"Attachment found but not an image: {attachment.url}")

        # Read webhooks dynamically
        webhooks = read_webhooks()

        # Send the embed to all webhooks
        for webhook_url in webhooks:
            print(f"Sending to webhook: {webhook_url}")  # Debugging log
            data = {
                "username": "Andrew Z Deals",  # Custom username
                "avatar_url": embed_footer_image_url,  # Custom avatar URL
                "embeds": [embed.to_dict()]  # Embed converted to dict
            }
            response = requests.post(webhook_url, json=data)
            print(f"Webhook URL: {webhook_url}, Response: {response.status_code}, Response Content: {response.content}")

    await bot.process_commands(message)

# Run the bot using the token from the environment variables
bot.run(DISCORD_BOT_TOKEN)
