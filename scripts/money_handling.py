import pandas as pd
import csv
import os
import asyncio
import datetime

def add_user(data):
    df = data.money_df.reset_index()
    df = df._append(pd.Series(0, index=df.columns), ignore_index=True)
    df.loc[(len(df) - 1),"user"] = str(data.user)
    data.money_df = df.set_index("user")
    data.money_df.to_csv(data.money_path,index=True)

async def get_one_dolla(data):
    if not f"{data.user}" in data.money_df.index:
        add_user(data)
    bal = data.money_df["balance"][f"{data.user}"]
    data.money_df.at[f"{data.user}","balance"] = bal + 1
    data.money_df.to_csv(data.money_path,index=True)
    if bal + 1 <= 1:
        await data.response.send(f"User: {data.user} has gained one dolla!\nThey now have {bal +1} dolla")
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser {data.user} has gained one dolla\nNew bal: {bal + 1}\n#######################")
    else:
        await data.response.send(f"User: {data.user} has gained one dolla!\nThey now have {bal +1} dollas")
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser {data.user} has gained one dolla\nNew bal: {bal + 1}\n#######################")


async def mute_for_five(data, member):
    bal = data.money_df["balance"][f"{data.user}"]
    try:
        if bal >= 5:
            await member.edit(mute=True)
            await data.response.send_message(f"User {member} has been muted by {data.user}")
            bal -= 5
            data.money_df.at[f"{data.user}","balance"] = bal
            data.money_df.to_csv(data.money_path,index=True)
            print(f"Response: User {member} has been muted by {data.user}\nNew bal: {bal}\n#######################")
            await asyncio.sleep(60)
            await member.edit(mute=False)
            print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser {member} has been un-muted\n#######################")
        else:
            await data.response.send_message(f"You only have {bal} dollas out of the required 5 dollas to mute someone", ephemeral=True)
            print(f"Response: You only have {bal} dollas out of the required 5 dollas to mute someone\n#######################")
    except:
        await data.response.send_message(f"User {member} is not currently connected to voice.", ephemeral=True)
        print(f"Time: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nResponse: User {member} is not currently connected to voice.\n#######################")

async def check_user_bal(data, member):
    try:
        bal = data.money_df["balance"][f"{member}"]
    except:
        await data.response.send_message(f"{member} has no money.", ephemeral=True)
        print(f"Response: {member} has no money.\n#######################")
        return
    await data.response.send_message(f"{member} has {bal} dollas", ephemeral=True)
    print(f"Response: {member} has {bal} dollas\n#######################")
