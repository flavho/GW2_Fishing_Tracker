import requests
import time

from sty import Style, RgbFg, fg, bg, ef, rs
import os
from dotenv import load_dotenv
import base64

import sqlite3
import discord


def create_new_user(apikey, name, discord_user_id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("insert into users values (?, ?, ?)", (apikey, name, discord_user_id))
    con.commit()
    con.close()

def get_user(discord_id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select * from users where discordid=:discord_id", {"discord_id": discord_id})
    save = cur.fetchall()
    con.close()
    return save

def create_tournament(apikey, name, discord_user_id, start, duration,id, preparing_time):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("insert into tournament values (?, ?, ?, ?, ?, ?, ?)", (apikey, name, discord_user_id, start, duration,id, preparing_time))
    con.commit()
    con.close()


def join_tournament(tournament_id, api_key, player_name, discord_id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select * from tournament where id=:tournament_id", {"tournament_id": tournament_id})
    save = cur.fetchall()
    api_keys = save[0][0] + "," + api_key
    char_names = save[0][1] + "," + player_name
    discord_id = save[0][2] + "," + discord_id
    cur.execute(f"update tournament SET subscriberkey = '{api_keys}', subscribername = '{char_names}', discordid = '{discord_id}' WHERE id = '{tournament_id}'")
    con.commit()
    con.close()


def generate_status_fish_by_apikey(apikey, character_name):
    ITEMS_IN_INVENTORY = []
    COUNT_INVENTORY = {}
    FISH_IN_INVENTORY = []
    TOTAL_FISH = 0
    JUNK = 0
    BASIC = 0
    FINE = 0
    MASTERWORK = 0
    RARE = 0
    EXOTIC = 0
    ASCENDED = 0
    LEGENDARY = 0

    fg.WHITE = Style(RgbFg(255, 255, 255))
    fg.JUNK = Style(RgbFg(209, 207, 207))
    fg.BASIC = Style(RgbFg(0, 0, 0))
    fg.FINE = Style(RgbFg(91, 161, 199))
    fg.MASTERWORK = Style(RgbFg(255, 150, 50))
    fg.RARE = Style(RgbFg(250, 206, 85))
    fg.EXOTIC = Style(RgbFg(255, 162, 0))
    fg.ASCENDED = Style(RgbFg(240, 72, 97))
    fg.LEGENDARY = Style(RgbFg(142, 60, 189))

    payload = {'access_token': apikey}
    r = requests.get(f'https://api.guildwars2.com/v2/characters/{character_name}/inventory', params=payload)
    json = r.json()
    for ibag in json["bags"]:
        for item in ibag['inventory']:
            if item is not None:
                item_id = item["id"]
                ITEMS_IN_INVENTORY.append(item_id)
                COUNT_INVENTORY[item_id] = item["count"]

    items_string = ' ,'.join(str(e) for e in ITEMS_IN_INVENTORY)
    payload_two = {'ids': items_string}
    re = requests.get('https://api.guildwars2.com/v2/items', params=payload_two)
    json_items = re.json()
    for e in json_items:
        if 'description' in e:
            if e['description'] == 'Double-click to convert to materials.':
                color = ""
                if e['rarity'] == "Junk":
                    JUNK += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Basic":
                    BASIC += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Fine":
                    FINE += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Masterwork":
                    MASTERWORK += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Rare":
                    RARE += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Exotic":
                    EXOTIC += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Ascended":
                    ASCENDED += COUNT_INVENTORY.get(e['id'])
                elif e['rarity'] == "Legendary":
                    LEGENDARY += COUNT_INVENTORY.get(e['id'])
                FISH_IN_INVENTORY.append(color + e['name'] + '  ' + str(COUNT_INVENTORY.get(e['id'])))
                TOTAL_FISH += COUNT_INVENTORY.get(e['id'])
    return (character_name + ':    ' + ' |  '.join(str(e) for e in FISH_IN_INVENTORY) + "\n" + '```diff\n' + 'Total Fish: ' + str(
        TOTAL_FISH) + ' | Legendary: ' + str(LEGENDARY) + '| '
                                                          'Ascended: ' + str(ASCENDED) + ' | EXOTIC: ' + str(
        EXOTIC) + ' | RARE: ' + str(RARE) + ' | MASTERWORK: ' +
            str(MASTERWORK) + ' | FINE: ' + str(FINE) + ' | BASIC: ' + str(BASIC)) + '\n```'


def generate_standings_apikey(subscribers):
    STANDINGS = {}
    for sub in subscribers:
        API_KEY = sub[0]
        PLAYER_NAME = sub[1]
        ITEMS_IN_INVENTORY = []
        COUNT_INVENTORY = {}
        FISH_IN_INVENTORY = []

        # Count
        TOTAL_FISH = 0
        JUNK = 0
        BASIC = 0
        FINE = 0
        MASTERWORK = 0
        RARE = 0
        EXOTIC = 0
        ASCENDED = 0
        LEGENDARY = 0

        # Rarity Score
        JUNK_SCORE = 0
        BASIC_SCORE = 1
        FINE_SCORE = 2
        MASTERWORK_SCORE = 3
        RARE_SCORE = 5
        EXOTIC_SCORE = 7
        ASCENDED_SCORE = 10
        LEGENDARY_SCORE = 15

        payload = {'access_token': API_KEY}
        r = requests.get(f'https://api.guildwars2.com/v2/characters/{PLAYER_NAME}/inventory', params=payload)
        json = r.json()
        for ibag in json["bags"]:
            for item in ibag['inventory']:
                if item is not None:
                    item_id = item["id"]
                    ITEMS_IN_INVENTORY.append(item_id)
                    COUNT_INVENTORY[item_id] = item["count"]

        items_string = ' ,'.join(str(e) for e in ITEMS_IN_INVENTORY)
        payload_two = {'ids': items_string}
        re = requests.get('https://api.guildwars2.com/v2/items', params=payload_two)
        json_items = re.json()
        for e in json_items:
            if 'description' in e:
                if e['description'] == 'Double-click to convert to materials.':
                    color = ""
                    if e['rarity'] == "Junk":
                        JUNK += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Basic":
                        BASIC += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Fine":
                        FINE += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Masterwork":
                        MASTERWORK += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Rare":
                        RARE += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Exotic":
                        EXOTIC += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Ascended":
                        ASCENDED += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Legendary":
                        LEGENDARY += COUNT_INVENTORY.get(e['id'])
        STANDINGS[
            PLAYER_NAME] = JUNK * JUNK_SCORE + BASIC * BASIC_SCORE + FINE * FINE_SCORE + MASTERWORK * MASTERWORK_SCORE + RARE * RARE_SCORE + EXOTIC * EXOTIC_SCORE + ASCENDED * ASCENDED_SCORE + LEGENDARY * LEGENDARY_SCORE
    return STANDINGS


def generate_advanced_standings_apikey(subscribers):
    STANDINGS = {}
    for sub in subscribers:
        API_KEY = sub[0]
        PLAYER_NAME = sub[1]
        ITEMS_IN_INVENTORY = []
        COUNT_INVENTORY = {}
        FISH_IN_INVENTORY = []

        # Count
        TOTAL_FISH = 0
        JUNK = 0
        BASIC = 0
        FINE = 0
        MASTERWORK = 0
        RARE = 0
        EXOTIC = 0
        ASCENDED = 0
        LEGENDARY = 0

        # Rarity Score
        JUNK_SCORE = 0
        BASIC_SCORE = 1
        FINE_SCORE = 2
        MASTERWORK_SCORE = 3
        RARE_SCORE = 5
        EXOTIC_SCORE = 7
        ASCENDED_SCORE = 10
        LEGENDARY_SCORE = 15

        payload = {'access_token': API_KEY}
        r = requests.get(f'https://api.guildwars2.com/v2/characters/{PLAYER_NAME}/inventory', params=payload)
        json = r.json()
        for ibag in json["bags"]:
            for item in ibag['inventory']:
                if item is not None:
                    item_id = item["id"]
                    ITEMS_IN_INVENTORY.append(item_id)
                    COUNT_INVENTORY[item_id] = item["count"]

        items_string = ' ,'.join(str(e) for e in ITEMS_IN_INVENTORY)
        payload_two = {'ids': items_string}
        re = requests.get('https://api.guildwars2.com/v2/items', params=payload_two)
        json_items = re.json()
        for e in json_items:
            if 'description' in e:
                if e['description'] == 'Double-click to convert to materials.':
                    color = ""
                    if e['rarity'] == "Junk":
                        JUNK += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Basic":
                        BASIC += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Fine":
                        FINE += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Masterwork":
                        MASTERWORK += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Rare":
                        RARE += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Exotic":
                        EXOTIC += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Ascended":
                        ASCENDED += COUNT_INVENTORY.get(e['id'])
                    elif e['rarity'] == "Legendary":
                        LEGENDARY += COUNT_INVENTORY.get(e['id'])
        STANDINGS[
            PLAYER_NAME] = [[JUNK, JUNK_SCORE], [BASIC, BASIC_SCORE], [FINE, FINE_SCORE],
                            [MASTERWORK, MASTERWORK_SCORE], [RARE, RARE_SCORE],
                            [EXOTIC, EXOTIC_SCORE], [ASCENDED, ASCENDED_SCORE], [LEGENDARY, LEGENDARY_SCORE]]
    return STANDINGS


if __name__ == '__main__':
    client = discord.Client()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')


    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))


    @client.event
    async def on_message(message):
        message_author = message.author.display_name + '#' + message.author.discriminator

        user = get_user(message_author)
        if len(user) == 0:
            if message.author == client.user:
                return
            await message.channel.send("You need to register to see information. Please type <Register> for more information")

            if message.content.startswith('Register:'):
                if message.channel.type.name == 'private':
                    creds = message.content[9:]
                    parts = creds.split(",")
                    api_key = parts[0]
                    name = parts[1]
                    message_author = message.author.display_name + '#' + message.author.discriminator
                    create_new_user(api_key, name, message_author)
                    await message.channel.send("User registered!")
                else:
                    await message.channel.send(
                        "Please use the private chat for user registration: Type <Register> for further information")

            elif message.content.startswith('Register'):
                await message.channel.send(
                    "Please send your user details in a private chat with GW2FishingTournament in the following format {API Key needs inventory, characters and account access}: \n Register:<apikey>,<character_name>")

        else:
            api_key = user[0][0]
            char_name = user[0][1]

            if message.author == client.user:
                return
            if message.content == 'Points':
                response = sorted(generate_advanced_standings_apikey(SUBSCRIBER_FISHING_CHALLENGE).items(),
                                key=lambda x: x[1],
                                reverse=True)
                place = 1
                for key in response:
                    print_message = f"Position {place}: " + str(key[0])
                    JUNK = key[1][0]
                    BASIC = key[1][1]
                    FINE = key[1][2]
                    MASTERWORK = key[1][3]
                    RARE = key[1][4]
                    EXOTIC = key[1][5]
                    ASCENDED = key[1][6]
                    LEGENDARY = key[1][7]
                    TOTAL = JUNK[0] * JUNK[1] + BASIC[0] * BASIC[1] + FINE[0] * FINE[1] + MASTERWORK[0] * MASTERWORK[1] + \
                            RARE[0] * RARE[1] + EXOTIC[0] * EXOTIC[1] + ASCENDED[0] * ASCENDED[1] + LEGENDARY[0] * \
                            LEGENDARY[1]
                    second_print = f"JUNK: {JUNK[0]} Fish * {JUNK[1]} Quantity = {JUNK[0] * JUNK[1]} Points" + "\n" + f"BASIC: {BASIC[0]} Fish * {BASIC[1]} Quantity = {BASIC[0] * BASIC[1]} Points" + "\n" + f"FINE: {FINE[0]} Fish * {FINE[1]} Quantity = {FINE[0] * FINE[1]} Points" + "\n" + f"MASTERWORK: {MASTERWORK[0]} Fish * {MASTERWORK[1]} Quantity = {MASTERWORK[0] * MASTERWORK[1]} Points" + "\n" + f"RARE: {RARE[0]} Fish * {RARE[1]} Quantity = {RARE[0] * RARE[1]} Points" + "\n" + f"EXOTIC: {EXOTIC[0]} Fish * {EXOTIC[1]} Quantity = {EXOTIC[0] * EXOTIC[1]} Points" + "\n" + f"ASCENDED: {ASCENDED[0]} Fish * {ASCENDED[1]} Quantity = {ASCENDED[0] * ASCENDED[1]} Points" + "\n" + f"LEGENDARY: {LEGENDARY[0]} Fish * {LEGENDARY[1]} Quantity = {LEGENDARY[0] * LEGENDARY[1]} Points "
                    await message.channel.send(
                        print_message + "\n" + second_print + "\n" + "Total: " + str(TOTAL) + " Points")
                    await message.channel.send("---------------------------------------------------")
                    place += 1


            elif message.content == 'Fish':
                response = generate_status_fish_by_apikey(api_key, char_name)
                await message.channel.send(response)


            elif message.content == 'Standings':
                response = sorted(generate_standings_apikey(SUBSCRIBER_FISHING_CHALLENGE).items(), key=lambda x: x[1],
                                reverse=True)
                place = 1
                for key in response:
                    print_message = f"Position {place}: " + str(key[0]) + ' -> ' + str(key[1]) + " Points"
                    await message.channel.send(print_message)
                    await message.channel.send("---------------------------------------------------")
                    place += 1


            elif message.content == 'help':
                await message.channel.send("Write <Points>, <Fish>, <Standings> for tournament information")


            elif message.content.startswith('Tournament:'):
                creds = message.content[11:]
                parts = creds.split(",")
                duration = parts[0]
                preparing_time = parts[1]
                current_time = time.time()

                id_string = str(int(current_time)) + char_name
                id_string_bytes = id_string.encode('ascii')
                base64_bytes = base64.b64encode(id_string_bytes)
                base64_id_string = base64_bytes.decode('ascii')

                create_tournament(api_key, char_name, message_author, current_time, duration, base64_id_string, preparing_time)
                await message.channel.send(f"Your event key is: {base64_id_string}")

            elif message.content.startswith('Join:'):
                key = message.content[5:]
                join_tournament(key, api_key, char_name, message_author)
                await message.channel.send(f"You joined the event")



    client.run(TOKEN)
