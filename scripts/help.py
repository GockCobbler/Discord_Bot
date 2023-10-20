import discord

async def help(data):
	embed = discord.Embed(title="How to use and abuse me",description="You earn dollas randomly by using text chat anywhere in the server.\nRight click on a user to check their balance or mute them for 1 minute.\nMuting a user costs 5 dollas and only works in voice chat.")
	embed.add_field(name="/trigger [add/del/list] [word]",value="This will make me keep track and report how many times each user says the word, or will stop a word from being tracked.",inline=False)
	embed.add_field(name="/image [prompt]",value="This will use AI to generate and send an image based on your prompt. The AI shuts down after 15 mins of inactivity and can be booted by using /image. Boot usually takes 5-10mins.",inline=False)
	embed.add_field(name="/chat [prompt]",value="This will let you talk to chat GPT. At this moment is has no context memory",inline=False)
	embed.add_field(name="/gamble [dollas] [prediction]",value="This lets you gamble dollas. Choose and amount to gamble and a prediction between 1 and 10. If you win you double your gamble.",inline=False)
	await data.response.send_message(embed=embed)
	print(f"Response: Help message sent.\n#######################")