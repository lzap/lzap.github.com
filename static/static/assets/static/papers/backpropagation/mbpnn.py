#!/usr/bin/python
# -*- coding: iso-8859-2 -*-
#
# Multilayered BackPropagation Neural Network
#
# Author: Lukas Zapletal -- PUBLIC DOMAIN
#

import sys, os, re
import math
import random
import string
import pdb

random.seed()

# Pomocná funkce vracející náhodné reálné číslo v rozmezí a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Pomocná funkce vytvářející matici I x J naplněnou výstupem fce fill
def makeMatrix(I, J, fill=lambda i,j: 0.0):
    m = []
    for i in range(I):
        m.append([fill(i,j) for j in range(J)])
    return m

# Akticační funkce -- vyzkoušel jsem 1/(1+e^-x) i tanh
def sigmoid(x):
    return math.tanh(x)
    #return 1.0 / (1.0 + math.exp(-x))

# První derivace aktivační funkce
def dsigmoid(y):
    return 1.0-y*y
    #return y*(1.0-y)

class NN:
    """
    Třída reprezentující neuronovou síť.
    """

    def __init__(self, ni, nh, no):
        """
        Konstruktor přebírá počet neuronů vstupní sítě, dále seznam počtu
        neuronů ve skrytých vrstvách (jejich počet je dán počtem prvků
        v tomto seznamu) a konečně počet neuronů výstupní vrstvy.
        """
        # do skrytých vrstev (krom poslední) přidáme jeden neuron navíc (práh)
        for i in xrange(len(nh) - 1):
            nh[i] += 1

        # počty vstupních (také o jeden navíc), skrytých a výstpních neuronů
        self.n = list((ni + 1,)) + nh + list((no,))

        # aktivační hodnoty
        self.a = [ [1.0]*x for x in self.n ]
        
        # vytvoření vah (matic vah) a nastavení na náhodné hodnoty
        self.w = []
        for i in range(len(self.n)-1):
            self.w.append(makeMatrix(self.n[i],\
                    self.n[i+1], lambda i,j: rand(-1.0, 1.0)))

        # vytvoření matic posledních změn (pro momentum)
        self.c = []
        for i in range(len(self.n)-1):
            self.c.append(makeMatrix(self.n[i],self.n[i+1]))
    
    def update(self, inputs):
        """
        Metoda pro dopředné šíření signálu.

        Na vstupu metoda očekává vektor vstupů, kterým je excitována vstupní
        vrstva sítě a signál je šířen až do výstupní vrstvy. Výsledek je vrácen
        opět v podobě vektoru (resp. seznamu reálných čísel).
        """
        if len(inputs) != self.n[0] - 1:
            raise ValueError, 'spatný počet vstupů'

        # modifikace aktivačních hodnot -- vstupní vrstva
        for i in range(self.n[0]-1):
            self.a[0][i] = inputs[i]

        # skryté vrstvy a výstupní
        for v in range(len(self.n) - 1):
            for j in range(self.n[v+1]):
                sum = 0.0
                for k in range(self.n[v]):
                    sum += self.a[v][k] * self.w[v][k][j]
                    #print v, k, j, self.a[v][k], self.w[v][k][j], sum, sigmoid(sum), self.a
                self.a[v+1][j] = sigmoid(sum)

        # vrátíme aktivační hodnoty z výstupní vrstvy (kopii)
        return self.a[-1][:]

    def backPropagate(self, targets, N, M):
        """
        Metoda pro zpětné šíření signálu.

        Očekává vzorek výstupu (vektor targets), koeficient učení (N)
        a koeficient vlivu předchozího kroku (M).
        """
        if len(targets) != self.n[-1]:
            raise ValueError, 'špatný počet výstupů: ' + str(targets)

        d = self.a[:]
        # výpočet odchylek na výstupu
        d[-1] = [0.0] * self.n[-1]
        for k in range(self.n[-1]):
            error = targets[k] - self.a[-1][k]
            d[-1][k] = dsigmoid(self.a[-1][k]) * error

        # výpočet odchylek v ostatních vrstvách
        for v in range(len(self.n) - 1, 1, -1):
            d[v-1] = [0.0] * self.n[v-1]
            for j in range(self.n[v-1]):
                error = 0.0
                for k in range(self.n[v]):
                    error = error + d[v][k] * self.w[v-1][j][k]
                d[v-1][j] = dsigmoid(self.a[v-1][j]) * error

        # aktualizace synaptických vah
        for v in range(len(self.n) - 1, 0, -1):
            for j in range(self.n[v]):
                for k in range(self.n[v-1]):
                    change = d[v][j] * self.a[v-1][k]
                    self.w[v-1][k][j] += N * change + M * self.c[v-1][k][j]
                    self.c[v-1][k][j] = change

        # výpočet celkové chyby
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5 * (targets[k] - self.a[-1][k]) ** 2
        return error

    def test(self, patterns):
        """
        Metoda provede ostestování na testovacím vzorku a vypíše výsledky
        přehledně na standardní výstup.

        Očekává seznam vektorů se vstupními hodnotami.
        """
        for p in patterns:
            print "%s -> %s" % (\
                    map(lambda x: str("%+.3f" % x), p),
                    map(lambda x: str("%+.3f" % x), self.update(p)))

    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        """
        Metoda provádí vlastní trénování. Na vstupu očekává seznam vzorků,
        což je pole, kde první prvek je vstupní vektor a druhý výstupní
        vektor, dále počet iterací, koeficient učení a koeficient
        vlivu z předchozího kroku.
        """
        print "Trenuji sit", self.n
        for i in xrange(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 100 == 0:
                print 'Chyba = %-14f' % error

def toPatterns(x):
    return list(map(float, x.split()))

class ConfigFile:
    def __init__(self, filename):
        """
        Konstruktor načte konfiguraci ze souboru filename a uloží hodnoty
        do struktury. Třída je míněna jako veřejná struktura (struct).
        """
        self.comment = re.compile(r"^\s*#")

        self.file = open(filename, "r")
        self.n_layers = int(self.readline()) # = hidden + output
        self.n_inputs = int(self.readline())
        self.input_labels = map(lambda x: x.split(),\
                self.readlines(self.n_inputs))
        self.num_layers = map(int, self.readline().split())
        self.output_labels = self.readlines(self.num_layers[-1])
        self.learning_rate = float(self.readline())
        self.momentum = float(self.readline())
        self.n_patterns = int(self.readline())
        _patterns = map(lambda x: list(map(float, x.split())),\
                self.readlines(self.n_patterns))
        self.patterns = map(lambda x: \
                [x[0:self.n_inputs], \
                x[self.n_inputs:self.n_inputs+self.num_layers[-1]]], \
                _patterns)
        self.n_tpatterns = int(self.readline())
        self.tpatterns = map(lambda x: list(map(float, x.split())),\
                self.readlines(self.n_tpatterns))
        self.file.close()

        # interpolujeme vstupy do intervalu 0 až 1
        minmax = map(lambda x: map(float, x), map(lambda x: x[1:], self.input_labels))
        for p in self.patterns:
            for i in range(len(p[0])):
                p[0][i] = self.interpolate(p[0][i], minmax[i])
        for p in self.tpatterns:
            for i in range(len(p)):
                p[i] = self.interpolate(p[i], minmax[i])

    def interpolate(self, value, minmax):
        """
        Metoda interpoluje hodnotu na interval 0-1. Očekává dvojici
        minmax, kde prvním prvkem je minumum a druhým maximum intevalu
        """
        return (value - minmax[0]) / (minmax[1] - minmax[0])

    def readlines(self, lines = 1):
        """
        Třída načte jeden nebo více řádků, které nejsou komentáři nebo
        prázdnými řádky, do seznamu řetězců. I když se načítá jen jeden
        řádek, metoda vrací seznam (o jednom prvku)!
        """
        result = []
        for line in self.file:
            line = line.strip()
            if self.comment.match(line) or len(line) == 0:
                continue
            lines -= 1
            if lines == 0:
                result.append(line)
                break
            else:
                result.append(line)
        return result
    
    def readline(self):
        """
        Načte jeden řádek, stejné jako volání readlines(...)[0].
        """
        return self.readlines(1)[0]

    def __str__(self):
        return """NEURONOVA SIT:
        Pocet vrstev: %d
        Pocet vstupu: %d
        Vstupy: %s
        Pocty neuronu: %s
        Koef. uceni: %f
        Koef. vlivu pr. kroku: %f
        Trenovaci mnozina: %s
        Testovaci mnozina: %s
        """ % (self.n_layers, self.n_inputs, self.input_labels, self.num_layers, \
                self.learning_rate, self.momentum, self.patterns, self.tpatterns)

def run(filename, steps = 4000):
    """
    Ukázková funkce pro učení XOR
    """
    conf = ConfigFile(filename)
    print conf

    # create a network with two input, two hidden, and one output nodes
    n = NN(conf.n_inputs, conf.num_layers[:len(conf.num_layers)-1], \
            conf.num_layers[-1])
    
    # train it with some patterns
    n.train(conf.patterns, steps, conf.learning_rate, conf.momentum)

    # test it
    print "Testovaci vzorky " + str(conf.output_labels) + ":"
    n.test(conf.tpatterns)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        run(sys.argv[-2], int(sys.argv[-1]))
    elif len(sys.argv) > 1:
        run(sys.argv[-1])
    else:
        print "Usage: python mbpnn.py configuration.txt [steps]"

# vim: set sw=4 ts=4 sts=4 sta et ai : #

