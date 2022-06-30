import discord, asyncio, os
import random
from discord.ext import commands
from datetime import *

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
    team1.sort()
    team2.sort()
    await ctx.send(f"1팀\n||{team1}||")
    await ctx.send(f"2팀\n||{team2}||")

@bot.command(aliases=["헬프"])
async def 도움(ctx):
    embed = discord.Embed(title="칼바람", description="by Korus 문제 있을 시 간부에게",color=0xFFFF00)
    embed.add_field(name="챔피언 뽑기",value="!roll [인원X3]",inline=False)
    embed.add_field(name="등록 챔피언 확인",value="!who \n *업데이트 안되어 있으면 간부한테 말해주세요*",inline=False)
    embed.add_field(name="팀 자동 배정",value="!teamnow\n 현재 채널의 인원으로 팀을 나눕니다.",inline=False)
    embed.add_field(name="팀 수동 배정",value="!team [A,B,C....]\n 명령어 뒤에 적은 인원들로 팀을 나눕니다.",inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx,*,str):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages:
            cham.append(str)
            file = open("champion_list.txt",'w',encoding='cp949')
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
            file = open("champion_list.txt",'w',encoding='cp949')
            file.writelines('\n'.join(cham))
            file.close()
            await ctx.send(f"{str} 삭제")
        else:
            await ctx.send("권한이 없습니다. 간부에게 문의하세요")

@bot.command()
async def team(ctx,str):
    people = str.split(",")
    random.shuffle(people)
    team1 = people[:int(len(people)/2)]
    team2 = people[int(len(people)/2):]
    await ctx.send(f'{team1}')
    await ctx.send(f'{team2}')
    
@bot.command()
async def teamnow(ctx):
    cnt = len(ctx.message.author.voice.channel.members)
    member_info = str(ctx.message.author.voice.channel.members).split("'")
    member = []
    for i in range(cnt):
        i = i*8+5
        member.append(member_info[i])
    
    random.shuffle(member)
    team1 = member[:int(cnt/2)]
    team2 = member[int(cnt/2):]
    
    await ctx.send(f"1팀 {team1}")
    await ctx.send(f"2팀 {team2}")

@bot.command(aliases=["ㅊㅊ","출첵","출근"])
async def 출석(ctx):
    now = datetime.now()
    user = ctx.message.author
    ymd = now.date()
    hour = now.hour
    minutes = now.minute
    attenddict[user] = now

    await ctx.send(f"{user}님 출근 {ymd} {hour}시 {minutes}분")

@bot.command(aliases=["ㅌㅌ","퇴근"])
async def 튀튀(ctx):
    now = datetime.now()
    user = ctx.message.author
    ymd = now.date()
    hour = now.hour
    minutes = now.minute

    duration = now - attenddict[user]
    

    del attenddict[user]
    await ctx.send(f"{user}님 퇴근 {ymd} {hour}시 {minutes}분\n {duration}만큼 하셨습니다.")



access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)  #봇의 토큰값
