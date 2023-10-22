import discord
import asyncio
import typing
import random as r
import config
from typing import Optional
from typing import Literal
from discord import app_commands
from scripts import *
from scripts import data_file as da
import datetime

config = config.keys()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(client)

async def sync_tree():
	await tree.sync() 
	print("Commands have been globaly synced.")

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game("with them toes"))
	print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
	if message.content == "fgshnswtsdgrs7986f9gaoihgaljkf4l3h908wgsdf83":
		await sync_tree()
	if not message.author == client.user:
		data = da.Splicer.from_message(message)
		if r.randint(0,16) == r.randint(0,16):
			await money_handling.get_one_dolla(data)
		await trigger_funcs.check_list(data)
		word_tally.tally(data)
		return

@tree.command(name = "about", description = "helpful info")
async def helper(interaction):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: help")
	await help.help(data)

@tree.command(name = "trigger", description = "Edit the current trigger words.")
@app_commands.rename(one="action",two="word")
@app_commands.describe(one="Add or Delete trigger word",two="Word to add or delete")
async def trigger_add_del(interaction,one: Literal["add","del","list"],two: Optional[app_commands.Range[str, 0, None]]):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: trigger_add_del")
	await trigger_funcs.trigger_edit(data,one,two)

@tree.command(name="image", description="Generate an AI image based on your prompt")
@app_commands.rename(one="prompt")
@app_commands.describe(one="Prompt you want to generate an image based off of")
async def ai_image_get(interaction,one:str):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: ai_image_get\nPrompt: {one}\n#######################")
	await data.response.send_message("Image is generating. This may take up to 10 minutes depending on file size and number of concurrent requests.", ephemeral=True)
	await ai_image.generate_image(data,one)

@tree.command(name="chat", description="Talk to chat GPT")
@app_commands.rename(one="prompt")
@app_commands.describe(one="Prompt you want to send")
async def chat_bot_ai(interaction,one:str):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: chat_bot_ai\nPrompt: {one}\n#######################")
	await data.response.send_message("generating response...", ephemeral=True)
	await chat_ai.chat_bot(data,one)

@tree.command(name="elongate", description="looooooooooooooooooooooooooong")
@app_commands.rename(one="message")
@app_commands.describe(one="make this message looooooooooooooooong, or is it tall?")
async def longgggg(interaction,one: str):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: longgggg\nPrompt: {one}\n#######################")
	await elongate.looooong(interaction,one)

@tree.command(name="blackjack", description="Gamble away your life savings... Or get rich")
@app_commands.rename(amount="dollas")
@app_commands.describe(amount="# of dollas to gamble")
async def black_jack(interaction,amount: int):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: black_jack\nAmount: {amount}\n#######################")
	await gamble_away.blackjack(data,amount)

@tree.command(name="slots", description="Gamble away your life savings... Or get rich")
@app_commands.rename(amount="dollas")
@app_commands.describe(amount="# of dollas to gamble")
async def slotts(interaction,amount: int):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: slots\nAmount: {amount}\n#######################")
	await slots.slot_rolls(data,amount)

@tree.context_menu(name="mute this foo for 5 dollas")
async def mute_for_money(interaction: discord.Interaction, target: discord.Member):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: Mute\nTarget: {target}")
	await money_handling.mute_for_five(data,target)

@tree.context_menu(name="Balance")
async def balance_check(interaction: discord.Interaction, target: discord.Member):
	data = da.Splicer.from_interaction(interaction)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nServer: {data.server}\nCommand: Balance interact\nTarget: {target}")
	await money_handling.check_user_bal(data,target)

#BUTTONS
'''
class GamblingMan(discord.ui.View):

	def __init__(self):
		super().__init__()

	@discord.ui.button(label='Hit', style=discord.ButtonStyle.green)
	async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message('Hit', ephemeral=True)

	@discord.ui.button(label='Stand', style=discord.ButtonStyle.green)
	async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message('Stand', ephemeral=True)
'''

client.run(config["DISCORD_BOT_TOKEN"])
