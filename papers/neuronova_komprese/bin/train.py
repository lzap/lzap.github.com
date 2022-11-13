#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from rgbimg import *
from snns import krui,util
from sys import argv

ImageBoundsError = "Image width or size not divisible by 8"
InternalError = "Internal error"

class image:

	"""Nahrává obrázek ve formátu RGBA (SGI .rgb). Čísla jsou uložena v
	řetězci ARGB"""
	def load(self, file):
		self._data = []
		(self._width, self._height) = sizeofimage(file)
		print "Obrázek načten, rozměry:", self._width, self._height
		if self._width % 8 != 0 or self._height % 8 != 0:
			raise ImageBoundsError

		rawdata = longimagedata(file)
		i = 0
		for x in rawdata:
			x = ord(x)
			if (i + 1) % 4 == 0:
				self._data.append(x)
			i += 1
	
	def store(self, file):
		data = ""
		for x in self._data:
			data += chr(255) + chr(x) * 3
		if len(data) != self._width * self._height * 4:
			raise InternalError
		longstoimage(data, self._width, self._height, 1, file)

	def blank(self):
		for i in xrange(len(self._data)):
			self._data[i] = 0

	def getBlock(self, index):
		result = []
		wb = self._width / 8
		v = (index / wb) * 8 * self._width # nad blokem
		h = (index % wb) * 8 # zleva
		for y in xrange(8):
			for x in xrange(8):
				result.append(self._data[v+h+x+self._width*y])
		return result

	def getBlockCount(self):
		return len(self._data) / 64

	def setBlock(self, index, block):
		wb = self._width / 8
		v = (index / wb) * 8 * self._width # nad blokem
		h = (index % wb) * 8 # zleva
		b = 0
		for y in xrange(8):
			for x in xrange(8):
				self._data[v+h+x+self._width*y] = block[b]
				b += 1

	def __iter__(self):
		self._ix = 0
		self._blocks = self.getBlockCount()
		return self

	def next(self):
		if self._ix >= self._blocks:
			raise StopIteration
		block = self.getBlock(self._ix)
		self._ix = self._ix + 1
		return block

# pomocne funkce
def pix2real(p):
	return p * (2.0/255.0) - 1.0

def real2pix(r):
	return int(r * 128.0 + 127.5)

krui.setLearnFunc('BackpropBatch')
krui.setUpdateFunc('Topological_Order')
krui.setUnitDefaults(1,0,krui.INPUT,0,1,'Act_TanH','Out_Identity')

print "Nahrávám obrázek"

im = image()
im.load("beerfox2.rgb")
print "Velikost:", len(im._data)

print "Konstruuji síť"

vnejsi_vrstvy = 8 * 8
vnitrni_vrstva = 4 * 4

# vstupni vrstva 8x8 (64 neuronu)
pos = [0,0,0]
inputs = []
for i in range(1, vnejsi_vrstvy + 1) :
	pos[0] = i
	num = krui.createDefaultUnit()
	inputs.append(num)
	krui.setUnitName(num,'Input_%i' % i)
	krui.setUnitPosition(num, pos)

# skryta vrstva 4x4 (16 neuronu)
pos[1]=2
hidden = []
for i in range(1, vnitrni_vrstva + 1) :
	pos[0] = i + 3
	num = krui.createDefaultUnit()
	hidden.append(num)
	krui.setUnitName(num,'Hidden_%i' % i)
	krui.setUnitTType(num,krui.HIDDEN)
	krui.setUnitPosition(num,pos)
	krui.setCurrentUnit(num)
	for src in inputs :
		krui.createLink(src,0)

# vystupni vrstva 8x8 (64)
pos[1]=4
outputs = []
for i in range(1, vnejsi_vrstvy + 1) :
	pos[0] = i
	num = krui.createDefaultUnit()
	outputs.append(num)
	krui.setUnitName(num,'Output_%i' % i)
	krui.setUnitTType(num,krui.OUTPUT)
	krui.setUnitPosition(num,pos)
	krui.setCurrentUnit(num)
	for src in hidden :
		krui.createLink(src,0)

print "Vytvářím vzorky pro SNNS"

krui.deleteAllPatterns()
patset = krui.allocNewPatternSet()
for block in im:
	for i in xrange(vnejsi_vrstvy) :
		krui.setUnitActivation(inputs[i], pix2real(block[i]))
		krui.setUnitActivation(outputs[i], pix2real(block[i]))
	krui.newPattern()

krui.initializeNet(-1,1)
krui.shufflePatterns(1)
krui.DefTrainSubPat()

pruch_1 = int(argv[1])
pruch_2 = int(argv[2])

print "Fáze učení (%d+%d průchodů)" % (pruch_1, pruch_2)

i=0
# první fáze učení
while i < pruch_1:
	res = krui.learnAllPatterns(0.3, 0.1)
	if not i % 100 : print "Fáze 1, chyba v cyklu %d:" % i, res[0]
	i = i + 1

# druhá fáze (jemnější)
i=0
while i < pruch_2:
	res = krui.learnAllPatterns(0.03, 0.1)
	if not i % 100 : print "Fáze 2, chyba v cyklu %d:" % i, res[0]
	i = i + 1

print "Rekonstruuji původní obrázek"

im.blank()

for p in xrange(krui.getNoOfPatterns()):
	krui.setPatternNo(p + 1)
	krui.showPattern(1);
	krui.updateNet()
	block = []
	for u in xrange(64 + 16 + 1, 64 * 2 + 16 + 1):
		block.append(real2pix(krui.getUnitActivation(u)))
	im.setBlock(p, block)

print "Zapisuji výsledný obrázek na disk"

im.store("compressed.rgb")			

print "Vytvářím soubor vzorků pro SNNS"
krui.saveNewPatterns('image.pat', patset)
print "Vytvářím soubor sítě pro SNNS"
krui.saveNet('image.net','image')

# konec
