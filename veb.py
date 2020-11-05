from pair import pair
from hash_table import hash_table
import numpy as np
import sys

class veb:

    def __init__(self, w, lookup = None):
        self.w = w

        self.min = None
        self.max = None

        self.clusters = hash_table(lookup = lookup)
        self.__lookup = self.clusters.get_lookup()
        self.summary = None

    def c(self, x):
        return x >> int(self.w / 2)

    def i(self, x):
        return x & ((1 << int(self.w/2)) - 1)

    def compose(self, c, i):
        return (c << int(self.w/2)) | i

    def add(self, x):
        if self.min == None:
            self.min = x
            self.max = x
        else:
            if x < self.min:
                aux = self.min
                self.min = x
                x = aux
            
            if x > self.max:
                self.max = x

            if self.w > 1:
                c = self.c(x)
                i = self.i(x)

                v = self.clusters.search(c)
                if v == None or v.min == None:
                    if self.summary == None:
                        self.summary = veb(self.w/2, lookup=self.__lookup)
                    self.summary.add(c)

                if v == None:
                    v = veb(self.w/2, lookup=self.__lookup)
                    self.clusters.add(pair(c, v))
                
                v.add(i)

    def delete(self, x):
        if x > self.max or x < self.min:
            return

        c = self.c(x)
        i = self.i(x)
        v = self.clusters.search(c)

        if x == self.min:
            cluster = None
            if self.summary != None:
                cluster = self.summary.min

            if cluster == None:
                self.min = None
            else:
                c = cluster
                i = self.clusters.search(cluster).min
                minimum = self.compose(cluster, i)
                if minimum != x or minimum < self.min:
                    self.min = minimum
                    x = self.min
                elif self.max == self.min:
                    self.min = None
                else:
                    self.min = self.max

        if v != None:
            v.delete(i)

            #If we deleted the min but the max is still there. We don't want to erase max and loose its value.
            if v.min == None and v.max != None:
                v.min = v.max
            elif v.min == None and self.summary != None:
                self.summary.delete(c)
                if v.max is None or v.max == x:
                    self.clusters.delete(c)            

        elif x == self.max:
            self.max = self.min
        elif self.w == 1:
            if x == 0 and self.max == 1:
                self.min = 1
            elif x == 0 and self.max == 0:
                self.min = 0
            self.max = self.min
        
        if self.summary != None:
            #If the summary isn't necessary anymore
            if self.summary.min == None:
                self.max = self.min
                self.summary = None
            elif x == self.max:
                c = self.summary.max
                v = self.clusters.search(c)
                self.max = self.compose(c, v.max)

    def successor(self, x):
        if x == None or x >= self.max:
            return None

        if x < self.min:
            return self.min

        c = self.c(x)
        i = self.i(x)
        v = self.clusters.search(c)

        if v != None and i < v.max:
            return self.compose(c, v.successor(i))
        
        #If x isn't in the cluster c, then we inspect the next cluster using summary
        if self.summary != None:
            c = self.summary.successor(c)
            v = self.clusters.search(c)
            return self.compose(c, v.min)
        else:
            return 1

    def predecessor(self, x):
        if x > self.max:
            return self.max

        if x <= self.min:
            return None

        c = self.c(x)
        i = self.i(x)
        v = self.clusters.search(c)

        #If the predecessor is in cluster c
        if v != None and i > v.min:
            return self.compose(c, v.predecessor(i))

        if i > self.min and v != None and i < v.max and i > v.min:
            return self.compose(c, self.min)

        #Summary is only used when we want to change clusters
        if self.summary != None:
            c = self.summary.predecessor(c)
            v = self.clusters.search(c)

            if v != None:
                return self.compose(c, v.max)
            else:
                return self.min
        else:
            return 0

output = open('output.txt', 'w')

table = veb(64)

with open(sys.argv[1]) as fp:
    for line in fp.readlines():
        command = line.strip().split(':')
        operation, value = command
        if operation == 'INC':
            table.add(int(value))
            output.write(operation + ":" + value + "\n\n")
        elif operation == 'REM':
            table.delete(int(value))
            output.write(operation + ":" + value + "\n\n")
        elif operation == 'PRE':
            pre = table.predecessor(int(value))
            output.write(operation + ":" + value + "\n")
            output.write(str(pre) + "\n\n")
        elif operation == 'SUC':
            suc = table.successor(int(value))
            output.write(operation + ":" + value + "\n")
            output.write(str(suc) + "\n\n")