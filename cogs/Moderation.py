import discord 
import asyncio
from discord.utils import get
from discord.ext import commands 

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client


    class DurationConverter(commands.Converter):
            async def convert(self, ctx, argument):
                amount = argument[:-1]
                unit = argument[-1]

                if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
                    return (int(amount), unit)

                raise commands.BadArgument(message='Not valid duration')



    @commands.command(aliases=['Kick'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"""L'utilisateur {member} a été kick pour " {reason} " """)


    
    @commands.command(aliases=['tban']) # Bannissement temporaire
    @commands.has_permissions(ban_members=True)
    async def Tban(self, ctx, member : commands.MemberConverter, duration : DurationConverter):

        multiplier = {'s' : 1, 'm': 60, 'h' : 3600, 'd' : 86400}
        amount, unit = duration

        await ctx.guild.ban(member)
        await ctx.send(f'{member} has been banned for {amount}{unit}.')
        await asyncio.sleep(amount * multiplier[unit])
        await ctx.guild.unban(member)



    @commands.command(aliases=['Ban']) # Bannissement permanent 
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"""L'utilisateur {member} a été banni pour " {reason} " """)



    @commands.command(aliases=['Unban'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: commands.MemberConverter):
        user = await commands.UserConverter().convert(ctx, member)
        if user is None:
            id_ = await commands.IDConverter().convert(str(member))
            if id_ is not None:
                try:
                    user = await self.client.fetch_user(int(id_.group(1)))
                except discord.Notfound:
                    user = None
            if user is None:
                await ctx.send('User not found')
                return
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned {user}')

    
    @commands.command(aliases=['Mute'])
    @commands.has_permissions()
    async def mute(self, ctx, member: commands.MemberConverter, *, duration: DurationConverter):

        role = get(member.guild.roles, name="Muted")
        multiplier = {'s' : 1, 'm': 60, 'h' : 3600, 'd' : 86400}
        amount, unit = duration


        if member.dm_channel == None:
            await member.create_dm()
        await member.dm_channel.send(content=f"Vous avez été muté pour une durée de {amount}{unit} \n Il vous sera impossible de converser sur le serveur jusqu'à la fin du temps imparti.")
        await member.add_roles(role)
        await asyncio.sleep(amount * multiplier[unit])
        await member.remove_roles(role)

        
        

async def setup(client):
    await client.add_cog(Moderation(client))