import os
import discord
import requests


from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
URL = os.getenv('DISCORD_WEBHOOK')

client = discord.Client()

TESTERS = [108062945740640256, 219093637986779138, 108072654577152000]
CREATION_CHANNEL = 672554910566580224

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

# Steps for Mode are as follows
# Mode 0 - Not creating
# Mode 1 - Mode enabled seeking name
# Mode 2 - Name provided seeking icon
# Mode 3 - Completed Status

MODE_MESSAGES = [" ",
                 "Please provide a name for your character.",
                 "Do you have an icon url for your character? Say 'No' if not.",
                 "Please give a brief description of your character.",
                 "Your character has been created!"
                 ]
USER_MODES = {}


class CreateCharacter():
    def __init__(self, author_id):
        self.MODE = 0
        self.author = author_id

    def set_mode(self, value):
        if isinstance(value, int):
            if value >= 0 and value <=4:
                self.MODE = value
            else:
                print("Value is out of range.")
        else:
            print("Incorrect type.")

def get_user_mode(author_id):
    if author_id in User_mode_info:
        print('author id was found, returning info')
        return User_mode_info[author_id]
    else:
        print("author id wasn't found, sending 0 and adding to table")
        User_mode_info.update({author_id: 0})
        return 0

def set_user_mode(author_id, value):
    User_mode_info.update({author_id: value})
    print(f"{author_id} has been set to {value}.")

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

    if author_id in USER_MODES:
        mode_info = USER_MODES[author_id]
    else:
        USER_MODES[author_id] = CreateCharacter(author_id)
        mode_info = USER_MODES[author_id]
    if message.content == "Taco":
        breakpoint()
    if mode_info.MODE > 0 and mode_info.author == author_id:
        if mode_info.MODE == 1:
            await message.channel.send("Mode 1 is active, moving on to mode 2.")
            ## todo: add details about author and date/time
            await message.channel.send(f"Your character's name was set to: {message.content}")
            mode_info.set_mode(2)
        elif mode_info.MODE == 2:
            await message.channel.send("Mode 2 is active, moving on to mode 3")
            if message.content.lower() == "no":
                await message.channel.send(f"Icon has been skipped.")
            else:
                await message.channel.send(f"Icon has been set to: {message.content}")
            mode_info.set_mode(3)
        elif mode_info.MODE == 3:
            await message.channel.send("Mode 3 is active, moving on.")
            mode_info.set_mode(0)

        await message.channel.send(MODE_MESSAGES[mode_info.MODE])
        return
    elif mode_info.MODE > 0 and mode_info.author != author_id:
        if message.content == "!create":
            await message.channel.send("Sorry someone else is creating a character right now.")
        else:
            print("Mode is active, but this message was not from the creating person, pass on to other person.")
        return
    else:
        pass
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
    elif message.content == "!create" and mode_info.MODE == 0:
        if channel_id == CREATION_CHANNEL:
            mode_info.set_mode(1)
            await message.channel.send(MODE_MESSAGES[mode_info.MODE])
        else:
            await message.channel.send("Sorry you're using the wrong channel to create your character.")

    if (author_id in TESTERS) and channel_id == TEST_CHANNEL and author_id in SELECTION:
        async with send_channel.typing():
            post(URL, CHARACTERS[SELECTION[author_id]], content)
            #await send_channel.send(f"{content}")
            await message.delete()
    breakpoint()

client.run(TOKEN)