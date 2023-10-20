import pandas as pd
import csv
import os
import random

async def correct_answer(data):
	return

def answer_gen():
	num_plus_num = [f"{random.randint(50, 864)}",f"{random.randint(0, 14320)}"]
	answer = int(num_plus_num[0]) + int(num_plus_num[1])
	print(num_plus_num)
	print(answer)


answer_gen()