from dataclasses import dataclass
import pandas as pd
import os
import csv
from scripts import word_tally

@dataclass
class Splicer:

	def __init__(self, user, response, server, content):
		self.user = user
		self.message = content
		self.response = response
		self.words_said = str(self.message).lower().split()
		self.server = server
		self.money_path = f"data/money/{server}.csv"
		if not os.path.isfile(self.money_path):
			df = pd.read_csv("data/money_template.csv", index_col="user")
			df.to_csv(self.money_path, index=True)
		self.money_df = pd.read_csv(self.money_path, index_col="user")
		self.trigger_path =  f"data/trigger_lists/{server}.csv"
		if not os.path.isfile(self.trigger_path):
			df = pd.read_csv("data/trigger_pd_template.csv", index_col="username")
			df.to_csv(self.trigger_path, index=True)
		self.trigger_df = pd.read_csv(self.trigger_path, index_col="username")
		self.trigger_list = self.trigger_df.columns.tolist()
		self.milestones = {1000: f"{user} has said 1000 words!!",5000: f"{user} has said 5000 words!!",10000: f"{user} has said 10000 words!!",100000: f"Holy fucking shit {user} has said 100000 words... get a life man"}
		self.tally_path = "data/word_tally.csv"
		self.tally_df = pd.read_csv("data/word_tally.csv", index_col="username")
		if not str(self.user) in self.tally_df.index:
			word_tally.add_user(self)
			self.tally_df = pd.read_csv("data/word_tally.csv", index_col="username")
		self.count = self.tally_df["word_total"][f"{user}"]
		self.said_count = len(self.words_said)

	@classmethod
	def from_interaction(cls, interaction):
		return cls(interaction.user, interaction.response, interaction.guild, interaction.followup)

	@classmethod
	def from_message(cls, message):
		return cls(message.author, message.channel, message.guild, message.content)
