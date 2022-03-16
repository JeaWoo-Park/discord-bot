import discord, asyncio, os
import random
from discord.ext import commands

game = discord.Game("칼바람")
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game)

file = open("champion_list.txt",'r')
cham = file.read().splitlines()
file.close()




@bot.command()
async def who(ctx):
    await ctx.send(cham)



@bot.command()
async def roll(ctx, num:int):
    randcham = random.sample(cham,num*2)
    team1 = randcham[:num]
    team2 = randcham[num:]
    await ctx.send(f"1팀\n||{team1}||")
    await ctx.send(f"2팀\n||{team2}||")

@bot.command(aliases=["헬프"])
async def 도움(ctx):
    embed = discord.Embed(title="칼바람", description="by Korus 문제 있을 시 간부에게",color=0xFFFF00)
    embed.add_field(name="챔피언 뽑기",value="!roll [인원X3]",inline=False)
    embed.add_field(name="등록 챔피언 확인",value="!who \n *업데이트 안되어 있으면 간부한테 말해주세요*",inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx,*,str):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages:
            cham.append(str)
            file = open("champion_list.txt",'w')
            file.writelines('\n'.join(cham))
            file.close()
            await ctx.send(f"{str} 추가")
        else:
            await ctx.send("권한이 없습니다. 간부에게 문의하세요")

@bot.command()
async def remove(ctx,*,str):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages:
            cham.remove(str)
            file = open("champion_list.txt",'w')
            file.writelines('\n'.join(cham))
            file.close()
            await ctx.send(f"{str} 삭제")
        else:
            await ctx.send("권한이 없습니다. 간부에게 문의하세요")

@bot.command()
async def team(ctx,str):
    people = str.split(",")
    team1 = people[:int(len(people)/2)]
    team2 = people[int(len(people)/2):]
    await ctx.send(f'{team1}')
    await ctx.send(f'{team2}')
    
@bot.command()
async def teamnow(ctx):
    
    #member = ctx.channel.name
    print(ctx.author.voice)
    cnt = len(ctx.message.author.voice.channel.members)
    member_info = str(ctx.message.author.voice.channel.members).split("'")
    member = []
    for i in range(cnt):
        member.append(member_info[i*8+5])
    
    random.shuffle(member)
    team1 = member[:int(cnt/2)]
    team2 = member[int(cnt/2):]
    
    await ctx.send(f"1팀 {team1}")
    await ctx.send(f"2팀 {team2}")

access_token = os.environ["BOT_TOKEN"]
bot.run('OTUzMzI2NDEyNTAzMzIyNzE0.YjC8aA.EjkQzd-eUrC4hrqWplEYexGUhes')  #봇의 토큰값
