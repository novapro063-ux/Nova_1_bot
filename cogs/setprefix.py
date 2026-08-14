import discord
from discord.ext import commands

class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setprefix", help="Change the bot's prefix for this server.")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        # MongoDB তে ওই সার্ভারের প্রেফিক্স আপডেট বা সেভ করা
        await self.bot.db.guilds.update_one(
            {"guild_id": ctx.guild.id},
            {"$set": {"prefix": new_prefix}},
            upsert=True
        )
        
        embed = discord.Embed(
            description=f"✅ Server prefix has been successfully updated to: **`{new_prefix}`**\n*Note: The default `nova` prefix will still work!*",
            color=0x2ecc71
        )
        await ctx.send(embed=embed)

    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need **Administrator** permission to change the prefix.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Please provide a new prefix! Example: `nova setprefix !`")

async def setup(bot):
    await bot.add_cog(SetPrefix(bot))
  
