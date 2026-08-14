import discord
from discord.ext import commands

class Cash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cash_emoji = "<:Nova:1453460518764548186>" # আপনার দেওয়া কাস্টম ইমোজি

    @commands.command(name="balance", aliases=["bal", "cash", "money", "wallet"], help="Check your current balance.")
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        # MongoDB থেকে ইউজারের ব্যালেন্স ফেচ করা
        user_data = await self.bot.db.users.find_one({"user_id": member.id})
        
        # যদি ডেটাবেসে ইউজার না থাকে, তবে তার ব্যালেন্স হবে 0
        balance = user_data.get("wallet", 0) if user_data else 0

        # ছবির সাথে হুবহু মিল রেখে এমবেড ডিজাইন (Green border)
        embed = discord.Embed(color=0x1ABC9C) # Cyan-Green color based on the image
        
        # ডিসপ্লে নেম এবং হুবহু টেক্সট ফরম্যাটিং
        embed.description = f"**{member.display_name}** you currently have... {self.cash_emoji}\n`{balance}` currency!!"

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cash(bot))
  
