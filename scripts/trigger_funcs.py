import os
import pandas as pd
import csv
from dataclasses import dataclass
import asyncio
import datetime

async def check_list(data):
	triggered_already = []
	for b in data.words_said:
		if b in data.trigger_list and b not in triggered_already:
			triggered_already.append(b)
			await trigger_said(data, b)
			
async def trigger_edit(data,action,word):
	if action == "list":
		await data.response.send_message(f"Current triggers: {data.trigger_list}", ephemeral=True)
		print(f"Response: Current triggers: {data.trigger_list}\n#######################")

	if action == "add":
		if not word in data.trigger_df.columns:
			data.trigger_df[f"{word}"] = "0"
			data.trigger_df.to_csv(data.trigger_path, index=True)
			await data.response.send_message(f"The word -{word}- now triggers a reply.", ephemeral=True)
			print(f"Response: The word -{word}- now triggers a reply.\n#######################")	
		else:
			await data.response.send_message(f"The word -{word}- already triggers a reply.", ephemeral=True)
			print(f"Response: The word -{word}- already triggers a reply.\n#######################")
			
	
	if action == "del":
		if word in data.trigger_df.columns:
			data.trigger_df.drop(columns=word,inplace=True)
			data.trigger_df.to_csv(data.trigger_path, index=True)
			await data.response.send_message(f"The word -{word}- no longer triggers a reply.", ephemeral=True)
			print(f"The word -{word}- no longer triggers a reply.\n#######################")
		else:
			await data.response.send_message(f"The word -{word}- didn't trigger a reply in the first place.", ephemeral=True)
			print(f"The word -{word}- didn't trigger a reply in the first place.\n#######################")
			

async def trigger_said(data, word):
	if not f"{data.user}" in data.trigger_df.index:
		add_user(data)
		data.trigger_df = pd.read_csv(data.trigger_path, index_col="username")
	said_count = 0
	bitch = word
	for a in data.words_said:
		if bitch in a:
			said_count += 1
	count = data.trigger_df[word][f"{data.user}"] + said_count
	data.trigger_df.at[f"{data.user}",f"{word}"] = count
	data.trigger_df.to_csv(data.trigger_path,index=True)
	await data.response.typing()
	await data.response.send(f"{data.user} has said -{word}- {count} times")
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nTrigger Said\nServer: {data.server}\nUser: {data.user}\nWord: {word}\nNew count: {count}\n#######################")
	
def add_user(data):
	df = data.trigger_df.reset_index()
	df = df._append(pd.Series(0, index=df.columns), ignore_index=True)
	df.loc[(len(df) - 1),"username"] = data.user
	data.trigger_df = df.set_index("username")
	data.trigger_df.to_csv(data.trigger_path,index=True)
	print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser addded to trigger_df\nDataframe: {data.trigger_path}\nUser: {data.user}\n#######################")
