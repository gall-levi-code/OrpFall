import os
import discord
import requests

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
URL = os.getenv('DISCORD_WEBHOOK')

client = discord.Client()

TESTERS = [108062945740640256, 219093637986779138, 108072654577152000, 410506804859109376]
ROLES = [672561758023450675, 672561940895105038]
SELECTION = {}
CHARACTERS = {
    1: {
        "username": "Dragon 1",
        "avatar_url": "https://res.cloudinary.com/teepublic/image/private/s--g2ftYnyD--/t_Resized%20Artwork/c_fit,g_north_west,h_954,w_954/co_262c3a,e_outline:48/co_262c3a,e_outline:inner_fill:48/co_ffffff,e_outline:48/co_ffffff,e_outline:inner_fill:48/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_jpg,h_630,q_90,w_630/v1529161246/production/designs/2793128_0.jpg",
        "tts": True,
    },
    2: {
        "username": "Dragon 2",
        "avatar_url": "https://i.imgur.com/57zxQLU.png",
        "tts": True,
    }
}

TEST_CHANNEL = 672555080456732695
OUTPUT_CHANNEL = 672554869529378826

COLORS = {1: "RED", 2: "BLUE", 3: "GREEN", 4: "YELLOW", 5: "ORANGE", 6: "BROWN", 7: "PURPLE", 8: "GREY", 9: "BLACK",
          10: "WHITE"}

COLORS_RGB = {

}


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    for each in guild.roles:
        members = ""
        for name in each.members:
            members += name.name + " "
        print(f'{each} has the following members: {members}')


def has_permissions(userguild, user):
    guild = discord.utils.get(userguild, name=GUILD)

    roles = guild.roles
    for role in roles:
        if role.id in ROLES:
            if user in role.members:
                return True
    return False


def post(url, data, content):
    data.update({"content": content})
    r = requests.post(url=url, data=data)
    print(r.text)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    author_id = message.author.id
    author_mention = message.author.mention
    channel_id = message.channel.id
    send_channel = client.get_channel(OUTPUT_CHANNEL)
    content = message.content

    if message.content == "!clear":
        await message.channel.purge()
        return
    elif message.content.find("!select") == 0:
        values = message.content.split()
        if len(values) > 2:
            await message.channel.send("Too many values, please enter only 1.")
        elif len(values) == 1:
            try:
                del SELECTION[author_id]
                await message.channel.send("Clearing your current selection.")
            except KeyError:
                await message.channel.send("Your selection was already empty.")
        else:
            if int(values[1]) in CHARACTERS:
                SELECTION.update({author_id: int(values[1])})
                await message.channel.send(f"You've now set your selection to {str(SELECTION[author_id])}, {CHARACTERS[SELECTION[author_id]]['username']}\nTyping into chat will now be redirected.")
            else:
                await message.channel.send(f"Your selection was not found in your characters list. Type !list for all characters.")
        print(values)
        return
    elif message.content == "!list":
        list = ""
        for key in CHARACTERS:
            list += f"{str(key)}: {CHARACTERS[key]['username']}\n"
        await message.channel.send(list)
        return


    if (author_id in TESTERS) and channel_id == TEST_CHANNEL and author_id in SELECTION:
        async with send_channel.typing():
            post(URL, CHARACTERS[SELECTION[author_id]], content)
            #await send_channel.send(f"{content}")
            await message.delete()


client.run(TOKEN)