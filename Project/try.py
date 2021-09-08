"""
Faceti click intre celule pentru a crea un zid.
Incercati sa inconjurati o celula cu toate cele 4 ziduri.
Daca apasati tasta i puteti activa/dezactiva imaginile.
Daca apasati tasta s opriti meciul in curs, iar nin consola sunt afisate statisticile pana in acel moment.
"""
import copy
import statistics
import time
import pygame
import sys

lines = 3
columns = 3
cell_dimension = 110
cell_padding = 5
width = 1000
height = 900
ecr = pygame.display.set_mode(size=(width, height))
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
NODES_NUMBER = 0


class Player:
    """
    Clasa jucator: vor fi instantiati 2 jucatori, fiecaruia corespunzandu-i cate un nume si o culoare + scor.
    """
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0


class Celula:
    # coordonatele nodurilor ()
    grosimeZid = 10  # numar impar
    fundalCelula = (255, 255, 255)
    culoareLinii = (0, 0, 0)
    afisImagini = True

    def __init__(self, left, top, w, h, lin, col, interfata, cod=0):
        """
        Fiecare celula reprezinta un patrat de pe tabla de joc care, pentru a fi cucerit, trebuia sa aiba toate cele 4
        ziduri selectate, Imaginea din interiorul patratului este determinata de jucatorul care selecteaa ultimul zid
         neselectat al celulei.
        """
        self.dreptunghi = pygame.Rect(left, top, w, h)
        self.zid = [None, None, None, None]
        # zidurile vor fi pe pozitiile 0-sus, 1-dreapta, 2-jos, 3-stanga
        self.cod = 0
        self.player = None

        # stanga sus
        self.point1 = pygame.Rect(left - 1 - self.__class__.grosimeZid // 2, top - 1 - self.__class__.grosimeZid // 2,
                                  self.__class__.grosimeZid, self.__class__.grosimeZid)
        # dreapta jos
        self.point2 = pygame.Rect(left + w - self.__class__.grosimeZid // 2, top + h - self.__class__.grosimeZid // 2,
                                  self.__class__.grosimeZid, self.__class__.grosimeZid)
        # stanga jos
        self.point3 = pygame.Rect(left - 1 - self.__class__.grosimeZid // 2, top + h - self.__class__.grosimeZid // 2,
                                  self.__class__.grosimeZid, self.__class__.grosimeZid)
        # dreapta sus
        self.point4 = pygame.Rect(left + w - self.__class__.grosimeZid // 2, top - 1 - self.__class__.grosimeZid // 2,
                                  self.__class__.grosimeZid, self.__class__.grosimeZid)

        # sus
        self.zid[0] = pygame.Rect(left + self.__class__.grosimeZid // 2 - 1, top - 1 - self.__class__.grosimeZid // 2,
                                  w - self.__class__.grosimeZid + 1, self.__class__.grosimeZid)
        # dreapta
        self.zid[1] = pygame.Rect(left + w - self.__class__.grosimeZid // 2, top + self.__class__.grosimeZid // 2 - 1,
                                  self.__class__.grosimeZid, h - self.__class__.grosimeZid + 1)
        # jos
        self.zid[2] = pygame.Rect(left + self.__class__.grosimeZid // 2 - 1, top + h - self.__class__.grosimeZid // 2,
                                  w - self.__class__.grosimeZid + 1, self.__class__.grosimeZid)
        # stanga
        self.zid[3] = pygame.Rect(left - 1 - self.__class__.grosimeZid // 2, top + self.__class__.grosimeZid // 2 - 1,
                                  self.__class__.grosimeZid, h - self.__class__.grosimeZid + 1)

    # print(self.zid)
    # 0001 zid doar sus
    # 0011 zid sus si dreapta etc

    def deseneaza(self):
        """
        Este desenata celula
        :return:
        """

        pygame.draw.rect(ecr, self.__class__.fundalCelula, self.dreptunghi)
        # masti=[1,2,4,8]
        masca = 1
        for i in range(4):
            if self.cod & masca:
                if self.zid[i]:
                    pygame.draw.rect(ecr, self.__class__.culoareLinii, self.zid[i])
            masca *= 2

        # pygame.draw.rect(self.display, self.__class__.culoareLinii, self.point2)
        pygame.draw.rect(ecr, self.__class__.culoareLinii, self.point1)
        pygame.draw.rect(ecr, self.__class__.culoareLinii, self.point2)
        pygame.draw.rect(ecr, self.__class__.culoareLinii, self.point3)
        pygame.draw.rect(ecr, self.__class__.culoareLinii, self.point4)


class Interfata:
    culoareEcran = (255, 255, 255)
    dimCelula = cell_dimension
    paddingCelula = cell_padding
    dimImagine = dimCelula - 2 * paddingCelula
    ecran = ecr

    JMIN = None
    JMAX = None

    def initializeaza(self):
        """
        Sunt initializate imaginile celor 2 jucatori
        :return:
        """

        # self.ecran = ecran
        # top_index = (height - nrLinii * (self.__class__.dimCelula + 1)) / ((self.__class__.dimCelula + 1) * 2)
        # left_index = (width - nrColoane * (self.__class__.dimCelula + 1)) / ((self.__class__.dimCelula + 1) * 2)
        # top_index = int(top_index) + 1
        # left_index = int(left_index) + 1
        # self.matrCelule = [[Celula(display=ecran, left=col * (self.__class__.dimCelula + 1),
        #                            top=lin * (self.__class__.dimCelula + 1), w=self.__class__.dimCelula,
        #                            h=self.__class__.dimCelula, lin=lin, col=col, interfata=self) for col in
        #                     range(left_index, nrColoane + left_index)] for lin in range(top_index, nrLinii + top_index)]

        blue_face = pygame.image.load('blue_face.png')
        self.blue_face = pygame.transform.scale(blue_face, (self.__class__.dimImagine, self.__class__.dimImagine))

        red_face = pygame.image.load('red_face.png')
        self.red_face = pygame.transform.scale(red_face, (self.__class__.dimImagine, self.__class__.dimImagine))

    def __init__(self, nrLinii=lines, nrColoane=columns, matrix=None):
        """
        Interfata reprezinta jocul atat dpdv grafic, cat si dpdv al mutarilor si al calculelor.
        :param nrLinii:
        :param nrColoane:
        :param matrix:
        """
        self.nrLinii = nrLinii
        self.nrColoane = nrColoane
        if matrix is not None:
            self.matrCelule = matrix
        else:
            top_index = (height - self.nrLinii * (self.__class__.dimCelula - 1)) / ((self.__class__.dimCelula + 1) * 2)
            left_index = (width - self.nrColoane * (self.__class__.dimCelula + 1)) / (
                    (self.__class__.dimCelula + 1) * 2)
            top_index = int(top_index) + 1
            left_index = int(left_index)
            self.matrCelule = [[Celula(left=col * (self.__class__.dimCelula + 1),
                                       top=lin * (self.__class__.dimCelula + 1), w=self.__class__.dimCelula,
                                       h=self.__class__.dimCelula, lin=lin, col=col, interfata=self) for col in
                                range(left_index, self.nrColoane + left_index)] for lin in
                               range(top_index, self.nrLinii + top_index)]

    @classmethod
    def jucator_opus(cls, jucator):
        """
        Este returnata o referinta catre jucatorul opus.
        :param jucator:
        :return:
        """
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def calcul_scor(self):
        """
        Pentru fiecare celula cucerita de un jucator, acestuia i se adauga un punct.
        :return:
        """
        jmin_score = 0
        jmax_score = 0

        for linie in self.matrCelule:
            for cel in linie:
                if cel.player is not None:
                    if cel.player.name == self.__class__.JMIN.name:
                        jmin_score += 1
                    elif cel.player.name == self.__class__.JMAX.name:
                        jmax_score += 1

        return jmin_score, jmax_score

    def test_final(self):
        """
        Test pentru a vedea daca jocul a ajuns la final.
        Daca un jucator a cucerit mai mult de jumatate din celule, acesta a castigat si jocul se opreste.
        :return:
        """
        limit = self.nrLinii * self.nrColoane
        if self.JMIN.score > limit // 2 or self.JMAX.score > limit // 2:
            return True
        return False

    @classmethod
    def result(self):
        """
        Este returnat rezultatul final al jocului.
        :return:
        """
        if self.JMIN.score == self.JMAX.score:
            return "Draw"
        elif self.JMIN.score > self.JMAX.score:
            return "You"
        else:
            return "AI"

    def final(self):
        """
        Functie utilizata in estimarea scorului.
        Diferita de fucntia care returneaza scorul curent al jocului.
        :return:
        """
        jmin_score, jmax_score = self.calcul_scor()
        if jmin_score + jmax_score == self.nrLinii * self.nrColoane:
            return True, jmin_score, jmax_score
        return False, jmin_score, jmax_score
        # jmin_score, jmax_score
        # elif jmax_score == jmin_score:
        #     return "Remiza", jmin_score, jmax_score
        # elif jmin_score > jmax_score:
        #     return self.__class__.JMIN, jmin_score, jmax_score
        # else:
        #     return self.__class__.JMAX, jmin_score, jmax_score

    def estimeaza_scor(self, adancime=5):
        """
        Estimeaza scorul dupa un anumit numar de mutari
        :param adancime:
        :return:
        """
        t_final, jmin_score, jmax_score = self.final()
        # if (adancime==0):
        if t_final:
            if jmin_score == jmax_score:
                return 0
            elif jmin_score > jmax_score:
                return -99 - adancime
            else:
                return 99 + adancime
        return jmax_score - jmin_score

    def estimare_scor_2(self):
        return

    # zidurile vor fi pe pozitiile 0-sus, 1-dreapta, 2-jos, 3-stanga
    def mutari(self, player):
        """
        Genereaza toate mutarile posibile dintr-o anumita stare.
        :param player: jucatorul care va muta
        :return: lista cu toate mutarile posibile facute de player
        """
        l_mutari = []
        masks = [1, 2, 0]
        for il, linie in enumerate(self.matrCelule):
            for ic, cel in enumerate(linie):
                if cel.player is None:
                    won_points = False
                    if ic == 0:
                        masks.append(3)
                    for i in masks:
                        masca = 2 ** i
                        if not (cel.cod & masca):
                            matr_tabla_noua = copy.deepcopy(self.matrCelule)
                            matr_tabla_noua[il][ic].cod |= 2 ** i

                            if masca == 1 and il > 0:
                                matr_tabla_noua[il - 1][ic].cod |= 4
                                if matr_tabla_noua[il - 1][ic].cod == 15:
                                    won_points = True
                                    matr_tabla_noua[il - 1][ic].player = player
                            elif masca == 2 and ic < len(matr_tabla_noua[0]) - 1:
                                matr_tabla_noua[il][ic + 1].cod |= 8
                                if matr_tabla_noua[il][ic + 1].cod == 15:
                                    won_points = True
                                    matr_tabla_noua[il][ic + 1].player = player
                            elif masca == 4 and il < len(matr_tabla_noua) - 1:
                                matr_tabla_noua[il + 1][ic].cod |= 1
                                if matr_tabla_noua[il + 1][ic].cod == 15:
                                    won_points = True
                                    matr_tabla_noua[il + 1][ic].player = player
                            elif masca == 8 and ic > 0:
                                matr_tabla_noua[il][ic - 1].cod |= 2
                                if matr_tabla_noua[il][ic - 1].cod == 15:
                                    won_points = True
                                    matr_tabla_noua[il][ic - 1].player = player

                            if matr_tabla_noua[il][ic].cod == 15:
                                won_points = True
                                matr_tabla_noua[il][ic].player = player

                            # for il, linie in enumerate(matr_tabla_noua):
                            #     for ic, cel in enumerate(linie):
                            #         print(cel.cod, end=" ")
                            #     print()
                            # print()
                            l_mutari.append((Interfata(matrix=matr_tabla_noua), won_points))

                    if ic == 0:
                        masks.pop()
            if il == 0:
                masks.pop()

        # l_mutari.sort(reverse=True, key=self.estimeaza_scor)
        # print(len(l_mutari))
        return l_mutari

    def deseneazaImag(self, imag, cel):
        self.ecran.blit(imag, (
            cel.dreptunghi.left + self.__class__.paddingCelula, cel.dreptunghi.top + self.__class__.paddingCelula))

    def deseneazaEcranJoc(self):

        self.ecran.fill(self.__class__.culoareEcran)
        white = (255, 255, 255)
        black = (0, 0, 0)

        font = pygame.font.Font('freesansbold.ttf', 80)
        text = font.render('Dots and Boxes', True, black, white)
        textRect = text.get_rect()
        textRect.center = (width // 2, 50)
        self.ecran.blit(text, textRect)

        for linie in self.matrCelule:
            for cel in linie:
                cel.deseneaza()
                # if Celula.afisImagini:
                #     imag = self.vesel if cel.cod != 15 else self.furios
                #     self.deseneazaImag(imag, cel)
        show_score()
        pygame.display.update()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        # print("admoanasnioabvpsdvaps")
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        l_stari_mutari = []
        # print(won_points)
        for move in l_mutari:
            if move[1]:
                next_player = self.j_curent
            else:
                next_player = Interfata.jucator_opus(self.j_curent)
            l_stari_mutari.append(Stare(move[0], next_player, self.adancime - 1, parinte=self))

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=50, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


# ecran initial
def deseneaza_alegeri(display, tabla_curenta):
    """
    Alegerile din pregame page.
    :param display:
    :param tabla_curenta:
    :return:
    """
    btn_alg = GrupButoane(
        top=height // 2 - height // 5,
        left=width // 2 - 200,
        listaButoane=[
            Buton(display=display, w=200, h=100, text="minimax", valoare="minimax"),
            Buton(display=display, w=200, h=100, text="alpha-beta", valoare="alpha-beta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=height // 2 - height // 5 + 120,
        left=width // 2 - 200,
        listaButoane=[
            Buton(display=display, w=200, h=100, text="First", valoare="x"),
            Buton(display=display, w=200, h=100, text="Second", valoare="0")
        ],
        indiceSelectat=0)
    btn_level = GrupButoane(
        top=height // 2 - height // 5 + 240,
        left=width // 2 - 300,
        listaButoane=[
            Buton(display=display, w=200, h=100, text="Easy", valoare="0"),
            Buton(display=display, w=200, h=100, text="Medium", valoare="1"),
            Buton(display=display, w=200, h=100, text="Hard", valoare="2")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=height // 2 + height // 4, left=width // 2 - 150 // 2, w=150, h=100, text="Play",
               culoareFundal=(155, 0, 55))
    pregame_page()
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_level.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_level.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0, 0, 0))  # stergere ecran
                                tabla_curenta.deseneazaEcranJoc()
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_level.getValoare()
            pygame.display.update()


""" Algoritmul MinMax """


def min_max(stare):
    global NODES_NUMBER
    NODES_NUMBER += 1
    if stare.adancime == 0 or stare.tabla_joc.final()[0]:
        # print("pppppppppppppppppppppppppppppppppppppppppp")     # EROARE AICEA BOS
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Interfata.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        # print("aaaa")
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        # print("bbb")
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def alpha_beta(alpha, beta, stare):
    global NODES_NUMBER
    NODES_NUMBER += 1
    if stare.adancime == 0 or stare.tabla_joc.final()[0]:
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Interfata.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Interfata.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    """
    Rezultatul final
    :param stare_curenta:
    :return:
    """
    final = stare_curenta.tabla_joc.final()[0]
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + str(final))
        return True
    return False


def pregame_page():
    """
    Este afisata pagina de inceput/home.
    :return:
    """
    font = pygame.font.Font('Fonts/Aller_Rg.ttf', 70)
    text = font.render("Dots and Boxes", True, black)
    textRect = text.get_rect()
    textRect.center = (width // 2, 150)
    bg = pygame.image.load("wall5.jpg")
    bg = pygame.transform.scale(bg, (1000, 900))
    # INSIDE OF THE GAME LOOP
    ecr.blit(bg, (0, 0))
    ecr.blit(text, textRect)


def final_result(display, interface, quit=False):
    """
    Sutn afisate optiuni dupa terminarea jocului.
    :param display:
    :param interface:
    :param quit:
    :return:
    """
    final_page(quit)
    choice = draw_final_buttons(display, interface)
    if choice == "Restart":
        main()
        return
    else:
        pygame.quit()
        sys.exit()
        return



def draw_final_buttons(display, tabla_curenta):
    """
    Sunt afisate butoanele din final page.
    :param display:
    :param tabla_curenta:
    :return:
    """
    restart = Buton(display=display, top=height // 2 + height // 4 + 50, left=width // 2 - 205, w=200, h=100, text="Restart",
                    valoare="Restart")
    quit = Buton(display=display, top=height // 2 + height // 4 + 50, left=width // 2 + 5, w=200, h=100, text="Quit",
                 valoare="Quit")

    restart.deseneaza()
    quit.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart.selecteazaDupacoord(pos):
                    return "Restart"
                elif quit.selecteazaDupacoord(pos):
                    return "Quit"
            pygame.display.update()


def final_page(quit=False):
    """
    Este afisata pagina finala.
    :param quit: este True daca jucatorul a renuntat, caz in care jocul s etermina brusc.
    :return:
    """
    font = pygame.font.Font('Fonts/Aller_Rg.ttf', 70)
    resulted = Interfata.result()
    if not quit:
        if resulted == "Draw":
            text = font.render("Draw", True, black, white)
        elif resulted == "You":
            text = font.render("You won!", True, blue, white)
        else:
            text = font.render("AI won!", True, red, white)
    else:
        text = font.render("Abandoned", True, black, white)
    textRect = text.get_rect()
    textRect.center = (width // 2, 250)
    # bg = pygame.image.load("wall5.jpg")
    # ecr.fill((189, 189, 189, 200), None, pygame.BLEND_RGBA_MULT)
    # bg = pygame.transform.scale(bg, (1000, 900))
    # INSIDE OF THE GAME LOOP
    # ecr.blit(bg, (0, 0))
    ecr.blit(text, textRect)


def show_turn(stare_curenta):
    """
    Culoarea cuvantului turn este schimbata in fucntie de culoarea jucatorului care are dreptul la mutare in acel moment.
    :param stare_curenta: reprezinta starea curenta a jocului.
    :return:
    """
    if stare_curenta.j_curent.name == Interfata.JMIN.name:
        turn = "Turn"
        color = blue
    else:
        turn = "Turn"
        color = red
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render(turn, True, color, white)

    textRect = text.get_rect()
    textRect.center = (width // 2, 250)
    ecr.blit(text, textRect)
    pygame.display.update()


def show_score():
    """
    Scorul curent este afisat in partea de sus a tablei de joc.
    Culoarea scorului reprezinta si culoarea jucatorului care are acel scor.
    :return:
    """
    font = pygame.font.Font('freesansbold.ttf', 50)
    text1 = font.render(str(Interfata.JMAX.score), True, red, (255, 255, 255))
    text2 = font.render(str(Interfata.JMIN.score), True, blue, (255, 255, 255))
    text = font.render("Score", True, (0, 0, 0))

    textRect = text.get_rect()
    textRect.center = (width // 2, 150)
    ecr.blit(text, textRect)

    textRect1 = text1.get_rect()
    textRect1.center = (width // 4 - 50, 150)
    ecr.blit(text1, textRect1)

    textRect2 = text2.get_rect()
    textRect2.center = (width - width // 4 + 50, 150)
    ecr.blit(text2, textRect2)


def show_stats(vector, text):
    """
    Sunt afisate statisticile jocului
    :param vector: poate fi vectorul de timp sau vectorul de nr de noduri.
    :param text: reprezinta tipul vectorului (noduri/timp)
    :return:
    """

    print("Statistici " + text)
    print("Minim: ", min(vector))
    print("Maxim: ", max(vector))
    print("Media: ", sum(vector) / len(vector))
    print("Mediana: ", statistics.median(vector))


def main():
    global  NODES_NUMBER
    Interfata.JMAX = Player('0', red)
    Interfata.JMIN = Player('x', blue)

    interf = Interfata()

    pygame.init()
    pygame.display.set_caption('Negulescu Stefan - Dots and Boxes - try')

    player, tip_algoritm, level = deseneaza_alegeri(ecr, interf)

    if level == "0":
        H_MAX = 1
    elif level == "1":
        H_MAX = 3
    else:
        H_MAX = 5

    if player == "x":
        stare_curenta = Stare(interf, Interfata.JMIN, H_MAX)
    else:
        stare_curenta = Stare(interf, Interfata.JMAX, H_MAX)
    # stare_curenta = Stare(interf, Interfata.JMIN, H_MAX)
    interf.initializeaza()
    interf.deseneazaEcranJoc()

    recent_wall = None
    thinking_time_user = []
    thinking_time_ai = []
    t_user = int(round(time.time() * 1000))
    beginning_time = int(round(time.time() * 1000))
    nodes_numbers = []

    while True:
        show_turn(stare_curenta)
        if stare_curenta.j_curent == Interfata.JMIN:
            for ev in pygame.event.get():
                # daca utilizatorul face click pe x-ul de inchidere a ferestrei
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_i:
                        Celula.afisImagini = not Celula.afisImagini
                        stare_curenta.tabla_joc.deseneazaEcranJoc()
                    if ev.key == pygame.K_s:
                        try:
                            print("\n===== STATISTICI =====")
                            show_stats(thinking_time_ai, "Timp gandire AI")
                            show_stats(nodes_numbers, "Numar noduri in memorie")
                            pygame.draw.rect(recent_wall[0], recent_wall[1], recent_wall[2])
                            ending_time = int(round(time.time() * 1000))
                            print("Timp rulare: ", ending_time - beginning_time)
                            final_result(ecr, interf, quit=True)
                        finally:
                            final_result(ecr, interf, quit=True)
                        break

                # daca utilizatorul a facut click
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    zidGasit = []
                    on_wall = False
                    for il, linie in enumerate(stare_curenta.tabla_joc.matrCelule):
                        for ic, cel in enumerate(linie):
                            for iz, zid in enumerate(cel.zid):
                                if zid and zid.collidepoint(pos):
                                    zidGasit.append((cel, iz, zid))
                                    on_wall = True
                    if on_wall:
                        new_wall = False
                        celuleAfectate = []
                        if 0 < len(zidGasit) <= 2:
                            for (cel, iz, zid) in zidGasit:
                                if not (cel.cod & 2 ** iz):
                                    if recent_wall is not None:
                                        pygame.draw.rect(recent_wall[0], recent_wall[1], recent_wall[2])
                                    recent_wall = (stare_curenta.tabla_joc.ecran, Celula.culoareLinii, zid)
                                    pygame.draw.rect(stare_curenta.tabla_joc.ecran, stare_curenta.j_curent.color, zid)
                                    cel.cod |= 2 ** iz
                                    celuleAfectate.append(cel)
                                    new_wall = True

                        if new_wall:
                            # doar de debug
                            print("\nMutarea utilizatorului:")
                            t_dupa = int(round(time.time() * 1000))
                            print("Matrice interfata: ")
                            for l in stare_curenta.tabla_joc.matrCelule:
                                for c in l:
                                    print(c.cod, end=" ")
                                print()
                            thinking_time_user.append(t_dupa - t_user)
                            print("Utilizatorul a \"gandit\" timp de " + str(t_dupa - t_user) + " milisecunde.")
                            got_points = False
                            for celA in celuleAfectate:
                                if celA.cod == 15 and Celula.afisImagini:
                                    stare_curenta.j_curent.score += 1
                                    celA.player = stare_curenta.j_curent
                                    stare_curenta.tabla_joc.deseneazaImag(stare_curenta.tabla_joc.blue_face, celA)
                                    got_points = True
                                    show_score()

                            if not got_points:
                                # t_inainte = int(round(time.time() * 1000))
                                stare_curenta.j_curent = Interfata.jucator_opus(stare_curenta.j_curent)

                    if stare_curenta.tabla_joc.test_final():
                        print("\n===== STATISTICI =====")
                        show_stats(thinking_time_ai, "Timp gandire AI")
                        show_stats(nodes_numbers, "Numar noduri in memorie")
                        pygame.draw.rect(recent_wall[0], recent_wall[1], recent_wall[2])
                        ending_time = int(round(time.time() * 1000))
                        print("Timp rulare: ", ending_time-beginning_time)
                        final_result(ecr, interf)
                        break

            pygame.display.update()

        else:
            # stare_curenta.j_curent = Interfata.jucator_opus(stare_curenta.j_curent)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            print("\nMutarea AI-ului:")
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-100, 100, stare_curenta)
            print("Numarul de noduri: ", NODES_NUMBER)
            print("Estimare: ", stare_actualizata.estimare)
            nodes_numbers.append(NODES_NUMBER)
            NODES_NUMBER = 0
            t_dupa = int(round(time.time() * 1000))
            # stare_actualizata = min_max(stare_curenta)
            # stare_actualizata = alpha_beta(-100, 100, stare_curenta)
            # stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Matrice interfata: ")
            neactualizat = stare_curenta.tabla_joc.matrCelule
            actualizat = stare_actualizata.stare_aleasa.tabla_joc.matrCelule
            for l in actualizat:
                for c in l:
                    print(c.cod, end=" ")
                print()


            # stare_curenta.tabla_joc.deseneaza_grid()
            got_points = False
            for i in range(len(neactualizat)):
                for j in range(len(neactualizat[0])):
                    if neactualizat[i][j].cod != actualizat[i][j].cod:
                        # print(neactualizat[i][j].cod, actualizat[i][j].cod)
                        masca = 1
                        for p in range(4):
                            if not (neactualizat[i][j].cod & masca) and (actualizat[i][j].cod & masca):
                                # print(neactualizat[i][j].cod, actualizat[i][j].cod)
                                if recent_wall is not None:
                                    pygame.draw.rect(recent_wall[0], recent_wall[1], recent_wall[2])
                                recent_wall = (
                                    stare_curenta.tabla_joc.ecran, Celula.culoareLinii, neactualizat[i][j].zid[p])
                                pygame.draw.rect(stare_curenta.tabla_joc.ecran, stare_curenta.j_curent.color,
                                                 neactualizat[i][j].zid[p])
                                neactualizat[i][j].cod += masca
                            masca *= 2
                        if neactualizat[i][j].cod == 15 and Celula.afisImagini:
                            stare_curenta.j_curent.score += 1
                            got_points = True
                            neactualizat[i][j].player = actualizat[i][j].player
                            stare_curenta.tabla_joc.deseneazaImag(stare_curenta.tabla_joc.red_face, neactualizat[i][j])
                            show_score()
            # stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            thinking_time_ai.append(t_dupa - t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            pygame.display.update()

            # print(Interfata.JMAX.score, Interfata.JMIN.score)

            if not got_points:
                t_user = int(round(time.time() * 1000))
                stare_curenta.j_curent = Interfata.jucator_opus(stare_curenta.j_curent)

            if stare_curenta.tabla_joc.test_final():
                pygame.draw.rect(recent_wall[0], recent_wall[1], recent_wall[2])
                pygame.display.update()
                print("\n===== STATISTICI =====")
                show_stats(thinking_time_ai, "Timp gandire AI")
                show_stats(nodes_numbers, "Numar noduri in memorie")
                ending_time = int(round(time.time() * 1000))
                print("Timp rulare: ", ending_time - beginning_time)
                final_result(ecr, interf)

                print("sasadasavdvewvqwvvq")
                break
    print("aaaaaaaaaaaaaasasasa")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
