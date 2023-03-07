import random
import json

def color():
    # this program choose colors for the embed randomly
    color = (0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f,
             0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da, 0x99aab5)
    randclr = random.choice(color)
    return randclr

def file_open(file_name):
    if file_name.endswith(".txt") or file_name.endswith(".dat"):
        with open(file_name,"r") as txt:
            return txt.read()
    elif file_name.endswith(".json"):
        with open(file_name , "w") as js:
            return json.load(js)
    else:
        raise ValueError
            