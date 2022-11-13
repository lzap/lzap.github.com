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

# Pomocn� funkce vracej�c� n�hodn� re�ln� ��slo v rozmez� a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Pomocn� funkce vytv��ej�c� matici I x J napln�nou v�stupem fce fill
def makeMatrix(I, J, fill=lambda i,j: 0.0):
    m = []
    for i in range(I):
        m.append([fill(i,j) for j in range(J)])
    return m

# Aktica�n� funkce -- vyzkou�el jsem 1/(1+e^-x) i tanh
def sigmoid(x):
    return math.tanh(x)
    #return 1.0 / (1.0 + math.exp(-x))

# Prvn� derivace aktiva�n� funkce
def dsigmoid(y):
    return 1.0-y*y
    #return y*(1.0-y)

class NN:
    """
    T��da reprezentuj�c� neuronovou s�.
    """

    def __init__(self, ni, nh, no):
        """
        Konstruktor p�eb�r� po�et neuron� vstupn� s�t�, d�le seznam po�tu
        neuron� ve skryt�ch vrstv�ch (jejich po�et je d�n po�tem prvk�
        v tomto seznamu) a kone�n� po�et neuron� v�stupn� vrstvy.
        """
        # do skryt�ch vrstev (krom posledn�) p�id�me jeden neuron nav�c (pr�h)
        for i in xrange(len(nh) - 1):
            nh[i] += 1

        # po�ty vstupn�ch (tak� o jeden nav�c), skryt�ch a v�stpn�ch neuron�
        self.n = list((ni + 1,)) + nh + list((no,))

        # aktiva�n� hodnoty
        self.a = [ [1.0]*x for x in self.n ]
        
        # vytvo�en� vah (matic vah) a nastaven� na n�hodn� hodnoty
        self.w = []
        for i in range(len(self.n)-1):
            self.w.append(makeMatrix(self.n[i],\
                    self.n[i+1], lambda i,j: rand(-1.0, 1.0)))

        # vytvo�en� matic posledn�ch zm�n (pro momentum)
        self.c = []
        for i in range(len(self.n)-1):
            self.c.append(makeMatrix(self.n[i],self.n[i+1]))
    
    def update(self, inputs):
        """
        Metoda pro dop�edn� ���en� sign�lu.

        Na vstupu metoda o�ek�v� vektor vstup�, kter�m je excitov�na vstupn�
        vrstva s�t� a sign�l je ���en a� do v�stupn� vrstvy. V�sledek je vr�cen
        op�t v podob� vektoru (resp. seznamu re�ln�ch ��sel).
        """
        if len(inputs) != self.n[0] - 1:
            raise ValueError, 'spatn� po�et vstup�'

        # modifikace aktiva�n�ch hodnot -- vstupn� vrstva
        for i in range(self.n[0]-1):
            self.a[0][i] = inputs[i]

        # skryt� vrstvy a v�stupn�
        for v in range(len(self.n) - 1):
            for j in range(self.n[v+1]):
                sum = 0.0
                for k in range(self.n[v]):
                    sum += self.a[v][k] * self.w[v][k][j]
                    #print v, k, j, self.a[v][k], self.w[v][k][j], sum, sigmoid(sum), self.a
                self.a[v+1][j] = sigmoid(sum)

        # vr�t�me aktiva�n� hodnoty z v�stupn� vrstvy (kopii)
        return self.a[-1][:]

    def backPropagate(self, targets, N, M):
        """
        Metoda pro zp�tn� ���en� sign�lu.

        O�ek�v� vzorek v�stupu (vektor targets), koeficient u�en� (N)
        a koeficient vlivu p�edchoz�ho kroku (M).
        """
        if len(targets) != self.n[-1]:
            raise ValueError, '�patn� po�et v�stup�: ' + str(targets)

        d = self.a[:]
        # v�po�et odchylek na v�stupu
        d[-1] = [0.0] * self.n[-1]
        for k in range(self.n[-1]):
            error = targets[k] - self.a[-1][k]
            d[-1][k] = dsigmoid(self.a[-1][k]) * error

        # v�po�et odchylek v ostatn�ch vrstv�ch
        for v in range(len(self.n) - 1, 1, -1):
            d[v-1] = [0.0] * self.n[v-1]
            for j in range(self.n[v-1]):
                error = 0.0
                for k in range(self.n[v]):
                    error = error + d[v][k] * self.w[v-1][j][k]
                d[v-1][j] = dsigmoid(self.a[v-1][j]) * error

        # aktualizace synaptick�ch vah
        for v in range(len(self.n) - 1, 0, -1):
            for j in range(self.n[v]):
                for k in range(self.n[v-1]):
                    change = d[v][j] * self.a[v-1][k]
                    self.w[v-1][k][j] += N * change + M * self.c[v-1][k][j]
                    self.c[v-1][k][j] = change

        # v�po�et celkov� chyby
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5 * (targets[k] - self.a[-1][k]) ** 2
        return error

    def test(self, patterns):
        """
        Metoda provede ostestov�n� na testovac�m vzorku a vyp�e v�sledky
        p�ehledn� na standardn� v�stup.

        O�ek�v� seznam vektor� se vstupn�mi hodnotami.
        """
        for p in patterns:
            print "%s -> %s" % (\
                    map(lambda x: str("%+.3f" % x), p),
                    map(lambda x: str("%+.3f" % x), self.update(p)))

    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        """
        Metoda prov�d� vlastn� tr�nov�n�. Na vstupu o�ek�v� seznam vzork�,
        co� je pole, kde prvn� prvek je vstupn� vektor a druh� v�stupn�
        vektor, d�le po�et iterac�, koeficient u�en� a koeficient
        vlivu z p�edchoz�ho kroku.
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
        Konstruktor na�te konfiguraci ze souboru filename a ulo�� hodnoty
        do struktury. T��da je m�n�na jako ve�ejn� struktura (struct).
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

        # interpolujeme vstupy do intervalu 0 a� 1
        minmax = map(lambda x: map(float, x), map(lambda x: x[1:], self.input_labels))
        for p in self.patterns:
            for i in range(len(p[0])):
                p[0][i] = self.interpolate(p[0][i], minmax[i])
        for p in self.tpatterns:
            for i in range(len(p)):
                p[i] = self.interpolate(p[i], minmax[i])

    def interpolate(self, value, minmax):
        """
        Metoda interpoluje hodnotu na interval 0-1. O�ek�v� dvojici
        minmax, kde prvn�m prvkem je minumum a druh�m maximum intevalu
        """
        return (value - minmax[0]) / (minmax[1] - minmax[0])

    def readlines(self, lines = 1):
        """
        T��da na�te jeden nebo v�ce ��dk�, kter� nejsou koment��i nebo
        pr�zdn�mi ��dky, do seznamu �et�zc�. I kdy� se na��t� jen jeden
        ��dek, metoda vrac� seznam (o jednom prvku)!
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
        Na�te jeden ��dek, stejn� jako vol�n� readlines(...)[0].
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
    Uk�zkov� funkce pro u�en� XOR
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

