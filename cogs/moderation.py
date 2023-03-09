import disnake
import json
import os
import asyncio
from disnake.ext import commands
from modules.general import color
from modules.general import file_open

prefi = "/"

data = file_open('./storage/main.json')
            
try:
    Mute_roles = file_open("./storage/mute_role.json")
except:
    print("hey dont mess with mute_role.json")
    
class Moderation(commands.Cog):
    
    def __init__(self,client):
        self.client = client
    
    @commands.slash_command(default_member_permissions=disnake.Permissions(kick_members = True),description="Used to kick members")
    async def kick(ctx:disnake.ApplicationCommandInteraction, user: disnake.User, reason:str=None):
        if data["kick_settings"]["kick"] == True:
            if user.id == ctx.guild.me.id:
                await ctx.send("why are you trying to kick me")
            else:
                try:
                    if ctx.author.top_role > user.top_role:
                        await user.kick(reason=reason)
                        if reason == None:
                            await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator} you better have a reason for this')
                        else:
                            await ctx.send(f"""{data["kick_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",reason)}""")
                except:
                    await ctx.send(f"{user.name}#{user.discriminator} has a higher role then me")


    @commands.slash_command(default_member_permissions= disnake.Permissions(ban_members = True),description = "Used to ban members")
    async def ban(ctx, user: disnake.User, reason:str=None):
        if data["ban_settings"]["ban"] == True:
            if user.id == ctx.guild.me.id:
                await ctx.send("why are you trying to ban me")
            else:
                try:
                    if ctx.author.top_role > user.top_role:
                        await user.ban(reason=reason)
                        if reason == None:
                            await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator} you better have a reason for this')
                        else:
                            await ctx.send(f"""{data["ban_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",reason)}""")
                except:
                    await ctx.send(f"{user.name}#{user.discriminator} has a higher role than me")


#!need to add unban

    @commands.slash_command(default_member_permissions=disnake.Permissions(manage_roles=True),description="Used to role members")
    async def role(ctx, user: disnake.User ,role: disnake.Role):
        if data["role_settings"]["role"] == True:
            if ctx.author.top_role > role and ctx.guild.me.top_role > role:
                if role in user.roles:
                    if data["unrole_settings"]["unrole"] == True:
                        try:
                            await user.remove_roles(role)
                            await ctx.send(f"""{data["unrole_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
                        except:
                            print(os.error())
                            try:
                                await user.remove_roles(disnake.utils.get(user.guild.roles, name=role))
                            except Exception as e:
                                # if error
                                await ctx.send('There was an error running this command ')
                            else:
                                await ctx.send(f"""{data["unrole_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
                    else:
                        await ctx.send(f"{user.name}#{user.discriminator} already has the role")
                else:
                    try:
                        await user.add_roles(role)
                        await ctx.send(f"""{data["role_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
                    except:
                        print(os.error())
                        try:
                            await user.add_roles(disnake.utils.get(user.guild.roles, name=role))
                        except Exception as e:
                            # if error
                            await ctx.send('There was an error running this command ')
                        else:
                            await ctx.send(f"""{data["role_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
            elif ctx.author.top_role <= role:
                await ctx.send("your role is not high enough to give that role")
            elif ctx.guild.me.top_role <= role:
                await ctx.send("my role is not high enough")
            else:
                await ctx.send("sorry there was an error while executing the command")


    @commands.slash_command(default_member_permissions=disnake.Permissions(manage_roles = True),description="Used to mute members")
    async def mute(ctx, user: disnake.User, time: str = "None", reason=None):
        timing = {"s": 1, "second": 1, "seconds": 1, "m": 60, "minute": 60, "minutes": 60,
                "h": 3600, "hour": 3600, "hours": 3600, "d": 86400, "day": 86400, "days": 86400}
        if data["mute_settings"]["mute"] == True:
            try:
                stc = Mute_roles[str(ctx.guild.id)]
                Mute_rol = (disnake.utils.get(user.guild.roles,
                            name=f"{Mute_roles[str(ctx.guild.id)]}"))
                if user.id == ctx.guild.me.id:
                    await ctx.send("why are you trying to mute me")
                else:
                    if ctx.author.top_role > user.top_role and ctx.guild.me.top_role > user.top_role:
                        if time != "None":
                            for t in timing.keys():
                                if t in time:
                                    try:
                                        time = int(time.replace(t, ""))
                                        await user.add_roles(Mute_rol)
                                        embed = disnake.Embed(title="Muted", color=color(), description=data["mute_settings"]["text"].replace(
                                            "[admin]", f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]", f"{user.name}#{user.discriminator}").replace("[reason]", f"{reason}"))
                                        await ctx.send(embed = embed) 
                                        await asyncio.sleep(timing[t]*time)
                                        await user.remove_roles(Mute_rol)
                                        break
                                    except:
                                        l = "no"
                        else:
                            l = "no"
                        try:
                            if l == "no":
                                if reason == None:
                                    await user.add_roles(Mute_rol)
                                    embed = disnake.Embed(title="Muted", color=color(), description=data["mute_settings"]["text"].replace(
                                        "[admin]", f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]", f"{user.name}#{user.discriminator}").replace("[reason]", f"{time}"))
                                    await ctx.send(embed = embed)
                                else:
                                    await user.add_roles(Mute_rol)
                                    embed = disnake.Embed(title="Muted", color=color(), description=data["mute_settings"]["text"].replace(
                                        "[admin]", f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]", f"{user.name}#{user.discriminator}").replace("[reason]", f"{time} {reason}"))
                                    await ctx.send(embed = embed)
                        except: 
                            return
                    elif ctx.author.top_role <= user.top_role:
                        embed = disnake.Embed(
                            title="Error", description=f":x: Your role is not high enough", color=color())
                        await ctx.send(embed=embed)
                    elif ctx.guild.me.top_role <= user.top_role:
                        embed = disnake.Embed(
                            title="Error", description=f":x: {user.name}#{user.discriminator} has a higher role than mine", color=color())
                        await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            title="Error", description=f":x: There was an error while executing the command", color=color())
                        await ctx.send(embed=embed)
            except KeyError as jsd:
                embed = disnake.Embed(
                    title="Error", description=f":x: couldnt find the Muted role pls set a Mute role using {prefi}mute_role", color=color())
                await ctx.send(embed=embed)


    @commands.slash_command(default_member_permissions= disnake.Permissions(manage_roles = True),description="Used to unmute members")
    async def unmute(ctx, user: disnake.User):
        Mute_rol = (disnake.utils.get(user.guild.roles,
                    name=f"{Mute_roles[str(ctx.guild.id)]}"))
        if data["unmute_settings"]["unmute"] == True:
            if ctx.author.top_role > user.top_role and ctx.guild.me.top_role > user.top_role:
                try:
                    await user.remove_roles(Mute_rol)
                    await ctx.send(f"""{data["unmute_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
                except:
                    await ctx.send(f'pls check if you have made the role Muted')
            elif ctx.author.top_role <= user.top_role:
                await ctx.send("your role is not hght enough")
            elif ctx.guild.me.top_role <= user.top_role:
                await ctx.send("my role is not high enough")
            else:
                await ctx.send("sorry there was an error while executing the command")


    @commands.slash_command(default_member_permissions = disnake.Permissions(manage_roles = True),description = "Used to add a mute role for the server")
    async def mute_role(ctx, role: disnake.Role):
        if data["mute_settings"]["mute"] == True:
            if str(ctx.guild.id) in Mute_roles.keys():
                del Mute_roles[str(ctx.guild.id)]
                Mute_roles[str(ctx.guild.id)] = f"{role}"
                with open("./storage/mute_role.json", "w") as mr:
                    json.dump(Mute_roles, mr, indent=4)
            else:
                Mute_roles[str(ctx.guild.id)] = f"{role}"
                with open("./storage/mute_role.json", "w") as mr:
                    json.dump(Mute_roles, mr, indent=4)
            await ctx.send(f"{role} has been set as the Mute role for this server")
            
def setup(client):
    client.add_cog(Moderation(client))