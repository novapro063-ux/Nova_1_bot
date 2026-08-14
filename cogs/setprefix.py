import discord
from discord.ext import commands
from discord import app_commands

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="setprefix", description="Change the custom prefix for this server.")
    @commands.has_permissions(administrator=True)
    @app_commands.describe(new_prefix="Type the new prefix (e.g., ! or ?)")
    async def set_prefix(self, ctx, new_prefix: str):
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
                f"**Usage:**\n"
                f"`{clean_prefix}bal` or `/balance`"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="Nova Economy System")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Prefix(bot))
    
