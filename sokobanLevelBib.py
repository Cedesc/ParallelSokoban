import random

Z_REIHEN = 10
Z_SPALTEN = 10
Z_WK_SCHWARZE_FELDER = 20

""" Beispiel-Level """

# vorgegebenes Beispiel-Level

beispielLevel1 = [
            [1, 1, 1, 1, 1, 1, 4, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 3, 1, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

beispielLevel2 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 1, 1],
            [1, 0, 2, 3, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 4],
            [1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

beispielLevel3 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 3, 2, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1],
            [4, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

beispielLevel4 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 3, 2, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 4, 1, 1, 1, 1, 1, 1]
           ]

beispielLevel = [beispielLevel1, beispielLevel2, beispielLevel3, beispielLevel4]


# einfaches Level zum testen

einfachesLevel1 = [
            [1, 1, 1, 1, 1, 1, 4, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

einfachesLevel2 = [
            [1, 1, 1, 1, 1, 1, 4, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

einfachesLevel3 = [
            [1, 1, 1, 1, 1, 1, 4, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

einfachesLevel4 = [
            [1, 1, 1, 1, 1, 1, 4, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
           ]

einfachesLevel = [einfachesLevel1, einfachesLevel2, einfachesLevel3, einfachesLevel4]


# kleines selbsterstelltes Level

kleineLevel1 = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 3, 0, 1],
            [1, 0, 2, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 4, 1]
]

kleineLevel2 = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 3, 0, 1],
            [1, 0, 2, 0, 1],
            [1, 0, 0, 0, 4],
            [1, 1, 1, 1, 1]
]

kleineLevel3 = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 3, 1, 1],
            [1, 0, 2, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 4, 1]
]

kleineLevel4 = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 3, 0, 1],
            [1, 0, 2, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 4, 1]
]

kleineLevel = [kleineLevel1, kleineLevel2, kleineLevel3, kleineLevel4]



anderesLevel1 = [
            [1, 1, 1, 1, 4, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 3, 1, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
           ]

anderesLevel2 = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1],
            [1, 2, 3, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 4],
            [1, 1, 1, 1, 1, 1, 1]
           ]

anderesLevel3 = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 2, 3, 0, 0, 0, 4],
            [1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
           ]

anderesLevel4 = [
            [1, 1, 1, 1, 4, 1, 1],
            [1, 2, 3, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1]
           ]

anderesLevel = [anderesLevel1, anderesLevel2, anderesLevel3, anderesLevel4]




def zufaelligesLevelErstellen(weite, hoehe, schwarzWahrscheinlichkeit):
    feld = []

    # schwarze und weisse Felder einfuegen
    for y in range(hoehe):
        reihe = []
        for x in range(weite):
            if x == 0 or y == 0 or x == weite-1 or y == hoehe-1:
                reihe.append(1)
                continue
            else:
                if random.randint(0,100) <= schwarzWahrscheinlichkeit:
                    reihe.append(1)
                else:
                    reihe.append(0)
        feld.append(reihe)

    # Spieler, Kiste und Ziel einfuegen
    xPosition = random.randint(1, weite-2)
    yPosition = random.randint(1, hoehe-2)
    feld[yPosition][xPosition] = 2
    while feld[yPosition][xPosition] == 2:
        xPosition = random.randint(1, weite - 2)
        yPosition = random.randint(1, hoehe - 2)
    feld[yPosition][xPosition] = 3

    z = random.randint(0, 3)
    if z == 0:
        feld[0][random.randint(1, weite - 2)] = 4
    elif z == 1:
        feld[weite-1][random.randint(1, weite - 2)] = 4
    elif z == 2:
        feld[random.randint(1, hoehe - 2)][0] = 4
    elif z == 3:
        feld[random.randint(1, hoehe - 2)][hoehe-1] = 4


    return feld

erstelltesLevel = [zufaelligesLevelErstellen(Z_REIHEN, Z_SPALTEN, Z_WK_SCHWARZE_FELDER) for x in range(4)]
