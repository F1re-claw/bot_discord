import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from io import BytesIO


class Data:

    def __init__(self, user):
        self.user = str(user)
        self.fichier_json = "./data.json"
        self.data = {}
        self.marine_ranks = {
            "Recrue": {
                "honneur": 0,
                "salaire": 20000
            },
            "Troisieme Classe": {
                "honneur": 20000,
                "salaire": 35000
            },
            "Seconde Classe": {
                "honneur": 55000,
                "salaire": 60000
            },
            "Première Classe": {
                "honneur": 100000,
                "salaire": 100000
            },
            "Caporal": {
                "honneur": 500000,
                "salaire": 200000
            },
            "Sergent": {
                "honneur": 1000000,
                "salaire": 400000
            },
            "Sergent-Chef": {
                "honneur": 2000000,
                "salaire": 600000
            },
            "Adjudant": {
                "honneur": 5000000,
                "salaire": 800000
            },
            "Adjudant-Chef": {
                "honneur": 10000000,
                "salaire": 1000000
            },
            "Sous-Lieutenant": {
                "honneur": 20000000,
                "salaire": 2000000
            },
            "Vice-Lieutenant": {
                "honneur": 35000000,
                "salaire": 3000000
            },
            "Lieutenant": {
                "honneur": 50000000,
                "salaire": 5000000
            },
            "Lieutenant-Commandant": {
                "honneur": 100000000,
                "salaire": 7500000
            },
            "Commandant": {
                "honneur": 200000000,
                "salaire": 10000000
            },
            "Colonel": {
                "honneur": 400000000,
                "salaire": 15000000
            },
            "Sous-Amiral": {
                "honneur": 700000000,
                "salaire": 20000000
            },
            "Contre-amiral": {
                "honneur": 1300000000,
                "salaire": 25000000
            },
            "Vice-amiral": {
                "honneur": 2000000000,
                "salaire": 35000000
            },
            "Amiral": {
                "honneur": 4000000000,
                "salaire": 50000000
            },
            "Amiral en Chef": {
                "honneur": 5000000000,
                "salaire": 65000000
            },
            "Chef de la Marine": {
                "honneur": 8000000000,
                "salaire": 90000000
            }
        }

        self.liste = [
            "force", "endurance", "resistance", "vitesse", "sagesse",
            "haki de l'armement", "haki de l'observation", "haki des rois",
            "maîtrise style de combat", "maîtrise du fdd", "Argent",
            "points à attribuer", "train", "date", "Inventaire", "honneurs",
            "alignement", "salaire", "username"
        ]
        aujourdhui = datetime.now()
        self.liste_value = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0,
            [aujourdhui.day, aujourdhui.month, aujourdhui.year], [], 0, 1,
            [aujourdhui.day, aujourdhui.month - 1, aujourdhui.year], ""
        ]
        self.nb_variables = len(self.liste)
        self.username = ""
        self.force = 0
        self.endurance = 0
        self.resistance = 0
        self.vitesse = 0
        self.sagesse = 0
        self.armement = 0
        self.observation = 0
        self.rois = 0
        self.style = 0
        self.fdd = 0
        self.argent = 0
        self.points = 50
        self.train = 0
        self.date = [0, 0, 0]
        self.inventaire = []
        self.honneurs = 0
        self.alignement = 0
        self.salaire = []

    def ajouter_personne(self):
        if not os.path.exists('data.json'):
            with open('data.json', 'w') as f:
                json.dump({}, f)

        with open('data.json', 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        if self.user not in data:
            data[self.user] = self.liste_value

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def initia(self):
        self.add()
        with open(self.fichier_json, "r") as fichier:
            self.data = json.load(fichier)
        if self.user in self.data:
            stats = self.data[self.user]
            self.force = stats[0]
            self.endurance = stats[1]
            self.resistance = stats[2]
            self.vitesse = stats[3]
            self.sagesse = stats[4]
            self.armement = stats[5]
            self.observation = stats[6]
            self.rois = stats[7]
            self.style = stats[8]
            self.fdd = stats[9]
            self.argent = stats[10]
            self.points = stats[11]
            self.train = stats[12]
            self.date = stats[13]
            self.inventaire = stats[14]
            self.honneurs = stats[15]
            self.alignement = stats[16]
            self.salaire = stats[17]
            self.username = stats[18]
        else:
            print("Identifiant introuvable dans les donnees.")

    def ajoute_db(self):
        self.stats = [
            self.force, self.endurance, self.resistance, self.vitesse,
            self.sagesse, self.armement, self.observation, self.rois,
            self.style, self.fdd, self.argent, self.points, self.train,
            self.date, self.inventaire, self.honneurs, self.alignement,
            self.salaire, self.username
        ]

        try:
            with open(self.fichier_json, "r") as fichier:
                data = json.load(fichier)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[self.user] = self.stats

        with open(self.fichier_json, "w") as fichier:
            json.dump(data, fichier, indent=4)

    def add(self):
        try:
            with open(self.fichier_json, 'r') as f:
                donnees = json.load(f)
        except FileNotFoundError:
            donnees = {}
        except json.JSONDecodeError:
            raise ValueError("Le fichier JSON est corrompu.")

        stats = donnees.get(self.user, [])

        if len(stats) != self.nb_variables:
            deficit = self.nb_variables - len(stats)
            for i in range(self.nb_variables - deficit, self.nb_variables):
                stats.append(self.liste_value[i])
            donnees[self.user] = stats
            with open(self.fichier_json, "w") as f:
                json.dump(donnees, f, indent=4)

    def affichage(self):
        prime = Image.open("images/prime.jpg")
        font_path = "images/one piece font.ttf"
        font_size = 18
        font = ImageFont.truetype(font_path, font_size)
        image_to_insert = Image.open(f"images/{self.user}.jpg")
        image_to_insert = image_to_insert.resize((110, 83))

        draw = ImageDraw.Draw(prime)

        prime_coordinates = [22, 165, 120, 182]
        nom_coordinates = [14, 146, 121, 164]

        width, height = 110, 83
        x, y = 14, 45
        coordinates = [x, y, x + width, y + height]

        draw.text((prime_coordinates[0] + 5, prime_coordinates[1] + 2),
                  str(self.honneurs),
                  fill=(0, 0, 0),
                  font=font)
        draw.text((nom_coordinates[0] + 5, nom_coordinates[1] + 2),
                  self.username,
                  fill=(0, 0, 0),
                  font=font)

        prime.paste(image_to_insert, (x, y))

        image_binary = BytesIO()
        prime.save(image_binary, format="JPEG")
        image_binary.seek(0)

        return image_binary


class Shop:

    def __init__(self):
        self.all_object = {
            "Barque": {
                "price": 1000,
                "description": "Un petit bateau pour naviguer sur l'eau.",
            },
            "Petit bateau": {
                "price":
                10000,
                "description":
                "Un bateau un peu plus spacieux pour vos aventures.",
            },
            "Petite dynamite": {
                "price":
                10000,
                "description":
                "Explosif pratique pour ouvrir des chemins ou neutraliser des obstacles.",
            },
            "Sabre basique": {
                "price":
                20000,
                "description":
                "Un sabre standard, idéal pour débuter dans le maniement des armes.",
            },
            "Sabre random": {
                "price":
                100000,
                "description":
                "Un sabre avec des caractéristiques aléatoires. Peut-être une perle rare ?",
            },
            "Bateau moyen": {
                "price":
                100000,
                "description":
                "Un bateau confortable pouvant accueillir une petite équipe.",
            },
            "Petit Appartement": {
                "price":
                100000,
                "description":
                "Un appartement modeste, idéal pour investir ou se reposer.",
            },
            "Magasin": {
                "price":
                1000000,
                "description":
                "Un magasin pour démarrer une activité commerciale rentable.",
            },
            "Escargophone": {
                "price": 2000000,
                "description":
                "Un dispositif de communication longue distance.",
            },
            "Ryo O'Wazamono": {
                "price":
                2000000,
                "description":
                "Un sabre de haute qualité, réservé aux experts du combat.",
            },
            "Sabre2": {
                "price":
                10000000,
                "description":
                "Un sabre rare avec 10% de chances d'être un O'Wazamono.",
            },
            "Casino": {
                "price":
                100000000,
                "description":
                "Investissez dans un casino et récoltez des bénéfices importants.",
            },
            "PetitFDD": {
                "price":
                150000000,
                "description":
                "Un fruit du démon aléatoire (paramecia ou zoan naturel).",
            },
            "O'Wazamono": {
                "price":
                200000000,
                "description":
                "Un sabre d'exception parmi les meilleurs du monde.",
            },
            "GrandFDD": {
                "price":
                400000000,
                "description":
                "Un fruit du démon aléatoire (paramecia, zoan naturel ou logia).",
            },
            "Logia": {
                "price":
                1500000000,
                "description":
                "Un fruit du démon de type logia, d'une puissance exceptionnelle.",
            },
        }

    def save(self):
        with open("shop.json", "w") as fichier:
            json.dump(self.all_object, fichier, indent=4)

    def initia(self):
        with open("shop.json", "r") as fichier:
            self.all_object = json.load(fichier)


class Quest:

    def __init__(self):
        self.quests = {
            "Tuer 10 pirates": {
                "price": 10,
                "description": 1000,
            }
        }

    def save(self):
        with open("quest.json", "w") as fichier:
            json.dump(self.quests, fichier, indent=4)

    def initia(self):
        with open("quest.json", "r") as fichier:
            self.quests = json.load(fichier)


class Backup:

    def __init__(self):
        self.datas = {}

    def save(self):
        with open("data.json", "r") as f:
            self.datas = json.load(f)
        with open("backup.json", "w") as f:
            json.dump(self.datas, f, indent=4)

    def init_dict(self):
        with open("backup.json", "r") as f:
            self.datas = json.load(f)
        return self.datas
