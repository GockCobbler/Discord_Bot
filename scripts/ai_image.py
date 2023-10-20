import aiohttp
import asyncio
import os
from PIL import Image
import numpy
import io
import discord
import datetime
import config

async def generate_image(data,prompt):
    try:
        config = config.keys()
        bearer = config["IMAGE_BEARER"]
        url = config["IMAGE_URL"]
        headers = {"Accept": "image/png","Authorization": f"Bearer {bearer}","Content-Type": "application/json"}
        json = {'inputs': f"{prompt}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as resp:
                image_bytes = await resp.read()
        image = Image.open(io.BytesIO(image_bytes))
        image.save("data/Images/image.png")
        await data.message.send(f"Prompt: {prompt}",file=discord.File(r'data/Images/image.png'))
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nResponse: Image sent successfully\n#######################")
    except:
        await data.message.send("AI booting up, please wait. This usually takes 5-15mins.", ephemeral=True)
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nResponse: AI booting up, please wait. This usually takes 5-10mins.\n#######################")

'''
async def generate_image(data,prompt):    
    bearer = config.keys()["IMAGE_BEARER"]
    url = 'https://eyus07jw9vhhdh6o.us-east-1.aws.endpoints.huggingface.cloud'
    headers = {"Accept": "image/png","Authorization": f"Bearer {bearer}","Content-Type": "application/json"}
    json = {'inputs': f"{prompt}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json) as resp:
            print(resp)
            image_bytes = await resp.read()
    image = Image.open(io.BytesIO(image_bytes))
    image.save("data/Images/image.png")
    '''