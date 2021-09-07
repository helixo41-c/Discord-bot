import discord
from discord.ext import commands
import datetime
import youtube_dl
from discord.utils import get
import os

client = commands.Bot( command_prefix = '$' )

# Words

# Connection
@client.event
async def on_ready():
    print( "CONNECTED!" )

# Message

# $$$:::COMMANDS FOR ALL USERS:::$$$

# ::: Voice channel :::
# ::: Play music

@client.command()
async def play_music( ctx, url : str ):
	song_there = os.path.isfile('song.mp3')

	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Old file deleted')
	except PermissionError:
		print("[log] File don't deleted")
	await ctx.send('Wait...')

	voice = get( client.voice_clients, guild = ctx.guild )

	ydl_opts = {
		'format' : 'bestaudio/best',
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}]
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("[log] Dowloading music...")
		ydl.download([url])

	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			name = file
			print("[log] Renaming file: {file}")
			os.rename(file, 'song.mp3')

	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, Music end'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	song_name = name.rsplit("-", 2)
	await ctx.send(f'playing music: {song_name[0]}')

# ::: Join

@client.command()
async def vcjoin( ctx ):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.move_to( channel )
	else:
		voice = await channel.connect()
		await ctx.send(f'Bot CONNECTED to a channel: {channel}')

# ::: Leave

@client.command()
async def vcleave( ctx ):
	channel = ctx.message.author.voice.channel
	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()
		await ctx.send(f'Bot DISCONNECTED from channel: {channel}')

# ::: Voice Channel end

# :::Help
@client.command( pass_context = True )
async def help_me( ctx ):

    emb = discord.Embed( title = 'Навигация по командам' )

    emb.add_field( name = '$help_me', value = 'Выводит это сообщение;' )
    emb.add_field( name = '$vcjoin', value = 'Подключить к голосовому чату;' )
    emb.add_field( name = '$vcleave', value = 'Отключить от голосового чата;' )
    emb.add_field( name = '$play_music [url from youtube]:', value = 'Воспроизвести песню из Ютуба' )
    emb.add_field( name = 'commands for administrator', value = '------------------------' )
    emb.add_field( name = '$clear_chat [number of messages]:', value = 'Очистка чата;' )
    emb.add_field( name = '$kick [user nick and ID]:', value = 'Выгнaть участника;' )
    emb.add_field( name = '$ban [user nick and ID]:', value = 'Бан участника;' )
    emb.add_field( name = '$add_game [game name]:', value = 'Добавление игры в список играемых;' )
    emb.add_field( name = '$del_game [game name]:', value = 'Удаление из списка играемых;' )
    await ctx.send( embed = emb )

# :::Time
@client.command( pass_context = True )
async def time( ctx ):

    now_date = datetime.datetime.now()

    await ctx.send( f'TIME is --> {now_date}' )


# $$$:::COMMANDS FOR ADMIN:::$$$

# :::Clear chat
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear_chat( ctx, amount = 100 ):
    await ctx.channel.purge( limit = amount )

# :::Kick
@client.command( pass_content = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason )
    await ctx.send( f'kick user { member.mention }' )

# :::Ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.ban( reason = reason )
    await ctx.send( f'ban user { member.mention }' )

#connect
token = open( 'token.txt', 'r' ).readline()

client.run( token )