import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import copy
import sokobanSettings as ss
import sokobanLevelBib as slb


""" 
Erklaerung: 
    - 0 entspricht leerem Feld
    - 1 entspricht Wand
    - 2 entspricht Spieler
    - 3 entspricht Kiste
"""


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.kiFeldnummer1Feld = ss.einFeldKI
        self.kiFeldnummer2Felder = ss.zweiFeldKI

        self.echtewW = ss.FENSTERBREITE
        self.echtewH = ss.FENSTERHOEHE
        self.wW = ss.FENSTERBREITE // 2       # wW = windowWidth
        self.wH = ss.FENSTERHOEHE // 2        # wH = windowHeight
        self.setGeometry(800, 30, self.echtewW, self.echtewH)
        self.setWindowTitle("Paralleles Sokoban")
        self.verschiebungNachUnten = self.wH // 8  # Gesamtverschiebung nach unten
        self.verschiebungNachRechts = self.wW // 8  # Gesamtverschiebung nach rechts

        self.level = copy.deepcopy(ss.LEVEL)
        self.anzahlZeilen = len(self.level[0])
        self.anzahlSpalten = len(self.level[0][0])
        self.levelKoordinaten = self.koordinatenBestimmen()
        self.spielerPosition = self.positionenBestimmenSpieler()
        self.kistePosition = self.positionenBestimmenKiste()
        self.zielPosition = self.positionBestimmenZiel()

        # 2 und 3 entfernen aus Level
        for n in range(4):
            self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
            self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0

        self.gewonnen = [False, False, False, False]
        # self.gemachteZuege enthaelt jede vergangene Position von Spieler und Kiste von jedem Feld
        self.gemachteZuege = [copy.deepcopy((self.spielerPosition, self.kistePosition))]

        # kiLoesung enthaelt jedes Feld und die dazugehoerige Lage der Kiste dazu fuer die optimale Loesung
        self.kiLoesung = None
        self.kiBewegungVorlage = None
        self.kiZaehler = 0

        self.keyPressEvent = self.fn

        self.timer = QTimer()
        self.timer.timeout.connect(self.gravitation)
        self.timer.start(2000)

        self.show()

    def gravitation(self):
        # self.nachUntenBewegen()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        raeudigeVerschiebungX = 0
        raeudigeVerschiebungY = 0
        for n in range(4):
            if n == 1:
                raeudigeVerschiebungX = self.wW
            if n == 2:
                raeudigeVerschiebungX = 0
                raeudigeVerschiebungY = self.wH
            if n == 3:
                raeudigeVerschiebungX = self.wW


            ''' Hintergrund '''
            painter.fillRect(0 + raeudigeVerschiebungX, 0 + raeudigeVerschiebungY,
                             self.wW + raeudigeVerschiebungX, self.wH + raeudigeVerschiebungY, QColor(205, 205, 205))
            if self.gewonnen[n]:
                painter.fillRect(0 + raeudigeVerschiebungX, 0 + raeudigeVerschiebungY,
                             self.wW + raeudigeVerschiebungX, self.wH + raeudigeVerschiebungY, QColor(155, 205, 155))


            ''' Netz aufbauen '''
            painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))

            # hoehe und breite eines Felds
            hoehe = (self.wH - 2 * self.verschiebungNachUnten) // self.anzahlZeilen
            breite = (self.wW - 2 * self.verschiebungNachRechts) // self.anzahlSpalten


            # vertikale Linien
            for verschiebung in range(self.anzahlSpalten + 1):
                painter.drawLine(self.verschiebungNachRechts + breite * verschiebung + raeudigeVerschiebungX,
                                 self.verschiebungNachUnten + raeudigeVerschiebungY,
                                 self.verschiebungNachRechts + breite * verschiebung + raeudigeVerschiebungX,
                                 self.wH - self.verschiebungNachUnten - 8 + raeudigeVerschiebungY)

            # horizontale Linien
            for verschiebung in range(self.anzahlZeilen + 1):
                painter.drawLine(self.verschiebungNachRechts + raeudigeVerschiebungX,
                                 self.verschiebungNachUnten + hoehe * verschiebung + raeudigeVerschiebungY,
                                 self.wW - self.verschiebungNachRechts - 2 + raeudigeVerschiebungX,
                                 self.verschiebungNachUnten + hoehe * verschiebung + raeudigeVerschiebungY)


            """ Level zeichnen """
            painter.setPen(QPen(QColor(200, 0, 0), 3, Qt.SolidLine))
            for i in range(self.anzahlZeilen):

                for j in range(self.anzahlSpalten):

                    if self.level[n][i][j] == 1:
                        painter.fillRect(self.levelKoordinaten[i][j][0][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][0][1] + raeudigeVerschiebungY,
                                         self.levelKoordinaten[i][j][1][0] - self.levelKoordinaten[i][j][0][0], # hoehe
                                         self.levelKoordinaten[i][j][1][1] - self.levelKoordinaten[i][j][0][1], # weite
                                         QColor(0,0,0))

                    """if self.level[n][i][j] == 2:
                        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
                        painter.setBrush(QColor(100, 255, 100))
                        painter.drawEllipse(self.levelKoordinaten[i][j][0][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][0][1] + raeudigeVerschiebungY,
                                         self.levelKoordinaten[i][j][1][0] - self.levelKoordinaten[i][j][0][0],
                                         self.levelKoordinaten[i][j][1][1] - self.levelKoordinaten[i][j][0][1])"""



                    """if self.level[n][i][j] == 3:
                        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
                        painter.setBrush(QColor(220, 220, 0))
                        painter.drawRect(self.levelKoordinaten[i][j][0][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][0][1] + raeudigeVerschiebungY,
                                         self.levelKoordinaten[i][j][1][0] - self.levelKoordinaten[i][j][0][0],  # hoehe
                                         self.levelKoordinaten[i][j][1][1] - self.levelKoordinaten[i][j][0][1])
                        painter.drawLine(self.levelKoordinaten[i][j][0][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][0][1] + raeudigeVerschiebungY,
                                         self.levelKoordinaten[i][j][1][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][1][1] + raeudigeVerschiebungY)
                        painter.drawLine(self.levelKoordinaten[i][j][0][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][1][1] + raeudigeVerschiebungY,
                                         self.levelKoordinaten[i][j][1][0] + raeudigeVerschiebungX,
                                         self.levelKoordinaten[i][j][0][1] + raeudigeVerschiebungY)"""

            """ Spieler zeichnen """
            painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
            painter.setBrush(QColor(100, 255, 100))
            xKoordinateSpieler = self.spielerPosition[n][0]
            yKoordinateSpieler = self.spielerPosition[n][1]
            painter.drawEllipse(self.levelKoordinaten[xKoordinateSpieler][yKoordinateSpieler][0][0] + raeudigeVerschiebungX,
                                self.levelKoordinaten[xKoordinateSpieler][yKoordinateSpieler][0][1] + raeudigeVerschiebungY,
                                self.levelKoordinaten[xKoordinateSpieler][yKoordinateSpieler][1][0] - self.levelKoordinaten[xKoordinateSpieler][yKoordinateSpieler][0][0],
                                self.levelKoordinaten[xKoordinateSpieler][yKoordinateSpieler][1][1] - self.levelKoordinaten[xKoordinateSpieler][yKoordinateSpieler][0][1])

            """ Kiste zeichnen """
            painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            painter.setBrush(QColor(220, 220, 0))
            xKoordinateKiste = self.kistePosition[n][0]
            yKoordinateKiste = self.kistePosition[n][1]
            painter.drawRect(self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][0] + raeudigeVerschiebungX,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][1] + raeudigeVerschiebungY,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][1][0] - self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][0],  # hoehe
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][1][1] - self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][1])
            painter.drawLine(self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][0] + raeudigeVerschiebungX,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][1] + raeudigeVerschiebungY,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][1][0] + raeudigeVerschiebungX,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][1][1] + raeudigeVerschiebungY)
            painter.drawLine(self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][0] + raeudigeVerschiebungX,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][1][1] + raeudigeVerschiebungY,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][1][0] + raeudigeVerschiebungX,
                             self.levelKoordinaten[xKoordinateKiste][yKoordinateKiste][0][1] + raeudigeVerschiebungY)


    def fn(self, e):

        # H druecken um Steuerung anzeigen zu lassen
        if e.key() == Qt.Key_H:
            print(""" Steuerung :
            Escape :  Fenster schliessen 
            R :  Level resetten
            Z :  einen Schritt zurueckgehen
            Q :  1-Feld-KI Berechnung
            W :  1-Feld-KI Ausfuehrung
            1 :  2-Feld-KI Berechnung
            2 :  2-Feld-KI Ausfuehrung
            +/- :  Feld aendern, auf das die 1-Feld-KI abzielt
            P :  zufaelliges Feld berichtigen - 1 Schritt
            O :  zufaelliges Feld berichtigen - komplett""")

        # esc druecken um Level zu schliessen
        if e.key() == Qt.Key_Escape:
            self.close()

        # R druecken um Level zu resetten
        if e.key() == Qt.Key_R:
            self.levelReset()
            self.update()

        # Z druecken um einen Schritt zurueckzugehen
        if e.key() == Qt.Key_Z:
            self.schrittZurueck()
            self.update()

        # nach links bewegen
        if e.key() == Qt.Key_Left:
            for n in range(4):
                self.nachLinksBewegen(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()

        # nach rechts bewegen
        if e.key() == Qt.Key_Right:
            for n in range(4):
                self.nachRechtsBewegen(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()

        # nach oben bewegen
        if e.key() == Qt.Key_Up:
            for n in range(4):
                self.nachObenBewegen(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()

        # nach unten bewegen
        if e.key() == Qt.Key_Down:
            for n in range(4):
                self.nachUntenBewegen(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()


        # Q druecken um KI durchlaufen zu lassen
        if e.key() == Qt.Key_Q:
            self.kiLoesung = self.kiSchritt(self.kiFeldnummer1Feld)
            #self.kiLoesung = self.kiSchritt(int(input("Das wievielte Feld soll berechnet werden? ")))
            self.kiBewegungVorlage = self.kiBewegungVorlageErstellen(self.kiLoesung)
            print(self.kiBewegungVorlage)

        # W druecken um bei der optimalen Loesung einen Schritt weiterzugehen
        if e.key() == Qt.Key_W:
            if len(self.kiBewegungVorlage) <= self.kiZaehler:
                print("Bewegungsliste komplett durchgegangen")
            else:
                if self.kiBewegungVorlage[self.kiZaehler] == "oben":
                    self.nachObenBewegen(self.kiFeldnummer1Feld)
                if self.kiBewegungVorlage[self.kiZaehler] == "rechts":
                    self.nachRechtsBewegen(self.kiFeldnummer1Feld)
                if self.kiBewegungVorlage[self.kiZaehler] == "unten":
                    self.nachUntenBewegen(self.kiFeldnummer1Feld)
                if self.kiBewegungVorlage[self.kiZaehler] == "links":
                    self.nachLinksBewegen(self.kiFeldnummer1Feld)
                self.kiZaehler += 1
                self.update()


        # 1 druecken um KI auf 2 Feldern durchlaufen zu lassen
        if e.key() == Qt.Key_1:
            self.kiLoesung = self.kiSchritt2Felder(self.kiFeldnummer2Felder[0], self.kiFeldnummer2Felder[1])
            self.kiBewegungVorlage = self.kiBewegungVorlageErstellen2Felder(self.kiLoesung)
            print(self.kiBewegungVorlage)

        # 2 druecken um bei der optimalen Loesung fuer 2 Felder einen Schritt weiterzugehen
        if e.key() == Qt.Key_2:
            if len(self.kiBewegungVorlage) <= self.kiZaehler:
                print("Bewegungsliste komplett durchgegangen")
            else:
                if self.kiBewegungVorlage[self.kiZaehler] == "oben":
                    self.nachObenBewegen(self.kiFeldnummer2Felder[0])
                    self.nachObenBewegen(self.kiFeldnummer2Felder[1])
                if self.kiBewegungVorlage[self.kiZaehler] == "rechts":
                    self.nachRechtsBewegen(self.kiFeldnummer2Felder[0])
                    self.nachRechtsBewegen(self.kiFeldnummer2Felder[1])
                if self.kiBewegungVorlage[self.kiZaehler] == "unten":
                    self.nachUntenBewegen(self.kiFeldnummer2Felder[0])
                    self.nachUntenBewegen(self.kiFeldnummer2Felder[1])
                if self.kiBewegungVorlage[self.kiZaehler] == "links":
                    self.nachLinksBewegen(self.kiFeldnummer2Felder[0])
                    self.nachLinksBewegen(self.kiFeldnummer2Felder[1])
                self.kiZaehler += 1
                self.update()


        # + druecken um Feld zu erhoehen, auf das die 1-Feld-KI abzielt
        if e.key() == Qt.Key_Plus:
            self.kiFeldnummer1Feld = (self.kiFeldnummer1Feld + 1) % 4
            print("KI-Zeiger nun auf :  ", self.kiFeldnummer1Feld)
            self.kiLoesung = None
            self.kiBewegungVorlage = None
            self.kiZaehler = 0

        # - druecken um Feld zu verringern, auf das die 1-Feld-KI abzielt
        if e.key() == Qt.Key_Minus:
            self.kiFeldnummer1Feld = (self.kiFeldnummer1Feld - 1) % 4
            print("KI-Zeiger nun auf :  ", self.kiFeldnummer1Feld)
            self.kiLoesung = None
            self.kiBewegungVorlage = None
            self.kiZaehler = 0


        # P druecken um zufaelliges Level zu erstellen/ueberpruefen
        if e.key() == Qt.Key_P:
            fertig = True
            for m in range(4):
                if not self.kiSchritt(m):
                    slb.erstelltesLevel[m] = slb.zufaelligesLevelErstellen(slb.Z_REIHEN, slb.Z_SPALTEN,
                                                                           slb.Z_WK_SCHWARZE_FELDER)
                    self.levelReset()
                    fertig = False
            if fertig:
                print("Zufaelliges Level ist fertig")
            self.update()

        if e.key() == Qt.Key_O:
            fertig = False
            felderFertig = [False, False, False, False]
            while not fertig:
                fertig = True
                for m in range(4):
                    if not felderFertig[m]:
                        if not self.kiSchritt(m):
                            slb.erstelltesLevel[m] = slb.zufaelligesLevelErstellen(slb.Z_REIHEN, slb.Z_SPALTEN,
                                                                                   slb.Z_WK_SCHWARZE_FELDER)
                            self.levelReset()
                            fertig = False
                        else:
                            felderFertig[m] = True

            print("Zufaelliges Level ist fertig")
            self.update()

    """ Grundfunktionen """

    def koordinatenBestimmen(self):

        # Idee: Fuer jeden Eintrag jeweils linke obere und rechte untere Koordinate f??r ein Rechteck bestimmen.
        #       Diese als Tupel von zwei Tupeln (2 Punkte, also 4 Koordinaten) in geschachtelter Liste so platzieren,
        #       dass sie die gleichen Indizes haben, wie die zugehoerigen Werte
        result = []

        # reine Vorberechnung
        breite = (self.wW - 2 * self.verschiebungNachRechts) // self.anzahlSpalten
        hoehe = (self.wH - 2 * self.verschiebungNachUnten) // self.anzahlZeilen

        for i in range(self.anzahlZeilen):
            zeile = []
            for j in range(self.anzahlSpalten):

                punktLinksOben = (self.verschiebungNachRechts + breite * j, self.verschiebungNachUnten + hoehe * i)
                punktRechtsUnten = (self.verschiebungNachRechts + breite * (j + 1), self.verschiebungNachUnten + hoehe * (i + 1))

                zeile.append( ( punktLinksOben , punktRechtsUnten ) )
            result.append(zeile)
        return result


    def positionenBestimmenSpieler(self):
        allePositionenSpieler = []
        for n in range(4):
            fertig = False
            for i in range(self.anzahlZeilen):
                for j in range(self.anzahlSpalten):
                    if self.level[n][i][j] == 2:
                        allePositionenSpieler.append([i, j])
                        fertig = True
                        break
                if fertig:
                    break
        return allePositionenSpieler


    def positionenBestimmenKiste(self):
        allePositionenKiste = []
        for n in range(4):
            fertig = False
            for i in range(self.anzahlZeilen):
                for j in range(self.anzahlSpalten):
                    if self.level[n][i][j] == 3:
                        allePositionenKiste.append([i, j])
                        fertig = True
                        break
                if fertig:
                    break
        return allePositionenKiste


    def positionBestimmenZiel(self):
        allePositionenZiele = []
        for n in range(4):
            fertig = False
            for i in range(self.anzahlZeilen):
                for j in range(self.anzahlSpalten):
                    if self.level[n][i][j] == 4:
                        allePositionenZiele.append([i, j])
                        fertig = True
                        break
                if fertig:
                    break
        return allePositionenZiele


    def levelReset(self):
        self.level = copy.deepcopy(ss.LEVEL)
        self.spielerPosition = self.positionenBestimmenSpieler()
        self.kistePosition = self.positionenBestimmenKiste()
        self.gewonnen = [False, False, False, False]
        self.gemachteZuege = [copy.deepcopy((self.spielerPosition, self.kistePosition))]
        self.kiZaehler = 0
        self.kiLoesung = None
        self.kiBewegungVorlage = None
        # 2 und 3 entfernen aus Level
        for n in range(4):
            self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
            self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0


    def pruefenObGewonnen(self):
        """ Ueberpruefen ob gesamtes Level geschafft ist """
        for n in range(4):
            if not self.gewonnen[n]:
                return False

        print("Glueckwunsch du hast gewonnen!")
        return True


    def aufZufaelligesLevelWechseln(self, m):
        if not self.kiSchritt(m):
            slb.erstelltesLevel[m] = slb.zufaelligesLevelErstellen(slb.Z_REIHEN, slb.Z_SPALTEN, slb.Z_WK_SCHWARZE_FELDER)
            self.levelReset()



    """ Bewegung """

    def schrittZurueck(self):
        if len(self.gemachteZuege) == 1:
            return False

        # letztes Element der Liste der gemachten Zuege loeschen
        self.gemachteZuege.pop()

        # alte Positionen im Level leeren
        for n in range(4):
            self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
            if self.gewonnen[n]:
                self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 4
                self.gewonnen[n] = False
            else:
                self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0

        # Positionen aendern
        self.spielerPosition = copy.deepcopy(self.gemachteZuege[-1][0])
        self.kistePosition = copy.deepcopy(self.gemachteZuege[-1][1])

        # Gewinn zurueckziehen, wenn Block nicht mehr im Zielfeld
        for n in range(4):
            if self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] == 4:
                self.gewonnen[n] = True

        return True


    def nachObenBewegen(self, m = 0):

        if not self.gewonnen[m]:
            if self.level[m][self.spielerPosition[m][0] - 1][self.spielerPosition[m][1]] == 0 and \
                    [self.spielerPosition[m][0] - 1, self.spielerPosition[m][1]] != self.kistePosition[m]:
                # Positionen aendern
                self.spielerPosition[m][0] -= 1

            elif [ self.spielerPosition[m][0] - 1, self.spielerPosition[m][1] ] == self.kistePosition[m] and \
                    self.level[m][self.kistePosition[m][0] - 1][self.kistePosition[m][1]] in [0,4]:

                # pruefen ob Abschnitt fertig
                if self.level[m][self.kistePosition[m][0] - 1][self.kistePosition[m][1]] == 4:
                    self.gewonnen[m] = True

                # Positionen aendern
                self.kistePosition[m][0] -= 1
                self.spielerPosition[m][0] -= 1

        # Zug abspeichern
        # self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))


    def nachUntenBewegen(self, m = 0):
        if not self.gewonnen[m]:
            if self.level[m][self.spielerPosition[m][0] + 1][self.spielerPosition[m][1]] == 0 and \
                    [self.spielerPosition[m][0] + 1, self.spielerPosition[m][1]] != self.kistePosition[m]:
                # Positionen aendern
                self.spielerPosition[m][0] += 1

            elif [ self.spielerPosition[m][0] + 1, self.spielerPosition[m][1] ] == self.kistePosition[m] and \
                    self.level[m][self.kistePosition[m][0] + 1][self.kistePosition[m][1]] in [0, 4]:

                # pruefen ob Abschnitt fertig
                if self.level[m][self.kistePosition[m][0] + 1][self.kistePosition[m][1]] == 4:
                    self.gewonnen[m] = True

                # Positionen aendern
                self.kistePosition[m][0] += 1
                self.spielerPosition[m][0] += 1

        # Zug abspeichern
        # self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))


    def nachRechtsBewegen(self, m = 0):
        if not self.gewonnen[m]:
            if self.level[m][self.spielerPosition[m][0]][self.spielerPosition[m][1] + 1] == 0 and \
                    [self.spielerPosition[m][0], self.spielerPosition[m][1] + 1] != self.kistePosition[m]:
                # Positionen aendern
                self.spielerPosition[m][1] += 1

            elif [self.spielerPosition[m][0], self.spielerPosition[m][1] + 1] == self.kistePosition[m] and \
                    self.level[m][self.kistePosition[m][0]][self.kistePosition[m][1] + 1] in [0, 4]:

                # pruefen ob Abschnitt fertig
                if self.level[m][self.kistePosition[m][0]][self.kistePosition[m][1] + 1] == 4:
                    self.gewonnen[m] = True

                # Positionen aendern
                self.kistePosition[m][1] += 1
                self.spielerPosition[m][1] += 1

        # Zug abspeichern
        # self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
        

    def nachLinksBewegen(self, m = 0):
        if not self.gewonnen[m]:
            if self.level[m][self.spielerPosition[m][0]][self.spielerPosition[m][1] - 1] == 0 and \
                    [self.spielerPosition[m][0], self.spielerPosition[m][1] - 1] != self.kistePosition[m]:
                # Positionen aendern
                self.spielerPosition[m][1] -= 1

            elif [self.spielerPosition[m][0], self.spielerPosition[m][1] - 1] == self.kistePosition[m] and \
                    self.level[m][self.kistePosition[m][0]][self.kistePosition[m][1] - 1] in [0, 4]:

                # pruefen ob Abschnitt fertig
                if self.level[m][self.kistePosition[m][0]][self.kistePosition[m][1] - 1] == 4:
                    self.gewonnen[m] = True

                # Positionen aendern
                self.kistePosition[m][1] -= 1
                self.spielerPosition[m][1] -= 1

        # Zug abspeichern
        # self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))


    """ KI """

    def oberesFeld(self, positionSpielerUndKisteO, m = 0):
        positionSpielerO = copy.deepcopy(positionSpielerUndKisteO[0])
        positionKisteO = copy.deepcopy(positionSpielerUndKisteO[1])

        # pruefen ob schon fertig
        if positionKisteO == self.zielPosition[m]:
            return positionSpielerO, positionKisteO

        if self.level[m][positionSpielerO[0] - 1][positionSpielerO[1]] == 0 and \
                [positionSpielerO[0] - 1, positionSpielerO[1]] != positionKisteO:
            # Positionen aendern
            positionSpielerO[0] -= 1

        elif [ positionSpielerO[0] - 1, positionSpielerO[1] ] == positionKisteO and \
                self.level[m][positionKisteO[0] - 1][positionKisteO[1]] in [0,4]:

            # pruefen ob Abschnitt fertig
            if self.level[m][positionKisteO[0] - 1][positionKisteO[1]] == 4:
                self.gewonnen[m] = True

            # Positionen aendern
            positionKisteO[0] -= 1
            positionSpielerO[0] -= 1

        return positionSpielerO, positionKisteO


    def rechtesFeld(self, positionSpielerUndKisteR, m = 0):
        positionSpielerR = copy.deepcopy(positionSpielerUndKisteR[0])
        positionKisteR = copy.deepcopy(positionSpielerUndKisteR[1])

        # pruefen ob schon fertig
        if positionKisteR == self.zielPosition[m]:
            return positionSpielerR, positionKisteR

        if self.level[m][positionSpielerR[0]][positionSpielerR[1] + 1] == 0 and \
                [positionSpielerR[0], positionSpielerR[1] + 1] != positionKisteR:
            # Positionen aendern
            positionSpielerR[1] += 1

        elif [positionSpielerR[0], positionSpielerR[1] + 1] == positionKisteR and \
                self.level[m][positionKisteR[0]][positionKisteR[1] + 1] in [0, 4]:

            # pruefen ob Abschnitt fertig
            if self.level[m][positionKisteR[0]][positionKisteR[1] + 1] == 4:
                self.gewonnen[m] = True

            # Positionen aendern
            positionKisteR[1] += 1
            positionSpielerR[1] += 1

        return positionSpielerR, positionKisteR


    def unteresFeld(self, positionSpielerUndKisteU, m = 0):
        positionSpielerU = copy.deepcopy(positionSpielerUndKisteU[0])
        positionKisteU = copy.deepcopy(positionSpielerUndKisteU[1])

        # pruefen ob schon fertig
        if positionKisteU == self.zielPosition[m]:
            return positionSpielerU, positionKisteU

        if self.level[m][positionSpielerU[0] + 1][positionSpielerU[1]] == 0 and \
                [positionSpielerU[0] + 1, positionSpielerU[1]] != positionKisteU:
            # Positionen aendern
            positionSpielerU[0] += 1

        elif [positionSpielerU[0] + 1, positionSpielerU[1]] == positionKisteU and \
                self.level[m][positionKisteU[0] + 1][positionKisteU[1]] in [0, 4]:

            # pruefen ob Abschnitt fertig
            if self.level[m][positionKisteU[0] + 1][positionKisteU[1]] == 4:
                self.gewonnen[m] = True

            # Positionen aendern
            positionKisteU[0] += 1
            positionSpielerU[0] += 1

        return positionSpielerU, positionKisteU


    def linkesFeld(self, positionSpielerUndKisteL, m = 0):
        positionSpielerL = copy.deepcopy(positionSpielerUndKisteL[0])
        positionKisteL = copy.deepcopy(positionSpielerUndKisteL[1])

        # pruefen ob schon fertig
        if positionKisteL == self.zielPosition[m]:
            return positionSpielerL, positionKisteL

        if self.level[m][positionSpielerL[0]][positionSpielerL[1] - 1] == 0 and \
                [positionSpielerL[0], positionSpielerL[1] - 1] != positionKisteL:
            # Positionen aendern
            positionSpielerL[1] -= 1

        elif [positionSpielerL[0], positionSpielerL[1] - 1] == positionKisteL and \
                self.level[m][positionKisteL[0]][positionKisteL[1] - 1] in [0, 4]:

            # pruefen ob Abschnitt fertig
            if self.level[m][positionKisteL[0]][positionKisteL[1] - 1] == 4:
                self.gewonnen[m] = True

            # Positionen aendern
            positionKisteL[1] -= 1
            positionSpielerL[1] -= 1

        return positionSpielerL, positionKisteL


    def kiSchritt(self, m = 0):

        moeglicheWege = [ [ (self.spielerPosition[m], self.kistePosition[m]) ] ]
        hilfsliste =[(self.spielerPosition[m], self.kistePosition[m])]  # der hilfsliste ein tupel aus spieler und kistenposition hinzufuegen

        abbruchzaehler = 0
        while True:
            abbruchzaehler += 1
            if abbruchzaehler > 200:
                print("Nicht loesbar")
                return False

            moeglicheWegeKopie = copy.deepcopy(moeglicheWege)
            moeglicheWege = []

            for welcherWeg in range(len(moeglicheWegeKopie)):
                momentanePosition = moeglicheWegeKopie[welcherWeg][-1]

                """ nach oben """
                naechstePositionO = self.oberesFeld(momentanePosition, m)
                if naechstePositionO not in hilfsliste:
                    wegO = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegO.append(naechstePositionO)
                    moeglicheWege.append(wegO)
                    hilfsliste.append(naechstePositionO)

                    if self.gewonnen[m]:
                        print("geschafft")
                        #print("Schnellster Weg :  ", wegO)
                        self.gewonnen[m] = False
                        return wegO

                """ nach rechts """
                naechstePositionR = self.rechtesFeld(momentanePosition, m)
                if naechstePositionR not in hilfsliste:
                    wegR = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegR.append(naechstePositionR)
                    moeglicheWege.append(wegR)
                    hilfsliste.append(naechstePositionR)

                    if self.gewonnen[m]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegR)
                        self.gewonnen[m] = False
                        return wegR

                """ nach unten """
                naechstePositionU = self.unteresFeld(momentanePosition, m)
                if naechstePositionU not in hilfsliste:
                    wegU = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegU.append(naechstePositionU)
                    moeglicheWege.append(wegU)
                    hilfsliste.append(naechstePositionU)

                    if self.gewonnen[m]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegU)
                        self.gewonnen[m] = False
                        return wegU

                """ nach links """
                naechstePositionL = self.linkesFeld(momentanePosition, m)
                if naechstePositionL not in hilfsliste:
                    wegL = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegL.append(naechstePositionL)
                    moeglicheWege.append(wegL)
                    hilfsliste.append(naechstePositionL)

                    if self.gewonnen[m]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegL)
                        self.gewonnen[m] = False
                        return wegL


    def kiBewegungVorlageErstellen(self, wegPlan):
        bewegung = []
        for spielerUndKisteIndex in range(len(wegPlan) - 1):
            if wegPlan[spielerUndKisteIndex][0][0] > wegPlan[spielerUndKisteIndex + 1][0][0]:
                bewegung.append("oben")
            if wegPlan[spielerUndKisteIndex][0][0] < wegPlan[spielerUndKisteIndex + 1][0][0]:
                bewegung.append("unten")
            if wegPlan[spielerUndKisteIndex][0][1] > wegPlan[spielerUndKisteIndex + 1][0][1]:
                bewegung.append("links")
            if wegPlan[spielerUndKisteIndex][0][1] < wegPlan[spielerUndKisteIndex + 1][0][1]:
                bewegung.append("rechts")

        return bewegung


    def kiBewegungVorlageErstellen2Felder(self, wegPlan):
        bewegung = []
        for spielerUndKisteIndex in range(len(wegPlan) - 1):
            if wegPlan[spielerUndKisteIndex][0][0][0] > wegPlan[spielerUndKisteIndex + 1][0][0][0]:
                bewegung.append("oben")
            elif wegPlan[spielerUndKisteIndex][0][0][0] < wegPlan[spielerUndKisteIndex + 1][0][0][0]:
                bewegung.append("unten")
            elif wegPlan[spielerUndKisteIndex][0][0][1] > wegPlan[spielerUndKisteIndex + 1][0][0][1]:
                bewegung.append("links")
            elif wegPlan[spielerUndKisteIndex][0][0][1] < wegPlan[spielerUndKisteIndex + 1][0][0][1]:
                bewegung.append("rechts")
            else:
                if wegPlan[spielerUndKisteIndex][1][0][0] > wegPlan[spielerUndKisteIndex + 1][1][0][0]:
                    bewegung.append("oben")
                elif wegPlan[spielerUndKisteIndex][1][0][0] < wegPlan[spielerUndKisteIndex + 1][1][0][0]:
                    bewegung.append("unten")
                elif wegPlan[spielerUndKisteIndex][1][0][1] > wegPlan[spielerUndKisteIndex + 1][1][0][1]:
                    bewegung.append("links")
                elif wegPlan[spielerUndKisteIndex][1][0][1] < wegPlan[spielerUndKisteIndex + 1][1][0][1]:
                    bewegung.append("rechts")

        return bewegung


    def kiSchritt2Felder(self, m = 0, n = 1):

        moeglicheWege = [ [ ( (self.spielerPosition[m], self.kistePosition[m]) , (self.spielerPosition[n], self.kistePosition[n]) ) ] ]
        hilfsliste =[ ( (self.spielerPosition[m], self.kistePosition[m]) , (self.spielerPosition[n], self.kistePosition[n]) ) ]

        abbruchzaehler = 0
        while True:
            abbruchzaehler += 1
            if abbruchzaehler > 10000:
                print("Abgebrochen")
                return

            moeglicheWegeKopie = copy.deepcopy(moeglicheWege)
            moeglicheWege = []

            for welcherWeg in range(len(moeglicheWegeKopie)):
                momentanePosition = moeglicheWegeKopie[welcherWeg][-1]

                """ nach oben """
                naechstePositionO1 = self.oberesFeld(momentanePosition[0], m)
                naechstePositionO2 = self.oberesFeld(momentanePosition[1], n)
                if (naechstePositionO1, naechstePositionO2) not in hilfsliste:
                    wegO = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegO.append((naechstePositionO1, naechstePositionO2))
                    moeglicheWege.append(wegO)
                    hilfsliste.append((naechstePositionO1, naechstePositionO2))

                    #if self.gewonnen[m] and self.gewonnen[n]:
                    if naechstePositionO1[1] == self.zielPosition[m] and naechstePositionO2[1] == self.zielPosition[n]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegO)
                        self.gewonnen[m] = False
                        self.gewonnen[n] = False
                        return wegO


                """ nach rechts """
                naechstePositionR1 = self.rechtesFeld(momentanePosition[0], m)
                naechstePositionR2 = self.rechtesFeld(momentanePosition[1], n)
                if (naechstePositionR1, naechstePositionR2) not in hilfsliste:
                    wegR = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegR.append((naechstePositionR1, naechstePositionR2))
                    moeglicheWege.append(wegR)
                    hilfsliste.append((naechstePositionR1, naechstePositionR2))

                    #if self.gewonnen[m]:
                    if naechstePositionR1[1] == self.zielPosition[m] and naechstePositionR2[1] == self.zielPosition[n]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegR)
                        self.gewonnen[m] = False
                        self.gewonnen[n] = False
                        return wegR


                """ nach unten """
                naechstePositionU1 = self.unteresFeld(momentanePosition[0], m)
                naechstePositionU2 = self.unteresFeld(momentanePosition[1], n)
                if (naechstePositionU1, naechstePositionU2) not in hilfsliste:
                    wegU = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegU.append((naechstePositionU1, naechstePositionU2))
                    moeglicheWege.append(wegU)
                    hilfsliste.append((naechstePositionU1, naechstePositionU2))

                    #if self.gewonnen[m]:
                    if naechstePositionU1[1] == self.zielPosition[m] and naechstePositionU2[1] == self.zielPosition[n]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegU)
                        self.gewonnen[m] = False
                        self.gewonnen[n] = False
                        return wegU


                """ nach links """
                naechstePositionL1 = self.linkesFeld(momentanePosition[0], m)
                naechstePositionL2 = self.linkesFeld(momentanePosition[1], n)
                if (naechstePositionL1, naechstePositionL2) not in hilfsliste:
                    wegL = copy.deepcopy(moeglicheWegeKopie[welcherWeg])
                    wegL.append((naechstePositionL1, naechstePositionL2))
                    moeglicheWege.append(wegL)
                    hilfsliste.append((naechstePositionL1, naechstePositionL2))

                    #if self.gewonnen[m]:
                    if naechstePositionL1[1] == self.zielPosition[m] and naechstePositionL2[1] == self.zielPosition[n]:
                        print("geschafft")
                        print("Schnellster Weg :  ", wegL)
                        self.gewonnen[m] = False
                        self.gewonnen[n] = False
                        return wegL






app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
