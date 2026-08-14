import discord
from discord.ext import commands
from discord import app_commands

class Cash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cash_emoji = "<:Nova:1453460518764548186>"

    @commands.hybrid_command(name="balance", aliases=["bal", "cash", "money"], description="Check your current balance.")
    @app_commands.describe(member="Check someone else's balance (optional)")
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        # MongoDB থেকে ব্যালেন্স আনা
        user_data = await self.bot.db.users.find_one({"user_id": member.id})
        balance = user_data.get("wallet", 0) if user_data else 0

        # ছবির স্টাইল অনুযায়ী এমবেড (Simple and clean)
        embed = discord.Embed(color=0x1ABC9C)
        embed.description = f"**{member.display_name}** you currently have... {self.cash_emoji}\n`{balance}` currency!!"

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cash(bot))
    
