import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen, QImage, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QEvent, QRect, QPointF, QPropertyAnimation, QTimer
import copy
import sokobanSettings as ss


""" 
Erklaerung: 
    - 0 entspricht leerem Feld
    - 1 entspricht Wand
    - 2 entspricht Spieler
    - 3 entspricht Kiste
"""

class Knoten:

    def __init__(self):
        self.positionen = (None, None)
        self.oben = None
        self.rechts = None
        self.unten = None
        self.links = None



class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.echtewW = ss.FENSTERBREITE
        self.echtewH = ss.FENSTERHOEHE
        self.wW = ss.FENSTERBREITE // 2       # wW = windowWidth
        self.wH = ss.FENSTERHOEHE // 2        # wH = windowHeight
        self.setGeometry(500, 30, self.echtewW, self.echtewH)
        self.setWindowTitle("Paralleles Sokoban")
        self.nachUnten = self.wH // 8  # Gesamtverschiebung nach unten
        self.nachRechts = self.wW // 8  # Gesamtverschiebung nach rechts

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

        # ein Eintrag besteht aus einer Liste, die self.gemachteZuege entspricht, wuerde man diesen Weg gehen
        self.moeglicheWegeKI = []


        self.keyPressEvent = self.fn
        self.show()


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
            hoehe = (self.wH - 2 * self.nachUnten) // self.anzahlZeilen
            breite = (self.wW - 2 * self.nachRechts) // self.anzahlSpalten


            # vertikale Linien
            for verschiebung in range(self.anzahlSpalten + 1):
                painter.drawLine(self.nachRechts + breite * verschiebung + raeudigeVerschiebungX,
                                 self.nachUnten + raeudigeVerschiebungY,
                                 self.nachRechts + breite * verschiebung + raeudigeVerschiebungX,
                                 self.wH - self.nachUnten - 8 + raeudigeVerschiebungY)

            # horizontale Linien
            for verschiebung in range(self.anzahlZeilen + 1):
                painter.drawLine(self.nachRechts + raeudigeVerschiebungX,
                                self.nachUnten + hoehe * verschiebung + raeudigeVerschiebungY,
                                self.wW - self.nachRechts - 2 + raeudigeVerschiebungX,
                                self.nachUnten + hoehe * verschiebung + raeudigeVerschiebungY)


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
                self.kiNachLinks(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()

        # nach rechts bewegen
        if e.key() == Qt.Key_Right:
            for n in range(4):
                self.kiNachRechts(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()

        # nach oben bewegen
        if e.key() == Qt.Key_Up:
            for n in range(4):
                self.kiNachOben(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()

        # nach unten bewegen
        if e.key() == Qt.Key_Down:
            for n in range(4):
                self.kiNachUnten(n)
            # Zug abspeichern
            self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))
            self.update()




        # I nach oben
        if e.key() == Qt.Key_I:
            self.kiNachOben()
            self.update()

        # K nach unten
        if e.key() == Qt.Key_K:
            self.kiNachUnten()
            self.update()

        # L nach rechts
        if e.key() == Qt.Key_L:
            self.kiNachRechts()
            self.update()

        # J nach links
        if e.key() == Qt.Key_J:
            self.kiNachLinks()
            self.update()



    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        print("               ", pos.x(), pos.y())     # zum ueberpruefen wo man klickt



    def koordinatenBestimmen(self):

        # Idee: Fuer jeden Eintrag jeweils linke obere und rechte untere Koordinate für ein Rechteck bestimmen.
        #       Diese als Tupel von zwei Tupeln (2 Punkte, also 4 Koordinaten) in geschachtelter Liste so platzieren,
        #       dass sie die gleichen Indizes haben, wie die zugehoerigen Werte
        result = []

        # reine Vorberechnung
        breite = (self.wW - 2 * self.nachRechts) // self.anzahlSpalten
        hoehe = (self.wH - 2 * self.nachUnten) // self.anzahlZeilen

        for i in range(self.anzahlZeilen):
            zeile = []
            for j in range(self.anzahlSpalten):

                punktLinksOben = (self.nachRechts + breite * j, self.nachUnten + hoehe * i)
                punktRechtsUnten = (self.nachRechts + breite * (j+1), self.nachUnten + hoehe * (i+1))

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


    def pruefenObGewonnen(self):
        """ Ueberpruefen ob gesamtes Level geschafft ist """
        for n in range(4):
            if not self.gewonnen[n]:
                return False

        print("Glueckwunsch du hast gewonnen!")
        return True


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


    def nachLinksBewegen(self):
        for n in range(4):
            if not self.gewonnen[n]:
                if self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] - 1] == 0:
                    # Positionen aendern
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] - 1] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][1] -= 1

                elif self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] - 1] == 3 and \
                        self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1] - 1] in [0, 4]:

                    # pruefen ob Abschnitt fertig
                    if self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1] - 1] == 4:
                        self.gewonnen[n] = True
                        self.pruefenObGewonnen()

                    # Positionen aendern
                    self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1] - 1] = 3
                    self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0
                    self.kistePosition[n][1] -= 1
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] - 1] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][1] -= 1

        # Zug abspeichern
        self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))


    def nachRechtsBewegen(self):
        for n in range(4):
            if not self.gewonnen[n]:
                if self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] + 1] == 0:
                    # Positionen aendern
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] + 1] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][1] += 1

                elif self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] + 1] == 3 and \
                        self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1] + 1] in [0, 4]:

                    # pruefen ob Abschnitt fertig
                    if self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1] + 1] == 4:
                        self.gewonnen[n] = True
                        self.pruefenObGewonnen()

                    # Positionen aendern
                    self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1] + 1] = 3
                    self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0
                    self.kistePosition[n][1] += 1
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1] + 1] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][1] += 1

        # Zug abspeichern
        self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))


    def nachObenBewegen(self):
        for n in range(4):
            if not self.gewonnen[n]:
                if self.level[n][self.spielerPosition[n][0] - 1][self.spielerPosition[n][1]] == 0:
                    # Positionen aendern
                    self.level[n][self.spielerPosition[n][0] - 1][self.spielerPosition[n][1]] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][0] -= 1


                elif self.level[n][self.spielerPosition[n][0] - 1][self.spielerPosition[n][1]] == 3 and \
                        self.level[n][self.kistePosition[n][0] - 1][self.kistePosition[n][1]] in [0, 4]:

                    # pruefen ob Abschnitt fertig
                    if self.level[n][self.kistePosition[n][0] - 1][self.kistePosition[n][1]] == 4:
                        self.gewonnen[n] = True
                        self.pruefenObGewonnen()

                    # Positionen aendern
                    self.level[n][self.kistePosition[n][0] - 1][self.kistePosition[n][1]] = 3
                    self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0
                    self.kistePosition[n][0] -= 1
                    self.level[n][self.spielerPosition[n][0] - 1][self.spielerPosition[n][1]] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][0] -= 1

        # Zug abspeichern
        self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))


    def nachUntenBewegen(self):
        for n in range(4):
            if not self.gewonnen[n]:
                if self.level[n][self.spielerPosition[n][0] + 1][self.spielerPosition[n][1]] == 0:
                    # Positionen aendern
                    self.level[n][self.spielerPosition[n][0] + 1][self.spielerPosition[n][1]] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][0] += 1

                elif self.level[n][self.spielerPosition[n][0] + 1][self.spielerPosition[n][1]] == 3 and \
                        self.level[n][self.kistePosition[n][0] + 1][self.kistePosition[n][1]] in [0, 4]:

                    # pruefen ob Abschnitt fertig
                    if self.level[n][self.kistePosition[n][0] + 1][self.kistePosition[n][1]] == 4:
                        self.gewonnen[n] = True
                        self.pruefenObGewonnen()

                    # Positionen aendern
                    self.level[n][self.kistePosition[n][0] + 1][self.kistePosition[n][1]] = 3
                    self.level[n][self.kistePosition[n][0]][self.kistePosition[n][1]] = 0
                    self.kistePosition[n][0] += 1
                    self.level[n][self.spielerPosition[n][0] + 1][self.spielerPosition[n][1]] = 2
                    self.level[n][self.spielerPosition[n][0]][self.spielerPosition[n][1]] = 0
                    self.spielerPosition[n][0] += 1

        # Zug abspeichern
        self.gemachteZuege.append(copy.deepcopy((self.spielerPosition, self.kistePosition)))




    def kiNachOben(self, m = 0):

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


    def kiNachUnten(self, m = 0):
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


    def kiNachRechts(self, m = 0):
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
        


    def kiNachLinks(self, m = 0):
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


    def kiSchritt(self):
        # in jede Richtung ueberpruefen ob Bewegung dorthin schlecht waere
        self.kiNachOben()









app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
