import random
import csv
import pandas as pd
from PIL import Image
from discord import File
import discord
from scripts import data_file as da
import datetime
import os

async def blackjack(data,amount):
    if not data.money_df.at[f"{data.user}","balance"] >= amount:
        await data.response.send_message(f"Get out of here broke boy you dont have enough to gamble {amount} dollas.")
        print(f"#######################\nBROKE IDIOT\n#######################")
        return
    data.money_df.at[f"{data.user}","balance"] -= amount
    data.money_df.to_csv(data.money_path,index=True)
    user_draws = [amount]
    while len(user_draws) <3:
        user_draws.append(random.randint(1,13))
    user1 = user_draws[1]
    user2 = user_draws[2]
    print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nFirst Two: {user1},{user2}\n#######################")
    userimg1 = Image.open(f"data/cards/{user1}/{random.randint(1,4)}.png")
    userimg2 = Image.open(f"data/cards/{user2}/{random.randint(1,4)}.png")
    user_send = Image.new('RGB', (userimg1.size[0] + userimg2.size[0], max(userimg1.size[1], userimg2.size[1])))
    user_send.paste(userimg1, (0, 0))
    user_send.paste(userimg2, (userimg1.size[0], 0))
    user_send.save(f"data/Images/{data.user}_user.png")
    file = File(f"data/Images/{data.user}_user.png")
    user_draws = [10 if x > 10 else x for x in user_draws]
    with open(f"data/temp_gamble/{data.user}.txt","w") as f:
        f.write(f"{str(user_draws[0])},{str(user_draws[1])},{str(user_draws[2])}")
    if sum(user_draws[1:]) == 21:
        data.server = True
        blackjack_winner(data)
    else:
        await data.response.send_message(content=f"{data.user}'s Hand: {sum(user_draws[1:])}",file=file, view=GamblingMan())

async def bust_da_nut(data):
    with open(f"data/temp_gamble/{data.user}.txt","r") as f:
            user_draws = [int(x) for x in f.read().split(",")]
    amount = user_draws[0]
    bal = data.money_df.at[f"{data.user}","balance"]
    if data.server == True:
        await data.message.send(f"User {data.user} lost {amount} dollas and now has {bal} dollas!! Why would you ever gamble?.")
    print(f"#######################\nLoser: lost {amount} dollas\n#######################")
    data.money_df.to_csv(data.money_path,index=True)
    os.remove(f"data/temp_gamble/{data.user}.txt")

async def blackjack_winner(data):
    with open(f"data/temp_gamble/{data.user}.txt","r") as f:
            user_draws = [int(x) for x in f.read().split(",")]
    amount = user_draws[0]
    data.money_df.at[f"{data.user}","balance"] += (amount*2)
    data.money_df.to_csv(data.money_path,index=True)
    bal = data.money_df.at[f"{data.user}","balance"]
    if data.server == True:
        await data.message.send(f"User {data.user} won {amount*2} dollas and now has {bal} dollas!! Gambling pays fellas.")
    print(f"#######################\nWinner: gained {amount*2} dollas\n#######################")
    os.remove(f"data/temp_gamble/{data.user}.txt")

class GamblingMan(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Hit', style=discord.ButtonStyle.blurple)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = da.Splicer.from_interaction(interaction)
        if os.path.isfile(f"data/temp_gamble/{data.user}.txt") == False:
            await data.response.send_message("you cannot play for another person.")
            print(f"#######################\n{data.user} tried to gamble for someone else\n#######################")
            return
        with open(f"data/temp_gamble/{data.user}.txt","r") as f:
            user_draws = [int(x) for x in f.read().split(",")]
        hit = random.randint(1,13)
        if hit > 10:
            hit = 10
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nHit: {hit}\n#######################")
        user_draws.append(hit)
        if sum(user_draws) + 10 < 22:
            user_draws = [11 if x == 1 else x for x in user_draws]
        with open(f"data/temp_gamble/{data.user}.txt","w") as f:
            f.write(str(user_draws[0]))
            aaa = user_draws[1:]
            for i in range(len(aaa)):
                f.write(f",{aaa[i]}")
        new = Image.open(f"data/cards/{hit}/{random.randint(1,4)}.png")
        old = Image.open(f"data/Images/{data.user}_user.png")
        ooh = Image.new('RGB', (old.size[0] + new.size[0], max(old.size[1], new.size[1])))
        ooh.paste(old, (0, 0))
        ooh.paste(new, (old.size[0], 0))
        ooh.save(f"data/Images/{data.user}_user.png")
        file = File(f"data/Images/{data.user}_user.png")
        if sum(user_draws[1:]) > 21:
            data.server = True
            file = File(f"data/Images/{data.user}_user.png")
            await interaction.response.edit_message(content=f"{data.user}'s Hand: {sum(user_draws[1:])}",attachments=[file], view=None)
            await bust_da_nut(data)
        else:
            await interaction.response.edit_message(content=f"{data.user}'s Hand: {sum(user_draws[1:])}",attachments=[file])       

    @discord.ui.button(label='Stand', style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = da.Splicer.from_interaction(interaction)
        if os.path.isfile(f"data/temp_gamble/{data.user}.txt") == False:
            await data.response.send_message("you cannot play for another person.")
            print(f"#######################\n{data.user} tried to gamble for someone else\n#######################")
            return
        with open(f"data/temp_gamble/{data.user}.txt","r") as f:
            user_draws = [int(x) for x in f.read().split(",")]
        file = File(f"data/Images/{data.user}_user.png")
        user_total = sum(user_draws[1:])        
        dealer_total = 0
        while dealer_total < 17:
            dealer_total += random.randint(1,10)
        if dealer_total > user_total and dealer_total <22:
            await interaction.response.edit_message(content=f"{data.user}'s Hand: {sum(user_draws[1:])}",attachments=[file], view=None)
            await data.message.send(f'Dealer had {dealer_total}, {data.user} lost {user_draws[0]} dollas!')
            await bust_da_nut(data)
        if user_total > dealer_total and user_total <22:
            await interaction.response.edit_message(content=f"{data.user}'s Hand: {sum(user_draws[1:])}",attachments=[file], view=None)          
            await data.message.send(f'Dealer had {dealer_total}, {data.user} won {user_draws[0]*2} dollas!')
            await blackjack_winner(data)
        if dealer_total == user_total:
            await interaction.response.edit_message(content=f"{data.user}'s Hand: {sum(user_draws[1:])}",attachments=[file], view=None)
            await data.message.send("Tie")
            data.money_df.at[f"{data.user}","balance"] += (amount*2)
            data.money_df.to_csv(data.money_path,index=True)
            os.remove(f"data/temp_gamble/{data.user}.txt")
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nStand\n#######################")

