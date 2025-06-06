import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

DISCORD_TOKEN=MTM4MDM1MTE5Njc2MTQyMzk4Mw.Gfbmli.TrcaXIJnnrNvhmG4YaYcj7oUFnO3zvMXbFi8KA
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def cgstart(ctx):
    # Изпраща embed
    embed = discord.Embed(title="Custom Game Queue", description="Реагирай с ✅ за участие!\nПървите 10 ще играят.", color=0x00ff00)
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")

    def check(reaction, user):
        return str(reaction.emoji) == "✅" and reaction.message.id == message.id and not user.bot

    participants = []

    try:
        while len(participants) < 10:
            reaction, user = await bot.wait_for('reaction_add', timeout=300.0, check=check)
            if user not in participants:
                participants.append(user)
                print(f"{user} се присъедини ({len(participants)}/10)")
    except asyncio.TimeoutError:
        await ctx.send("Времето изтече, не се събраха 10 участника.")
        return

    # Разделяме на отбори
    random.shuffle(participants)
    team1 = participants[:5]
    team2 = participants[5:]

    # Имена на гласовите канали
    vc1 = discord.utils.get(ctx.guild.voice_channels, name="Канал 1")
    vc2 = discord.utils.get(ctx.guild.voice_channels, name="Канал 2")

    if not vc1 or not vc2:
        await ctx.send("Не можах да намеря гласовите канали 'Канал 1' и 'Канал 2'.")
        return

    # Преместване на участниците
    for member in team1:
        if member.voice:
            await member.move_to(vc1)

    for member in team2:
        if member.voice:
            await member.move_to(vc2)

    await ctx.send("Играчите бяха разделени на отбори и преместени!")
bot.run(DISCORD_TOKEN)