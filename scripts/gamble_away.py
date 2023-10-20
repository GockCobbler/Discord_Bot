import random
import csv
import pandas as pd

def gamble_result(choice):
    if choice == random.randint(0,10):
        return True
    else:
        return False

def broked_boy(data,amount):
    if data.money_df.at[f"{data.user}","balance"] >= amount:
        return False
    else:
        return True

async def gamble(data,amount, choice):
    broke_boy = broked_boy(data,amount)
    if not broke_boy: 
        result = gamble_result(choice)
        if result:
            data.money_df.at[f"{data.user}","balance"] += (amount*2)
            bal = data.money_df.at[f"{data.user}","balance"]
            await data.response.send_message(f"User {data.user} won {amount*2} dollas and now has {bal} dollas!! Gambling pays fellas.")
            print(f"Winner: gained {amount*2} dollas\n#######################")
        else:
            data.money_df.at[f"{data.user}","balance"] -= amount
            bal = data.money_df.at[f"{data.user}","balance"]
            await data.response.send_message(f"User {data.user} lost {amount} dollas and now has {bal} dollas!! Why would you ever gamble?.")
            print(f"Loser: lost {amount} dollas\n#######################")
    else:
        bal = data.money_df.at[f"{data.user}","balance"]
        await data.response.send_message(f"You're too broke to gamble {amount} dollas, you only have {bal} dollas.", ephemeral=True)
        print("BROKE IDIOT\n#######################")
    data.money_df.to_csv(data.money_path,index=True)