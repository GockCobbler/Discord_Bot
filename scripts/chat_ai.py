import aiohttp
import asyncio
import discord
import datetime
import config

async def chat_bot(data, prompt):
    bearer = config.keys()["GPT_BEARER"]
    url = 'https://api.openai.com/v1/chat/completions'
    system_msg = "you will respond with factually correct information when possible. you are also a psychopathic serial killer who is always as rude as possible. You like responding snappy and consice. Responses must be under 2000 characters."
    headers = {'Authorization': f'Bearer {bearer}','Content-Type':'application/json'}
    json = {'messages': [{"role": "system", "content": system_msg},{"role": "user", "content": f"{prompt}"}],'model': "gpt-4"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json) as resp:
            response = await resp.json()
            try:
                message = response["choices"][0]["message"]["content"]
                await data.message.send(f"User: {data.user}\nPrompt: {prompt}\nResponse:\n{message}")
                print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nPrompt: {prompt}\nResponse: {message}\n#######################")
            except:
                await data.message.send("GPT is currently down, try again later.",ephemeral=True)
                print(f"#######################\nTime: {datetime.datetime.now().strftime('%I:%M:%S %p')}\nUser: {data.user}\nPrompt: {prompt}\nResponse: Error\n#######################")