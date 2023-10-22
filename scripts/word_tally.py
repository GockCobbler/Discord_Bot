import os
import pandas as pd
import csv
from dataclasses import dataclass
from scripts import trigger_funcs as tf

def tally(data):
	if not f"{data.user}" in data.tally_df.index:
		add_user(data)
	data.tally_df.at[f"{data.user}","word_total"] += data.said_count
	data.tally_df.to_csv("data/word_tally.csv",index=True)
	milestone(data)

def milestone(data):
	count = data.tally_df["word_total"][f"{data.user}"]
	if count >= 1000:
		rounded = round(count, -3)
	else:
		rounded = count
	if rounded in data.milestones:
		has_milestone = data.tally_df[f"{rounded}"][f"{data.user}"]
		if has_milestone == 0:
			send_mile(data.milestones[rounded])
			data.tally_df.at[f"{data.user}",f"{rounded}"] = 1
			data.tally_df.to_csv("data/word_tally.csv",index=True)

async def send_mile(mile):
	await data.response.send_message(mile)

def add_user(data):
	df = data.tally_df.reset_index()
	df = df._append(pd.Series(0, index=df.columns), ignore_index=True)
	df.loc[(len(df) - 1),"username"] = str(data.user)
	data.tally_df = df.set_index("username")
	data.tally_df.to_csv(data.tally_path,index=True)
