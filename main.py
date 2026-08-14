import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

# ডাইনামিক প্রেফিক্স ফাংশন
async def get_prefix(bot, message):
    # ডিফল্ট প্রেফিক্স (বড় হাতের, ছোট হাতের এবং স্পেস সহ)
    default_prefixes = ["nova", "nova ", "Nova", "Nova ", "NOVA", "NOVA "]
    
    if not message.guild:
        return default_prefixes
        
    # ডেটাবেস থেকে কাস্টম প্রেফিক্স চেক করা
    try:
        guild_data = await bot.db.guilds.find_one({"guild_id": message.guild.id})
        if guild_data and "prefix" in guild_data:
            custom_prefix = guild_data["prefix"]
            # কাস্টম প্রেফিক্সের সাথে স্পেস সহ এবং স্পেস ছাড়া দুটোই রিটার্ন করবে
            return [custom_prefix, f"{custom_prefix} "] + default_prefixes
    except:
        pass
        
    return default_prefixes

class NovaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix=get_prefix, intents=intents)
        
        # MongoDB কানেকশন সেটআপ
        mongo_uri = os.getenv('MONGO_URI') # আপনার .env ফাইলে MONGO_URI অ্যাড করে নেবেন
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.mongo_client["nova_economy"] # ডেটাবেসের নাম
        
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✅ Successfully loaded: {filename}')
                except Exception as e:
                    print(f'❌ Failed to load {filename}: {e}')

bot = NovaBot()

@bot.event
async def on_ready():
    print('--------------------------------')
    print(f'Logged in as: {bot.user.name}')
    print('MongoDB Connected!')
    print('Status: Online and Ready!')
    print('--------------------------------')

async def main():
    async with bot:
        token = os.getenv('TOKEN')
        if token is None:
            print("Error: Bot token not found in .env!")
            return
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())

