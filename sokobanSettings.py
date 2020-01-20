import sokobanLevelBib

""" Spiel-Settings """
FENSTERBREITE = 1000
FENSTERHOEHE = 800
ANZAHLREIHEN = 15
ANZAHLSPALTEN = 15
SCHWIERIGKEIT = -1000


VORGEFERTIGTESLEVEL = sokobanLevelBib.beispielLevel

LEVEL = VORGEFERTIGTESLEVEL





"""
KI Idee:

    moeglicheWege = [ [ (spielerP, kisteP ] ]

    hilfsliste = [ (spielerP, kisteP) ]       # der hilfsliste ein tupel aus spieler und kistenposition hinzufuegen
    
    while True:
        
        eingefuegt = False           # gibt an ob von diesem Punkt aus mindestens ein naechster Punkt hinzugefuegt wurde
        
        moeglicheWegeKopie = copy.deepcopy(moeglicheWege)
        
        moeglicheWege = []
        
        for welcherWeg in range(len(moeglicheWegeKopie)):
        
            for richtung in [oben, rechts, unten, links]:       # jede richtung abgehen
                
                momentanePositionen = moeglicheWegeKopie[welcherWeg][-1]
                
                naechstePosition = richtung()                   # oben, rechts, unten, links gibt jeweils tupel mit spieler und kistenposition aus
                
                if naechstePosition not in hilfsliste:
                    
                    moeglicheWegeKopie[welcherWeg].append(naechstePosition)
                    
                    moeglicheWege.append(moeglicheWegeKopie[welcherWeg])
                        
                    hilfsliste.append( (spielerP, kisteP) )
                        
                    eingefuegt = True
    
        
        wenn zielpunkt erreicht wurde: aufhoeren und liste, die diesen punkt beinhaltet, ausgeben

"""

#                    wenn nein und erster eintrag fuer die liste: fuege punkt der gemachte zuege liste hinzu und fuege hilfsliste hinzu
#                    wenn nein und nicht erster eintrag: erstelle kopie der momentanen liste und ersetze das letzte element mit dem punkt und fuege hilfsliste hinzu

#        wenn kein neuer eintrag gemacht wurde, loesche die momentane liste        EDIT: nicht noetig da gar nich hinzugefuegt wird