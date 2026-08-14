import discord
from discord.ext import commands

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setprefix", help="Change the custom prefix for this server.")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix: str):
        # প্রেফিক্স ক্লিন করা
        clean_prefix = new_prefix.strip()
        
        # MongoDB-তে সেভ করা
        await self.bot.db.guilds.update_one(
            {"guild_id": ctx.guild.id},
            {"$set": {"prefix": clean_prefix}},
            upsert=True
        )
        
        embed = discord.Embed(
            title="✨ Prefix Updated",
            description=(
                f"Successfully set the custom prefix to: **`{clean_prefix}`**\n\n"
                f"**Available Prefixes:**\n"
                f"1. `Nova` (Default - Always works)\n"
                f"2. `{clean_prefix}` (Your custom prefix)"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="Nova Economy System")
        await ctx.send(embed=embed)

    @set_prefix.error
    async def set_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ **Access Denied!** You need `Administrator` permission.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ **Usage:** `Nova setprefix <prefix>`")

async def setup(bot):
    await bot.add_cog(Prefix(bot))
    
