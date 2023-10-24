import aiohttp
import asyncio
import os
from PIL import Image
import numpy
import io
import discord
import datetime
import config
import requests

async def convert_prompt(shitty_prompt):
    cbearer = config.keys()["GPT_BEARER"]
    curl = 'https://api.openai.com/v1/chat/completions'
    csystem_msg = "Your task is to take the following and format it for a Stable Diffusion text-to-image ai. your output prompt should include only descriptive words and styles, this must be in one line, do not use the words description or style, you are to add descriptive imagry words and imagry styles based off what might be in the descirbed prompt. the output prompt must not contain anything other than the final output to text-to-image. your output must not exceed 30 words. do not use the word prompt. If a name is said make sure that name goes in the output"
    cheaders = {'Authorization': f'Bearer {cbearer}','Content-Type':'application/json'}
    cjson = {'messages': [{"role": "system", "content": csystem_msg},{"role": "user", "content": f"{shitty_prompt}"}],'model': "gpt-3.5-turbo"}
    async with aiohttp.ClientSession() as session:
        async with session.post(curl, headers=cheaders, json=cjson) as resp:
            cresponse = await resp.json()
    try:
        prompt = cresponse["choices"][0]["message"]["content"]
        print(f"#######################\nNew Prompt: {prompt}\n#######################")
    except:
        prompt = shitty_prompt
    return prompt

async def generate_image(data,shitty_prompt):
    try:
        prompt = await convert_prompt(shitty_prompt)
        configs = config.keys()
        bearer = configs["IMAGE_BEARER"]
        url = configs["IMAGE_URL"] 
        headers = {"Accept": "image/png","Authorization": f"Bearer {bearer}","Content-Type": "application/json"}
        json = {'inputs': f"{prompt}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as resp:
                image_bytes = await resp.read()
        image = Image.open(io.BytesIO(image_bytes))
        image.save("data/Images/image.png")
        await data.message.send(f"Prompt: {shitty_prompt}\n AI Editted prompt: {prompt}",file=discord.File(r'data/Images/image.png'))
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nResponse: Image sent successfully\n#######################")
    except:
        await data.message.send("AI booting up, please wait. This usually takes 5-15mins.", ephemeral=True)
        print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nResponse: AI booting up, please wait. This usually takes 5-10mins.\n#######################")

'''
THIS IS TO SEE WHERE ERRORS ARE WHEN USING NEW API URL

async def generate_image(data,prompt):
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
    '''
