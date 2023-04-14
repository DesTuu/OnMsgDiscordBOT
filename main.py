import discord
import requests
import json
import os
from keep_alive import keep_alive
from poke_types import *
from tutor import Kanto, Unova, Hoenn, Sinnoh
import pandas as pd
from swear_words import swear_words, symbols
import sqlite3
import settings

# kicak = 0
# destu = 0
# saari = 0
# pacia = 0
# bzdursky = 0

# connection = sqlite3.connect("counter.db")
# cur = connection.cursor()

# try:
#   cur.execute("""CREATE TABLE counter(id, counter)""")
#   connection.commit()
# except:
#   pass

# cur.execute("""SELECT * FROM counter""")
# kicak_value = cur.fetchall()[0][1]
# if kicak < kicak_value:
#   kicak = kicak_value
# cur.execute("""SELECT * FROM counter""")
# destu_value = cur.fetchall()[1][1]
# if destu < destu_value:
#   destu = destu_value
# cur.execute("""SELECT * FROM counter""")
# saari_value = cur.fetchall()[2][1]
# if saari < saari_value:
#   saari = saari_value
# cur.execute("""SELECT * FROM counter""")
# pacia_value = cur.fetchall()[3][1]
# if pacia < pacia_value:
#   pacia = pacia_value
# cur.execute("""SELECT * FROM counter""")
# bzdursky_value = cur.fetchall()[4][1]
# if bzdursky < bzdursky_value:
#   bzdursky = bzdursky_value
# connection.close

logger = settings.logging.getLogger('bot')

intents = discord.Intents().all()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents, activity=discord.Game(name='WinRAR'))

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote

temp_channels = []

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
  possible_channel_name = f"😎 {member.display_name} 😎"
  try:
    if after.channel.id == 1083416638835146802:
      temp_channel = await after.channel.clone(name=possible_channel_name)
      await member.move_to(temp_channel)
      temp_channels.append(temp_channel.id)
  except AttributeError:
    pass
  try:
    if before.channel.id in temp_channels:
      if len(before.channel.members) == 0:
        await before.channel.delete()
  except AttributeError:
    pass

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
  if payload.message_id == 1082308093112766535:
    role = payload.member.guild.get_role(371220781729972225)
    await payload.member.add_roles(role)

  if payload.message_id == 1085542516935364710:
    if payload.emoji.id == 1084757554686603305:
      role = payload.member.guild.get_role(1084738918001430608)
      await payload.member.add_roles(role)
    if payload.emoji.id == 1084755172338696212:
      role = payload.member.guild.get_role(1084738766209556501)
      await payload.member.add_roles(role)
    if payload.emoji.id == 1086681178398019684:
      role = payload.member.guild.get_role(1086670550727921724)
      await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
  if payload.message_id == 1085542516935364710:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
    if payload.emoji.id == 1084757554686603305:
      role = discord.utils.get(guild.roles, id=1084738918001430608)
      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.remove_roles(role)
    if payload.emoji.id == 1084755172338696212:
      role = discord.utils.get(guild.roles, id=1084738766209556501)
      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.remove_roles(role)
    if payload.emoji.id == 1086681178398019684:
      role = discord.utils.get(guild.roles, id=1086670550727921724)
      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.remove_roles(role)
  
@bot.event
async def on_message(message):
  global kicak, pacia, destu, saari, bzdursky, kicak_value, pacia_value, destu_value, saari_value, bzdursky_value
  if message.author == bot.user:
    return

  m = message.content
  # if 1081203887190585434 != message.channel.id:
  #   for j in symbols:
  #       if j in message.content:
  #         message.content = message.content.replace(j, "")
  #   new_message = message.content.lower()
  #   message.content = str(message.content.lower())
  #   for k in range(len(message.content)):
  #     try:
  #       if message.content[k] == message.content[k-1]:
  #         new_message = new_message.replace(message.content[k], '', 1)
  #     except:
  #       pass
  #   for i in swear_words:
  #     if i in message.content or i in str(new_message):
  #       await message.delete()
  #       connection = sqlite3.connect("counter.db")
  #       cur = connection.cursor()
  #       if message.author.id == 457298064995123201:
  #         kicak += 1
  #         if kicak > kicak_value:
  #           cur.execute("""UPDATE counter SET counter=? WHERE id=1""", (kicak,))
  #           connection.commit()
  #         else:
  #           kicak = kicak_value + 1
  #         await message.author.send(f"To poważny serwer! Tu panuje zakaz pisania słowa: {m}! Właśnie przeklnąłeś {kicak}. raz na tym serwerze!")
  #         if kicak % 10 == 0:
  #           await message.channel.send(f"Gratulacje Kicako! Właśnie przeklnąłeś {kicak}. raz na tym serwerze!")
  #       elif message.author.id == 354712325053218819:
  #         destu += 1
  #         if destu > destu_value:
  #           cur.execute("""UPDATE counter SET counter=? WHERE id=2""", (destu,))
  #           connection.commit()
  #         else:
  #           destu = destu_value + 1
  #         await message.author.send(f"To poważny serwer! Tu panuje zakaz pisania słowa: {m}! Właśnie przeklnąłeś {destu}. raz na tym serwerze!")
  #         if destu % 10 == 0:
  #           await message.channel.send(f"Gratulacje DesTu! Właśnie przeklnąłeś {destu}. raz na tym serwerze!")
  #       elif message.author.id == 188032154507149312:
  #         saari += 1
  #         if saari > saari_value:
  #           cur.execute("""UPDATE counter SET counter=? WHERE id=3""", (saari,))
  #           connection.commit()
  #         else:
  #           saari = saari_value + 1
  #         await message.author.send(f"To poważny serwer! Tu panuje zakaz pisania słowa: {m}! Właśnie przeklnąłeś {saari}. raz na tym serwerze!")
  #         if saari % 10 == 0:
  #           await message.channel.send(f"Gratulacje Saari! Właśnie przeklnąłeś {saari}. raz na tym serwerze!")
  #       elif message.author.id == 392769575835402242:
  #         pacia += 1
  #         if pacia > pacia_value:
  #           cur.execute("""UPDATE counter SET counter=? WHERE id=4""", (pacia,))
  #           connection.commit()
  #         else:
  #           pacia = pacia_value + 1
  #         await message.author.send(f"To poważny serwer! Tu panuje zakaz pisania słowa: {m}! Właśnie przeklnąłeś {pacia}. raz na tym serwerze!")
  #         if pacia % 10 == 0:
  #           await message.channel.send(f"Gratulacje Pacia! Właśnie przeklnąłeś {pacia}. raz na tym serwerze!")
  #       elif message.author.id == 541172544833716225:
  #         bzdursky += 1
  #         if bzdursky > bzdursky_value:
  #           cur.execute("""UPDATE counter SET counter=? WHERE id=5""", (bzdursky,))
  #           connection.commit()
  #         else:
  #           bzdursky = bzdursky_value + 1
  #         await message.author.send(f"To poważny serwer! Tu panuje zakaz pisania słowa: {m}! Właśnie przeklnąłeś {bzdursky}. raz na tym serwerze!")
  #         if bzdursky % 10 == 0:
  #           await message.channel.send(f"Gratulacje Fifi! Właśnie przeklnąłeś {bzdursky}. raz na tym serwerze!")
  #       else:
  #         await message.author.send(f"To poważny serwer! Tu panuje zakaz pisania słowa: {m}!")
  #       connection.close

  if message.content.startswith("$voteban"):
    ban = m[9:]
    message = await message.channel.send(f"Czy na pewno chcecie zbanować użytkownika {ban}? Musi być minimum 80% głosów na tak.")
    await message.add_reaction("\U00002705")
    await message.add_reaction("\U0000274c")
    
  
  if message.content.startswith("$rank"):
    embed = discord.Embed(title="Ranking przekleństw", color=0x00ff00)
    embed.add_field(name="DesTu", value=destu)
    embed.add_field(name="Pacia", value=pacia)
    embed.add_field(name="Saari", value=saari)
    embed.add_field(name="Kicako", value=kicak)
    embed.add_field(name="Fifi", value=bzdursky)
    await message.channel.send(embed=embed)

  if message.content.startswith("$mess"):
    await message.delete()
    await message.channel.send(m.replace('$mess', ''))
  
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$moves'):
    moves_list = []
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{message.content.lower()[7:]}')
    data = response.json()
    for item in data["moves"]:
      type_name = item["move"]["name"]
      type_name = type_name.title()
      type_name = type_name.replace("-", " ")
      moves_list.append(type_name)
    moves_list.sort()
    moves_list = str(moves_list)
    moves_list = moves_list.replace("'", "")
    moves_list = moves_list.replace("[", "")
    moves_list = moves_list.replace("]", "")
    await message.channel.send(f'Alfabetycznie posortowana lista ruchów Pokemona - {message.content.title()[7:]}:\n\n{moves_list}')

  if message.content.startswith('$check'):
    message2 = message.content.lower()
    message2 = message2.split(" ")
    message2 = list(message2)
    moves_list2 = []
    message3 = str(message2[1])
    response2 = requests.get(f'https://pokeapi.co/api/v2/pokemon/{message3.lower()}')
    data2 = response2.json()
    for item in data2["moves"]:
      type_name2 = item["move"]["name"]
      type_name2 = type_name2.replace("-", " ")
      type_name2 = type_name2.lower()
      moves_list2.append(type_name2)
      move2 = message2[2:]
      move2 = str(move2)
      move2 = move2.lower()
      char_remove = ["'", "[", "]", ","]
      for char in char_remove:
        move2 = move2.replace(char, "")
    if move2 in moves_list2:
      await message.channel.send("Tak, może się nauczyć!")
    else: 
      await message.channel.send("Nie, nie może się nauczyć lub wpisałeś niewłaściwą nazwę!")

  if message.content.startswith('$eff'):
    message4 = message.content.lower()
    message4 = message4.split(" ")
    message4 = list(message4)
    message5 = str(message4[2])
    this_type = str(message4[1]).lower()
    this_type = eval(this_type)
    response4 = requests.get(f'https://pokeapi.co/api/v2/pokemon/{message5.lower()}')
    data4 = response4.json()
    L = []

    for item in data4['types']:
      type = item['type']['name']
      L.append(type)

    for item in this_type:
      if L[0] in this_type:
        A = this_type[L[0]]
      else:
        A = 1
      try:
        if L[1] in this_type:
            B = this_type[L[1]]
        else:
            B = 1
      except(IndexError):
        B = 1

    total = A*B
    if total == 1:
      total = int(total)

    the_type = str(message4[1]).title()
    await message.channel.send(f"{the_type} bije {total}x w {message5.title()}'a")

  if message.content.startswith('$gender'):
    message6 = message.content.lower()
    message6 = message6.split(" ")
    message6 = list(message6)
    message6 = str(message6[1])
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{message6}')
    message6 = message6.title()
    data = response.json()['gender_rate']
    if data == -1:
      await message.channel.send(f"{message6} jest genderless. Można breedować tylko z {message6} i Ditto, ale nie ponosisz kosztów za wybór płci!")
    if data == 0:
      await message.channel.send(f"{message6} występuje tylko w formie męskiej. Można breedować tylko z Ditto, ale nie ponosisz kosztów za wybór płci!")
    if data == 1:
      await message.channel.send(f"{message6} ma 12,5% na bycie samicą! Ponosisz 21 000$ za każdy wybór płci samicy!")
    if data == 2:
      await message.channel.send(f"{message6} ma 25% na bycie samicą! Ponosisz 9 000$ za każdy wybór płci samicy!")
    if data == 4:
      await message.channel.send(f"{message6} ma 50% na bycie samicą! Koszt wyboru obu płci wynosi: 5 000$")
    if data == 6:
      await message.channel.send(f"{message6} ma 75% na bycie samicą! Ponosisz 9 000$ za każdy wybór płci samca!")
    if data == 8:
      await message.channel.send(f"{message6} ma 100% na bycie samicą! Nie ponosisz żadnych kosztów za wybór płci! Uwaga! {message6} nie nadaje się do breedowania innych pokemonów!")

  if message.content.startswith('$breed'):
    message8 = message.content.lower()
    message8 = message8.split(" ")
    message8 = list(message8)
    breed_iv = int(message8[3])
    message9 = str(message8[1])
    gtl = int(message8[2])
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{message9}')
    data = response.json()['gender_rate']
    message9 = str(message9).title()
    if data == -1:
      gender_female = 0
      await message.channel.send(f"{message9} jest genderless. Można breedować tylko z {message9} i Ditto, ale nie ponosisz kosztów za wybór płci!")
    if data == 0:
      gender_female = 0
      await message.channel.send(f"{message9} występuje tylko w formie męskiej. Można breedować tylko z Ditto, ale nie ponosisz kosztów za wybór płci!")
    if data == 1:
      gender_female = 21_000
      await message.channel.send(f"{message9} ma 12,5% na bycie samicą! Ponosisz 21 000$ za każdy wybór płci samicy!")
    if data == 2:
      gender_female = 9_000
      await message.channel.send(f"{message9} ma 25% na bycie samicą! Ponosisz 9 000$ za każdy wybór płci samicy!")
    if data == 4:
      gender_female = 5_000
      await message.channel.send(f"{message9} ma 50% na bycie samicą! Koszt wyboru obu płci wynosi: 5 000$")
    if data == 6:
      gender_female = 5_000
      await message.channel.send(f"{message9} ma 75% na bycie samicą! Ponosisz 9 000$ za każdy wybór płci samca!")
    if data == 8:
      gender_female = 0
      await message.channel.send(f"{message9} ma 100% na bycie samicą! Nie ponosisz żadnych kosztów za wybór płci! Uwaga! {message9} nie nadaje się do breedowania innych pokemonów!")
      
    gender = 5_000
    everstone = 6_000
    cycle2 = gtl * 2 + 20_000
    cycle = 20_000
    everstone_cycle = 10_000 + everstone

    five = (cycle2 * 8) + (cycle * 7) + (4 * gender_female) + (7 * gender)
    five_nature = (7 * cycle2) + (4 * everstone_cycle) + (4 * cycle) + (7 * gender) + gtl
    five_total = five_nature + five
    three = (cycle2 * 2) + cycle + (2 * gender_female) + gender
    three_nature = cycle2 + gtl + (2 * everstone_cycle) + gender
    three_total = three + three_nature
    four = three + (cycle2 * 2) + (2 * gender) + (2 * cycle) + gender_female
    four_nature = (2 * cycle2) + cycle + (3 * gender) + (3 * everstone_cycle) + cycle2 + gtl
    four_total = four + four_nature
    six = (five * 2) - (3 * gender_female) + (4 * gender) + cycle
    six_nature = (11 * cycle2) + (8 * cycle) + (12 * gender) + (5 * everstone_cycle) + gtl
    six_total = six + six_nature
    if breed_iv == 5:
      await message.channel.send(f"Do zbreedowania Pokemona {message9.title()} {breed_iv}x31IV potrzeba: \n Minimum: {'{:_}'.format(five)}$ - liczenie na farta, że natura wejdzie ({int((1/25)*100)}% szansy) \n Maksymalnie: {'{:_}'.format(five_total)}$ - jeśli podczas breedu w ogóle natura nie wejdzie")
    if breed_iv == 3:
      await message.channel.send(f"Do zbreedowania Pokemona {message9.title()} {breed_iv}x31IV potrzeba: \n Minimum: {'{:_}'.format(three)}$ - liczenie na farta, że natura wejdzie ({int((1/25)*100)}% szansy) \n Maksymalnie: {'{:_}'.format(three_total)}$ - jeśli podczas breedu w ogóle natura nie wejdzie")
    if breed_iv == 4:
      await message.channel.send(f"Do zbreedowania Pokemona {message9.title()} {breed_iv}x31IV potrzeba: \n Minimum: {'{:_}'.format(four)}$ - liczenie na farta, że natura wejdzie ({int((1/25)*100)}% szansy) \n Maksymalnie: {'{:_}'.format(four_total)}$ - jeśli podczas breedu w ogóle natura nie wejdzie")
    if breed_iv == 6:
      await message.channel.send(f"Do zbreedowania Pokemona {message9.title()} {breed_iv}x31IV potrzeba: \n Minimum: {'{:_}'.format(six)}$ - liczenie na farta, że natura wejdzie ({int((1/25)*100)}% szansy) \n Maksymalnie: {'{:_}'.format(six_total)}$ - jeśli podczas breedu w ogóle natura nie wejdzie")

    message9 = str(message9).lower()
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{message9}')
    data = response.json()
    evolution = data["evolves_from_species"]
  
    if evolution == None:
        pokebaby = message9
    else:
      evolution = str(evolution).replace("'", "").split(',')
      evolution = evolution[0][7:]
      response2 = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{evolution}')
      data2 = response2.json()
      evolution1 = data2['evolves_from_species']
      if evolution1 == None:
        pokebaby = str(evolution).lower()
      else:
        evolution1 = str(evolution1).replace("'", "").split(',')
        evolution1 = evolution1[0][7:]
        response4 = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{evolution1}')
        data4 = response4.json()
        evolution2 = data4['evolves_from_species']
        if evolution2 == None:
          pokebaby = str(evolution1).lower()
        else:
          pokebaby = str(evolution2).lower()          
  
    response3 = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokebaby}')
    data3 = response3.json()
    data3 = str(data3['is_baby']).title()
    if data3 == 'True':
      await message.channel.send(f'Pamiętaj, że {pokebaby.title()} jest pokemonem baby! Nie możesz go breedować, dopóki nie przejdzie ewolucji! Zazwyczaj trzeba nabić Hapiness (radość), aby ewolwuować!')
    

  if message.content.startswith('$move'):
    move_name = message.content.lower().replace('$move ', "")
    if " " in move_name:
      move_name = move_name.replace(" ", "-", 1)

    response = requests.get(f'http://pokeapi.co/api/v2/move/{move_name}/')
    data = response.json()
    
    accuracy = data['accuracy']
    power = data['power']
    pp = data['pp']
    max_pp = int(pp * 1.6)
    effect_chance = data['effect_chance']
    priority = data['priority']

    hits = str(data['meta']).split(':')
    max_hits = str(hits[14]).replace(", 'max_turns'", "")
    min_hits = str(hits[16]).replace(", 'min_turns'", "")
    
    for i in data['effect_entries']:
        effect = i['short_effect']
    
    type_name = data['type']
    type_name = str(type_name).split()
    type_name = type_name[1]
    type_name = str(type_name).replace(',', '')
    type_name = type_name.replace("'", "").title()

    string = f'\nBije od{min_hits}x do{max_hits}x w jednej turze '
    accuracy1 = ''
    
    if '$effect_chance%' in effect:
      effect = str(effect).replace('$effect_chance', str(effect_chance))
    if priority >= 1:
      priority = '+' + str(priority)
    if priority == 0:
      priority = "0 - Bez priorytetu"
    if "-" in move_name:
      move_name = move_name.replace("-", " ")
    if power == None:
      power = "0 - Ruch statusowy lub bije obrażenia zależne od czegoś (przeczytaj opis)"
    if accuracy == None:
      accuracy = 100 
      accuracy1 = '- Zawsze użyje, nawet po obniżeniu celności'
    if min_hits == max_hits:
      string = f'\nBije{max_hits}x w jednej turze '
      if max_hits == ' None':
        max_hits = ' 1'
        string = ''

    embed = discord.Embed(title=f"Informacje o ruchu {move_name.title()}:", color=0x00ff00)
    embed.add_field(name="Typ", value=type_name)
    embed.add_field(name="Moc", value=power)
    embed.add_field(name="Celność", value=f"{accuracy}% {accuracy1}")
    embed.add_field(name="Priority", value=priority)
    embed.add_field(name="PP/Max PP", value=f"{pp}/{max_pp}")
    embed.add_field(name="Info", value=f"{effect} {string}")

    await message.channel.send(embed=embed)

  if message.content.startswith('$tutor'):
    await message.channel.send(f"Kanto: {Kanto} \n\nHoenn: {Hoenn} \n\nSinnoh: {Sinnoh} \n\nUnova: {Unova}")

  if message.content.startswith('$ability'):

    ability1 = message.content[9:].lower()
    if " " in ability1:
      ability1 = ability1.replace(" ", "-")
  
    response10 = requests.get(f'https://pokeapi.co/api/v2/ability/{ability1}/')
    data10 = response10.json()
    
    for item in data10["effect_entries"]:
    	info = item['effect']
      
    await message.channel.send(info)

  if message.content.startswith('$abils'):
    abilities = message.content.split(' ')
    abilities = str(abilities[1]).lower()

    if abilities == 'darmanitan':
      abilities = 'darmanitan-standard'
    if abilities == 'mr':
      abilities = 'mr-mime'

    abi_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{abilities}')
    abi_data = abi_response.json()
    abi_list = []
    
    for i in abi_data['abilities']:
      abi_name = i['ability']['name']
      if "-" in abi_name:
        abi_name = str(abi_name).replace('-', ' ')
      abi_list.append(abi_name)

    string = ' '
    n = len(abi_list)
    if n > 1:
      string = 'Ostatnia wyświetlona Abilitka jest Hidden!'
    
    char_remover = ["[", "]", "'"]
    for char in char_remover:
      abi_list = str(abi_list).replace(char, "")
    
    await message.channel.send(f"Abilitki Pokemona {abilities.title()}: \n{abi_list.title()} \n{string} \nJeśli chcesz przeczytać co dana Abilitka robi to wpisz: $ability nazwaability")

  if message.content.startswith("$pok"):
    poke = message.content.split(" ")[1].lower()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke}")
    data = response.json()

    abils = []
    tys = []
    
    for i in data['abilities']:
      ability = i['ability']['name'].replace("-", " ")
      hidden = i['is_hidden']
      if hidden == False:
          abils.append(ability)
      else:
          abils.append(f"{ability} (    7Y6HU\O9Hidden)")
  
    abils = "\n".join(abils).title()
    
    for i in data['types']:
        type = i['type']['name']
        tys.append(type)

    tys = "\n".join(tys).title()
    
    hp = dict(data['stats'][0])['base_stat']
    att = dict(data['stats'][1])['base_stat']
    deff = dict(data['stats'][2])['base_stat']
    spatt = dict(data['stats'][3])['base_stat']
    spdef = dict(data['stats'][4])['base_stat']
    speed = dict(data['stats'][5])['base_stat']
    
    embed = discord.Embed(title="", color=0x00ff00)
    embed.add_field(name="Typing", value=tys)
    embed.add_field(name="Abilitki", value=abils)
    embed.add_field(name="Base Staty", value=f"HP: {hp}\nAttack: {att}\nDeffense: {deff}\nSp. Attack: {spatt}\n Sp. Deffense: {spdef}\nSpeed: {speed}")
    # embed.set_thumbnail(url=pokemon.sprites.front_default)
    
    await message.channel.send(embed=embed)

  if message.content.startswith("$s"):
    survey = m[3:]
    await message.delete()
    message = await message.channel.send(survey)
    await message.add_reaction("\U00002705")
    await message.add_reaction("\U0000274c")

  if message.content.startswith("$china"):
    df = pd.read_csv('chinese_new_year_23.csv')
    
    df = df.to_string().replace(" ", "")
    df = df.split('\n')
    df = [i.split(';') for i in df]
    
    animal = []
    pokemons = {}
    
    for i in range(len(df)):
        if i > 0:
            animal.append(df[i][1])
    
    for i in range(len(df)):
        if i > 0:
            pokemons[str(i)] = []
            pokemons[str(i)].append(df[i][4:])
            for j in range(len(pokemons[str(i)][0])):
                try:
                    pokemons[str(i)][0].remove("")
                except:
                    pass
    
    for i in range(len(pokemons)):
        poke = str(pokemons[str(i+1)]).replace("[", "")
        poke = poke.replace("]", "")
        poke = poke.replace("'", "")
        pokemons[str(i+1)] = poke

    splited = ":".join(pokemons.values())
    splited = splited.split(":")

    pd.set_option('display.max_colwidth', 100)
    df1 = pd.DataFrame({" ": animal[:7], "": splited[:7]})
    df2 = pd.DataFrame({" ": animal[7:14], "": splited[7:14]})
    df3 = pd.DataFrame({" ": animal[14:21], "": splited[14:21]})
    df4 = pd.DataFrame({" ": animal[21:27], "": splited[21:27]})

    await message.channel.send(df1)
    await message.channel.send(df2)
    await message.channel.send(df3)
    await message.channel.send(df4)

keep_alive()

my_secret = os.environ["TOKEN"]
bot.run(my_secret)

