import os
import discord
from datetime import datetime, timedelta
from discord.ext import commands
from data import Data, Quest, Shop
from keep_alive import keep_alive
from random import randint
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def rol(n):
  return randint(1, n)

@bot.command()
async def roll(n):
  return randint(1, n)


@bot.command()
async def bonjour(ctx):
  await ctx.send(f"Bonjour {ctx.author} !")


@bot.command()
async def salaire(ctx):
  data = Data(ctx.author)
  data.initia()

  aujourdhui = datetime.now()
  jour = data.salaire[0]
  mois = data.salaire[1]
  année = data.salaire[2]
  dernier_salaire = datetime(année, mois, jour)

  temps = aujourdhui - dernier_salaire

  if temps >= timedelta(weeks=1):
    data.honneurs += 1000
    data.honneurs = round(data.honneurs * 1.05)
    data.salaire = [aujourdhui.day, aujourdhui.month, aujourdhui.year]
    if data.alignement == 0:
      current_grade = None
      for grade, info in data.marine_ranks.items():
        if data.honneurs >= info["honneur"]:
          current_grade = grade

      if current_grade:
        salaire = data.marine_ranks[current_grade]["salaire"]
        await ctx.send(f"Votre salaire de {salaire:,} 💰 a été réclamé.")
        data.argent += salaire
        data.ajoute_db()
      else:
        await ctx.send("Aucun grade trouvé pour attribuer un salaire.")
    else:
      await ctx.send("Votre prime a augmenté !")
      data.ajoute_db()
  else:
    await ctx.send("Arrête de faire le rat comme ça la ")


@bot.command()
async def start(ctx, alignment, username):
  data = Data(ctx.author)
  data.ajouter_personne()
  data.initia()
  data.argent = rol(15000)
  data.honneurs = rol(150000)
  data.username = username
  if alignment == "pirate":
    data.alignement = 1
    data.ajoute_db()
    await ctx.send("Votre personnage a été créé avec succès !")
  elif alignment == "marine":
    data.alignement = 0
    data.ajoute_db()
    await ctx.send("Votre personnage a été créé avec succès !")
  else:
    await ctx.send("L'alignement n'existe pas.")


@bot.command(name="Al")
async def al(ctx):
  x = Data(ctx.author)
  x.initia()
  if x.alignement == 1:
    embed = discord.Embed(title="Pirate")
    embed.add_field(name="Prime", value=x.honneurs, inline=True)
  if x.alignement == 0:
    embed = discord.Embed(title="Marine")
    embed.add_field(name="Honneur", value=x.honneurs, inline=True)
    for grade, info in x.marine_ranks.items():
      if x.honneurs >= info["honneur"]:
        current_grade = grade
        current_grade_info = info
      else:
        next_grade = grade
        next_grade_honneur = info["honneur"]
        break
    else:
      next_grade = None

    embed.add_field(name="Grade actuel", value=current_grade, inline=True)
    if next_grade:
      embed.add_field(name="Prochain grade", value=next_grade, inline=False)
      embed.add_field(name="Honneur pour prochain grade",
                      value=next_grade_honneur,
                      inline=False)
    else:
      embed.add_field(name="Vous êtes au grade le plus élevé",
                      value="Chef de la Marine",
                      inline=True)
  await ctx.send(embed=embed)


@bot.command()
async def profile(ctx, user: discord.Member = None):
  if user is None:
    user = ctx.author

  data = Data(user)
  data.initia()
  embed = discord.Embed(title="Profile",
                        description="Voici votre profile",
                        color=0x00ff00)
  embed.add_field(name="Force", value=data.force, inline=True)
  embed.add_field(name="Endurance", value=data.endurance, inline=True)
  embed.add_field(name="Resistance", value=data.resistance, inline=True)
  embed.add_field(name="Vitesse", value=data.vitesse, inline=True)
  embed.add_field(name="Sagesse", value=data.sagesse, inline=True)
  embed.add_field(name="Haki Armement", value=data.armement, inline=True)
  embed.add_field(name="Haki Observation", value=data.observation, inline=True)
  embed.add_field(name="Haki Rois", value=data.rois, inline=True)
  embed.add_field(name="Maîtrise style de combat",
                  value=data.style,
                  inline=True)
  embed.add_field(name="Puissance FDD", value=data.fdd, inline=True)
  embed.add_field(name="Points à répartir", value=data.points, inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def inventaire(ctx, user: discord.Member = None):
  if user is None:
    user = ctx.author
  data = Data(user)
  data.initia()
  embed = discord.Embed(title="Inventaire",
                        description=str(data.argent) + " berrys",
                        color=0x00ff00)
  for i in data.inventaire:
    embed.add_field(name=i, value=1, inline=True)
  await ctx.send(embed=embed)


@bot.command()
async def alignment(ctx):
  data = Data(ctx.author)
  data.initia()
  if data.alignement == 1:
    data.alignement = 0
    data.honneurs = 0
    data.ajoute_db()
    await ctx.send("Vous êtes désormais un marine !")
  else:
    data.alignement = 1
    data.honneurs = round(data.honneurs * 1.2)
    data.ajoute_db()
    await ctx.send("Vous êtes désormais un pirate !")


@bot.command()
async def prime(ctx):
  data = Data(ctx.author)
  data.initia()
  liste = []
  embed = discord.Embed(title="Prime",
                        description="Voici la liste des pirates",
                        color=0x00ff00)
  with open('data.json', 'r') as f:
    try:
      data = json.load(f)
    except json.JSONDecodeError:
      data = {}
  cles_principales = list(data.keys())
  for i in cles_principales:
    if data[i][16] == 1:
      liste.append([data[i][18], data[i][15]])
  liste.sort(key=lambda x: x[1], reverse=True)
  for i in liste:
    embed.add_field(name=i[0], value=i[1], inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def honneur(ctx):
  data = Data(ctx.author)
  data.initia()
  liste = []
  embed = discord.Embed(title="Prime",
                        description="Voici la liste des marines",
                        color=0x00ff00)
  with open('data.json', 'r') as f:
    try:
      data = json.load(f)
    except json.JSONDecodeError:
      data = {}
  cles_principales = list(data.keys())
  for i in cles_principales:
    if data[i][16] == 0:
      liste.append([data[i][18], data[i][15]])
  liste.sort(key=lambda x: x[1], reverse=True)
  for i in liste:
    embed.add_field(name=i[0], value=i[1], inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def train(ctx):
  x = Data(ctx.author)
  x.ajouter_personne()
  x.initia()
  if x.train != 0:
    aujourdhui = datetime.now()
    jour = aujourdhui.day
    mois = aujourdhui.month
    année = aujourdhui.year
    if jour > x.date[0] or mois > x.date[1] or année > x.date[2]:
      x.train = 0
  if x.train != 2:
    x.train += 1
    if x.force + x.resistance + x.vitesse + x.sagesse + x.endurance < 250:
      x.points += round(5 * (1 + x.sagesse / 100))
    elif x.force + x.resistance + x.vitesse + x.sagesse + x.endurance < 600:
      x.points += round(10 * (1 + x.sagesse / 100))
    elif x.force + x.resistance + x.vitesse + x.sagesse + x.endurance < 2000:
      x.points += round(15 * (1 + x.sagesse / 100))
    else:
      x.points += round(20 * (1 + x.sagesse / 100))
    await ctx.send(
        f"Vous avez gagné {round(5 * (1 + x.sagesse / 100))} points !")
  else:
    await ctx.send(
        f"Vous avez perdu {round(5 * (1 + x.sagesse / 100))} points !")
  aujourdhui = datetime.now()
  x.date[0] = aujourdhui.day
  x.date[1] = aujourdhui.month
  x.date[2] = aujourdhui.year
  x.ajoute_db()


@bot.command()
async def add(ctx, stat, nb):
  x = Data(ctx.author)
  x.ajouter_personne()
  x.initia()
  nb = int(nb)
  if x.points >= nb:
    x.points -= nb
    if stat == "force":
      x.force += nb
    elif stat == "endurance":
      x.endurance += nb
    elif stat == "resistance":
      x.resistance += nb
    elif stat == "vitesse":
      x.vitesse += nb
    elif stat == "sagesse":
      x.sagesse += nb
    elif stat == "fdd":
      x.fdd += nb
    elif stat == "points":
      x.points += nb
    else:
      await ctx.send("Cette statistique n'existe pas !")
    x.ajoute_db()
    await ctx.send(f"Vous avez ajouté {nb} points à {stat} !")
  else:
    await ctx.send("Vous n'avez pas assez de points pour ajouter cela")


@bot.command(name="admin-add")
@commands.has_permissions(administrator=True)
async def add1(ctx, stat, nb: int, user: discord.Member):
  x = Data(user)
  x.initia()

  if hasattr(x, stat):
    current_value = getattr(x, stat)
    setattr(x, stat, current_value + nb)

    x.ajoute_db()

    await ctx.send(
        f"✅ {ctx.author.mention} a ajouté **{nb}** points à la statistique `{stat}` de {user.mention} !"
    )
  else:
    await ctx.send(
        f"❌ {ctx.author.mention}, la statistique `{stat}` n'existe pas pour {user.mention}."
    )


@add1.error
async def add1_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        f"❌ {ctx.author.mention}, vous n'avez pas la permission requise pour exécuter cette commande (Administrateur nécessaire)."
    )


"""Toute la partie Shop """


@bot.command(name="shop")
async def display_shop(ctx):
  shops = Shop()
  shops.initia()
  shop = shops.all_object

  embed = discord.Embed(
      title="🛒 Shop",
      description="Voici la liste des objets disponibles :",
      color=discord.Color.blue(),
  )
  for item, details in shop.items():
    price = details["price"]
    description = details["description"]

    embed.add_field(
        name=f"{item} - {price:,} 💰",
        value=description,
        inline=False,
    )
  await ctx.send(embed=embed)


@bot.command(name="sell")
async def Sale_item(ctx, item_name):
    data = Data(ctx.author)
    data.initia()
    shop = Shop()
    shop.initia()
    shop_items = shop.all_object

    # Vérifier si l'objet existe dans le magasin
    if item_name not in shop_items:
      await ctx.send("Cet objet n'existe pas dans le magasin !")
      return

    # Vérifier si l'utilisateur possède l'objet
    for i in range(len(data.inventaire)):
      if item_name == str(data.inventaire[i]):  # Adaptez ici si nécessaire
        item_details = shop_items[item_name]
        price = item_details["price"]

        # Supprimer l'objet et ajouter l'argent
        data.argent += price // 2
        data.inventaire.pop(i)  # Supprimer l'objet
        data.ajoute_db()  # Sauvegarder les changements
        await ctx.send(f"Vous avez vendu {item_name} pour {price // 2:,} 💰.")
        break
    else:
      await ctx.send("L'objet n'est pas dans votre inventaire !")


@bot.command(name="buy")
async def buy_item(ctx, *, item_name=None):
  x = Data(ctx.author)
  x.initia()
  shops = Shop()
  shops.initia()
  shop = shops.all_object
  if not item_name:
    await ctx.send(
        f"❌ {ctx.author.mention}, veuillez préciser l'objet que vous souhaitez acheter. Utilisez `!shop` pour voir les objets disponibles."
    )
    return
  item1 = ""
  item_name = item_name.lower()
  found_item = None
  for item in shop.keys():
    item1 = item.replace(" ", "")
    if item.lower() == item_name or item1 == item_name:
      found_item = item
      break

  if found_item:
    if x.argent >= shop[found_item]["price"]:
      x.argent -= shop[found_item]["price"]
      if found_item == "Sabre random":
        rarity = rol(100)
        if rarity <= 6:
          found_item = "Ryo O'Wazamono"
        else:
          found_item = "Sabre basique"
      price = shop[found_item]["price"]
      await ctx.send(
          f"🎉 {ctx.author.mention}, vous avez acheté **{found_item}** pour **{price} 💰**!"
      )
      x.inventaire.append(found_item)
      x.ajoute_db()
    else:
      await ctx.send(
          f"❌ {ctx.author.mention}, vous n'avez pas assez d'argent pour acheter **{found_item}**."
      )
  else:
    await ctx.send(
        f"❌ {ctx.author.mention}, cet objet n'existe pas dans le shop.")


@bot.command(name="add_shop")
@commands.has_permissions(administrator=True)
async def add_shop(ctx, item_name, price):
  shops = Shop()
  shops.initia()
  shop = shops.all_object
  if item_name in shop:
    await ctx.send(f"❌ L'objet **{item_name}** existe déjà dans le shop.")
  else:
    shop[item_name]["price"] = int(price)
    shops.save()
    await ctx.send(
        f"✅ L'objet **{item_name}** a été ajouté au shop avec un prix de {price} 💰."
    )


@add_shop.error
async def add_shop_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        f"❌ {ctx.author.mention}, vous n'avez pas la permission requise pour exécuter cette commande (Administrateur nécessaire)."
    )


@bot.command(name="del")
@commands.has_permissions(administrator=True)
async def Del(ctx, item_name):
  shops = Shop()
  shops.initia()
  if item_name in shops.all_object:
    del shops.all_object[item_name]
    shops.save()
    await ctx.send(f"✅ L'objet **{item_name}** a été retiré du shop.")


@Del.error
async def Del_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        f"❌ {ctx.author.mention}, vous n'avez pas la permission requise pour exécuter cette commande (Administrateur nécessaire)."
    )


@bot.command(name="del_user")
@commands.has_permissions(administrator=True)
async def Del_user(ctx, user: discord.Member):
  users = user.name
  data = Data(users)
  data.initia()
  with open("data.json", "r") as f:
    datas = json.load(f)
  del datas[users]
  with open("data.json", "w") as f:
    json.dump(datas, f, indent=4)


@bot.command(name="add_quest")
@commands.has_permissions(administrator=True)
async def add_quest(ctx, quest_name, points, berrys, honneur):
  quest = Quest()
  quest.initia()
  quests = quest.quests
  if quest_name in quests:
    await ctx.send(f"❌ La quête **{quest_name}** existe déjà.")
  else:
    quests[str(quest_name)] = {
        "points": points,
        "berrys": berrys,
        "honneur/prime": honneur
    }
    quest.save()
    await ctx.send(
        f"✅ La quête **{quest_name}** a été ajouté aux quêtes avec une récompense de {points} points, {berrys} berrys et {honneur} d'honneur ou de prime."
    )


@add_quest.error
async def add_quest_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        f"❌ {ctx.author.mention}, vous n'avez pas la permission requise pour exécuter cette commande (Administrateur nécessaire)."
    )


@bot.command(name="delq")
@commands.has_permissions(administrator=True)
async def Delq(ctx, quest_name):
  quest = Quest()
  quest.initia()
  if quest_name in quest.quests:
    del quest.quests[quest_name]
    quest.save()
    await ctx.send(f"✅ La quête **{quest_name}** a été supprimée.")


@Delq.error
async def Delq_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        f"❌ {ctx.author.mention}, vous n'avez pas la permission requise pour exécuter cette commande (Administrateur nécessaire)."
    )

@bot.command()
async def Memory(ctx):
  with open('data.json', 'r') as f:
    try:
      data = json.load(f)
    except json.JSONDecodeError:
      data = {}
  await ctx.send(f"{data}")


@bot.command(name="quest")
async def display_quest(ctx):
  quest = Quest()
  quest.initia()
  quests = quest.quests

  embed = discord.Embed(
      title="Quêtes",
      description="Voici la liste des quêtes :",
      color=discord.Color.blue(),
  )
  for item, details in quests.items():
    points = details["points"]
    berrys = details["berrys"]
    honneurs = details["honneur/prime"]

    embed.add_field(
        name=f"{item}",
        value=
        f"Récompenses : {points} points, {berrys} berrys, {honneurs} d'honneur ou de prime",
        inline=False,
    )
  await ctx.send(embed=embed)

keep_alive()
bot.run("MTMwODUxNjYwMDAwNTEzMjQxOA.GofXHP.04x2UtlLoZr-d3qr1a3C_7Hg1HucJzfdc6303w")
