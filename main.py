import requests
import time
from sty import Style, RgbFg, fg, bg, ef, rs
import os


def print_fish_by_apikey(apikey, character_name):
    ITEMS_IN_INVENTORY = []
    COUNT_INVENTORY = {}
    FISH_IN_INVENTORY = []
    TOTAL_FISH = 0
    JUNK = 0
    BASIC =0
    FINE =0
    MASTERWORK =0
    RARE =0
    EXOTIC =0
    ASCENDED =0
    LEGENDARY =0

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
                    color = fg.JUNK
                elif e['rarity'] == "Basic":
                    BASIC += COUNT_INVENTORY.get(e['id'])
                    color = fg.BASIC
                elif e['rarity'] == "Fine":
                    FINE += COUNT_INVENTORY.get(e['id'])
                    color = fg.FINE
                elif e['rarity'] == "Masterwork":
                    MASTERWORK += COUNT_INVENTORY.get(e['id'])
                    color = fg.MASTERWORK
                elif e['rarity'] == "Rare":
                    RARE += COUNT_INVENTORY.get(e['id'])
                    color = fg.RARE
                elif e['rarity'] == "Exotic":
                    EXOTIC += COUNT_INVENTORY.get(e['id'])
                    color = fg.EXOTIC
                elif e['rarity'] == "Ascended":
                    ASCENDED += COUNT_INVENTORY.get(e['id'])
                    color = fg.ASCENDED
                elif e['rarity'] == "Legendary":
                    LEGENDARY += COUNT_INVENTORY.get(e['id'])
                    color = fg.LEGENDARY
                FISH_IN_INVENTORY.append(color + e['name'] + '  ' + str(COUNT_INVENTORY.get(e['id'])))
                TOTAL_FISH += COUNT_INVENTORY.get(e['id'])
    print(character_name + ':    ' + ' |  '.join(str(e) for e in FISH_IN_INVENTORY) + fg.WHITE)
    print(character_name + ':    ' + 'Total Fish: ' +  str(TOTAL_FISH) + ' | Legendary: ' + str(LEGENDARY) + '| '
            'Ascended: ' + str(ASCENDED) + ' | EXOTIC: ' + str(EXOTIC) + ' | RARE: ' + str(RARE) + ' | MASTERWORK: ' +
            str(MASTERWORK) + ' | FINE: ' + str(FINE) + ' | BASIC: ' + str(BASIC))


if __name__ == '__main__':
    os.system('color 8f')

    SUBSCRIBER_FISHING_CHALLENGE = [
        ['072C6BF4-DA86-8948-BB0E-0818531EDD11859E8F18-B863-4EC2-9931-003970C7E73C', 'Fish O Matic']
    ]

    while True:
        for e in SUBSCRIBER_FISHING_CHALLENGE:
            print_fish_by_apikey(e[0], e[1])
        time.sleep(20)
