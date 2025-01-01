import discord
import aiohttp
import asyncio
import json

# Your bot's token and Nomi AI API key
discord_token = 'DISCORD_BOT_TOKEN'  # Replace with your actual Discord bot token
nomi_api_key = 'NOMI_API_KEY'  # Replace with your actual Nomi API key
nomi_api_url = 'NOMI_API_CHAT_ENDPOINT_URL'  # Replace with your Nomi AI chat endpoint URL

# Set up the client
intents = discord.Intents.default()
intents.message_content = True  # Make sure the bot can read messages
client = discord.Client(intents=intents)

async def get_nomi_reply(message_content):
    # Prepare headers for the Nomi API request
    headers = {
        "Authorization": nomi_api_key,
        "Content-Type": "application/json",
    }

    # Prepare the data to send in the request
    data = {
        "messageText": message_content  # Pass the full message to the Nomi AI
    }

    # Make the HTTP request asynchronously
    async with aiohttp.ClientSession() as session:
        async with session.post(nomi_api_url, headers=headers, json=data) as response:
            if response.status == 200:
                nomi_response = await response.json()
                return nomi_response.get("replyMessage", {}).get("text", "No response from Nomi AI.")
            else:
                return "Error connecting to Nomi AI."

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == client.user:
        return

    # Print received message for debugging purposes
    print(f"Received message: {message.content}")

    # Get response from Nomi AI asynchronously
    bot_reply = await get_nomi_reply(message.content)

    # Send the response back to the Discord channel
    await message.channel.send(bot_reply)

# Run the bot with the Discord token
client.run(discord_token)
