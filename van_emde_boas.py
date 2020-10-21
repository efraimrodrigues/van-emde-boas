#/usr/bin/python3

#universe = 18446744073709551615
universe = 2**24

import sys
import numpy as np
import math
import random

class van_emde_boas:

    def __init__(self, u, block_size = 64, e = 1, cleaning_threshold = 0.25):
        self.__q = 64 #Key size
        self.__block_size = block_size #Size of blocks the key will be split into
        self.__e = e #Doubling and halving constant parameter

        self.__n = 0 #Number of elements in the table
        self.__r = 0 #Number of elements removed from the table
        self.__cleaning_threshold = cleaning_threshold #Threshold parameter for cleaning the table

        self.debug = False #Debugging control

        self.min = None
        self.max = None
        
        self.r = int(np.floor(np.sqrt(u)))

        self.clusters = []
        self.summary = None

        if self.r > 1:
            for i in range(0, self.r):
                self.clusters.append(van_emde_boas(self.r))

    def bin(self, key):
        b = [int(i) for i in list('{0:0b}'.format(key))]

        if len(b) < self.__q:
            b = [0] * (self.__q - len(b)) + b
        
        if len(b) > self.__q:
            raise Exception("Invalid key size.")

        #Breaks binary array into blocks of size self.__block_size
        b = [b[i:i + self.__block_size] for i in range(0, len(b), self.__block_size)]

        return b

    def int(self, b_array):
        return sum(b<<index for index, b in enumerate(b_array[::-1]))

    def __xor(self, x, y):
        return x ^ y

    def __table(self, index, key):
        return self.__lookup[index][key]

    def __resize(self, size):
        old_table = self.table

        self.__n = 0
        self.__r = 0
        self.table = [None] * size

        for element in old_table:
            if element != None and not math.isnan(element):
                self.add(element)

    def __cleaning(self):
        self.__resize(len(self.table))

    def __doubling(self):
        self.__resize(len(self.table) * 2)

    def __halving(self):
        self.__resize(math.ceil(len(self.table) / 2))

    def __hash(self, key):
        t = None

        bin_array = self.bin(key)

        for index, element in enumerate(bin_array):
            if index > 0:
                t = self.__xor(t, self.__table(index, self.int(element)))
            elif index == 0:
                t = self.int(element)

        return t

    def c(self, x):
        return x >> int(self.__q / 2)

    def i(self, x):
        return x & ((1 << int(self.__q/2)) - 1)

    def compose(self, c, i):
        return c << (self.__q / 2) | i

    def successor(self, x):
        if x < self.min:
            return self.min

        c = self.c(x)
        i = self.i(x)
        if i < self.clusters[c].max:
            return self.compose(c, self.clusters[c].successor(i))

        if self.summary != None:
            c = self.summary.successor(c)
            return self.compose(c, self.clusters[c].min)

    def add(self, x):
        if self.min == None:
            self.min = x
            self.max = x
        else:
            if x < self.min:
                aux = self.min
                self.min = x
                x = self.min
            
            if x > self.max:
                self.max = x

            if self.r > 1:
                c = self.c(x)
                i = self.i(x)
                if self.clusters[c].min == None:
                    if self.summary == None:
                        self.summary = van_emde_boas(self.r)
                    self.summary.add(c)
                
                self.clusters[c].add(i)

    def delete(self, key):
        self.__n = self.__n - 1

        h = self.__hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != None and self.table[t] != key and math.isnan(self.table[t]):
            t = (h + i) % m
            i = i + 1

        if self.table[t] == key:
            self.table[t] = float("NaN")
            self.__r = self.__r + 1
        else:
            return [h, -1, False, False, m]

        halving = False
        cleaning = False
        #Checks if it needs halving
        if self.__n < m/4:
            self.__halving()
            halving = True

        #Checks if it needs cleaning
        if self.__r/m > self.__cleaning_threshold:
            self.__cleaning
            cleaning = True

        return [h, t, cleaning, halving, m]

    def search(self, key):
        h = self.__hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != None and self.table[t] != key:
            t = (h + i) % m

            if self.table[t] != None:
                i = i + 1

        if self.table[t] == key:
            return [h, t]
        else:
            return [h, -1]

table = van_emde_boas(universe)

table.add(30)

table.add(10)

table.add(20)

table.add(40)

table.add(35)

table.add(12)