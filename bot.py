import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Read webhook URLs from file
with open('webhooks.txt', 'r') as file:
    webhooks = [line.strip() for line in file]

intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# URL for the image you want to use in the embed footer
embed_footer_image_url = "https://cdn.discordapp.com/attachments/1245140639235051624/1269076967261606018/2024-08-02_7.38.16_PM.jpg?ex=66aebf87&is=66ad6e07&hm=3a4ef986c2f963a595643b593372e6071cd70e4cdf5b3bd7b7eea0ed27624058"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

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

        # Send the embed to all webhooks
        for webhook_url in webhooks:
            data = {
                "username": "Andrew Z Deals",
                "avatar_url": embed_footer_image_url,
                "embeds": [embed.to_dict()]
            }
            response = requests.post(webhook_url, json=data)
            print(f"Webhook Response: {response.status_code}, Response Content: {response.content}")

    await bot.process_commands(message)

# Run the bot using the token from the environment variables
bot.run(DISCORD_BOT_TOKEN)
