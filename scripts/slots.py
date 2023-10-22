import random
import discord
from collections import Counter
import asyncio


async def slot_rolls(data,amount):
	if not data.money_df.at[f"{data.user}","balance"] >= amount:
		await data.response.send_message(f"Get out of here broke boy you dont have enough to gamble {amount} dollas.")
		print(f"#######################\nBROKE IDIOT\n#######################")
		return
	data.money_df.at[f"{data.user}","balance"] -= amount
	data.money_df.to_csv(data.money_path,index=True)
	rolls= []
	message = "Rolls: "
	await data.response.send_message(message)
	while len(rolls) < 7:
		roll = random.randint(1,15)
		rolls.append(roll)
		message = message + f" -{roll}-"
		await data.interaction.edit_original_response(content=message)
		await asyncio.sleep(1)
	counter = Counter(rolls)
	win_amount = max(counter.values())
	if win_amount >= 1:
		data.money_df.at[f"{data.user}","balance"] += (amount*win_amount)
		data.money_df.to_csv(data.money_path,index=True)
		bal = data.money_df.at[f"{data.user}","balance"]
		await data.message.send(f"User {data.user} won {amount} x {win_amount} dollas and now has {bal} dollas!! Gambling pays fellas.")
		print(f"#######################\nWinner: won {amount} dollas\n#######################") 
	else:
		data.money_df.to_csv(data.money_path,index=True)
		bal = data.money_df.at[f"{data.user}","balance"]
		await data.message.send(f"User {data.user} lost {amount} dollas and now has {bal} dollas!! Why would you ever gamble?.")
		print(f"#######################\nLoser: lost {amount} dollas\n#######################")   	


