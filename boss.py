import discord
import sqlite3 # For accessing the the database to  make the data easier to manager long term
import os # For loading the token from .env file
from dotenv import load_dotenv # For loainding the token from .env file

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

def get_quote():
    connection = sqlite3.connect('boss.db')
    cursor = connection.cursor()
    bossQuote = cursor.execute("SELECT Name, Quote FROM Quote INNER JOIN Boss ON Quote.Boss = Boss.BID ORDER BY RANDOM() LIMIT 1").fetchone()

    quote = f'{bossQuote[1]} - {bossQuote[0]}'

    connection.close()
    return quote


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$boss'):
            await message.channel.send(get_quote())

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token) # Replace with your own token if you aren't using a .env file or have it in your local constants.
