import discord
from discord.ext import commands
import os
import asyncio
import motor.motor_asyncio

# প্রেফিক্স লজিক
async def get_prefix(bot, message):
    # ডিফল্ট প্রেফিক্স 'Nova'
    prefixes = ["Nova", "nova", "NOVA"]
    
    if not message.guild:
        return prefixes

    try:
        # MongoDB থেকে কাস্টম প্রেফিক্স ফেচ করা
        guild_data = await bot.db.guilds.find_one({"guild_id": message.guild.id})
        if guild_data and "prefix" in guild_data:
            custom_prefix = guild_data["prefix"].strip()
            if custom_prefix and custom_prefix not in prefixes:
                prefixes.append(custom_prefix)
    except Exception as e:
        print(f"Error fetching prefix: {e}")
        
    return prefixes

class NovaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True 
        
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            help_command=None,
            case_insensitive=True,      # বড়/ছোট হাতের অক্ষর ডিটেক্ট করবে
            strip_after_prefix=True     # প্রেফিক্স এবং কমান্ডের মাঝখানে স্পেস থাকলে কাজ করবে
        )
        
        # MongoDB কানেকশন
        mongo_uri = os.getenv('MONGO_URI') 
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.mongo_client["nova_economy"] 
        
    async def setup_hook(self):
        print("--- Loading Cogs ---")
        if os.path.exists('./cogs'):
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        await self.load_extension(f'cogs.{filename[:-3]}')
                        print(f"✅ Loaded: {filename}")
                    except Exception as e:
                        print(f"❌ Failed: {filename} - {e}")
        
        # স্ল্যাশ কমান্ড সিঙ্ক
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands!")
        except Exception as e:
            print(f"❌ Sync failed: {e}")

bot = NovaBot()

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print('MongoDB Connected!')
    await bot.change_presence(activity=discord.Game(name="Nova bal | Economy"))

async def main():
    async with bot:
        token = os.getenv('TOKEN')
        if not token:
            print("Error: TOKEN not found!")
            return
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
    
