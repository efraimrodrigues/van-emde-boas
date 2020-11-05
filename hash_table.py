#/usr/bin/python3

#universe = 18.446.744.073.709.551.615
import sys

import numpy as np
import math
import random

from pair import pair

class hash_table:

    def __init__(self, block_size = 8, e = 0.5, cleaning_threshold = 0.01, lookup = None):
        self.__q = 64 #Key size
        self.__block_size = block_size #Size of blocks the key will be split into
        self.__e = e #Doubling and halving constant parameter
        self.table = [None]
        self.__n = 0 #Number of elements in the table
        self.__r = 0 #Number of elements removed from the table
        self.__cleaning_threshold = cleaning_threshold #Threshold parameter for cleaning the table
        self.__lookup = [] #Lookup tables used for hashing the key

        self.debug = False #Debugging control

        table_size = 2**self.__block_size
        if lookup is None:
            universe = 2**64
            for i in range(0, self.__block_size):
                lookup_table = []
                for i in range(table_size):
                    lookup_table.append(random.randint(0, universe))

                self.__lookup.append(lookup_table)
        else:
            if len(lookup) != self.__block_size:
                raise Exception("Invalid lookup table.")
            
            for i in range(len(lookup)):
                if len(lookup[i]) != table_size:
                    raise Exception("[" + str(i) + "]" + " Invalid lookup table.")

            self.__lookup = lookup

    def __bin(self, key):
        b = [int(i) for i in list('{0:0b}'.format(int(key)))]

        if len(b) < self.__q:
            b = [0] * (self.__q - len(b)) + b
        
        if len(b) > self.__q:
            raise Exception("Invalid key size.")

        #Breaks binary array into blocks of size self.__block_size
        b = [b[i:i + self.__block_size] for i in range(0, len(b), self.__block_size)]

        return b

    def __int(self, b_array):
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
            if element != None and not math.isnan(element.get_key()):
                self.add(element)

    def __cleaning(self):
        self.__resize(len(self.table))

    def __doubling(self):
        self.__resize(len(self.table) * 2)

    def __halving(self):
        self.__resize(math.ceil(len(self.table) / 2))

    def __hash(self, key):
        t = None

        bin_array = self.__bin(key)

        for index, element in enumerate(bin_array):
            if index > 0:
                t = self.__xor(t, self.__table(index, self.__int(element)))
            elif index == 0:
                t = self.__int(element)

        return t

    def get_n(self):
        return self.__n

    def get_lookup(self):
        return self.__lookup

    def add(self, entry):
        self.__n = self.__n + 1

        h = 0
        t = None
        m = len(self.table)

        h = self.__hash(entry.get_key())

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != None and not math.isnan(self.table[t].get_key()):
            t = (h + i) % m
            i = i + 1

        self.table[t] = entry

        doubling = False
        #Checks if it needs doubling
        if m < (1 + self.__e)*self.__n:
            self.__doubling()
            m = len(self.table)
            doubling = True

        return [h, t, doubling, m]

    def delete(self, key):
        self.__n = self.__n - 1

        h = self.__hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != None and (self.table[t].get_key() != key or math.isnan(self.table[t].get_key())):
            t = (h + i) % m
            i = i + 1

        if self.table[t] != None and self.table[t].get_key() == key:
            self.table[t] = pair(float("NaN"),float("NaN"))
            self.__r = self.__r + 1
        else:
            return [h, -1, False, False, m]

        halving = False
        cleaning = False
        #Checks if it needs halving
        if self.__n < m/4:
            self.__halving()
            m = len(self.table)
            halving = True

        #Checks if it needs cleaning
        if self.__r/m > self.__cleaning_threshold:
            self.__cleaning
            cleaning = True

        return [h, t, cleaning, halving, m]

    def search(self, key):
        if key == None:
            return None

        h = self.__hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != None and self.table[t].get_key() != key:
            t = (h + i) % m

            if self.table[t] != None:
                i = i + 1

            #If the whole table has been scanned and the value wasn't found, return None
            if i >= len(self.table):
                return None

        if self.table[t] != None and self.table[t].get_key() == key:
            return self.table[t].get_value()
        else:
            return None

"""output = open('output.txt', 'w')

table = hash_table()

output.write(str(len(table.table)) + "\n\n")

with open(sys.argv[1]) as fp:
    for line in fp.readlines():
        command = line.strip().split(':')
        operation, value = command
        if operation == 'INC':
            h, t, doubling, m = table.add(pair(int(value), int(value)))
            output.write(operation + ":" + value + "\n\n")
            output.write(str(h) + " " + str(t) + "\n\n")

            if doubling:
                output.write("DOBRAR TAM:" + str(m) + "\n\n")
        elif operation == 'REM':
            h, t, cleaning, halving, m = table.delete(int(value))

            output.write(operation + ":" + value + "\n\n")
            output.write(str(h) + " " + str(t) + "\n\n")

            if halving:
                output.write("METADE TAM:" + str(m) + "\n\n")

            if cleaning:
                output.write("LIMPAR\n")
        elif operation == 'BUS':
            h, t = table.search(int(value))

            output.write(operation + ":" + value + "\n\n")
            output.write(str(h) + " " + str(t) + "\n\n")
"""