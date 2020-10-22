from pair import pair
from hash_table import hash_table

class veb:

    def __init__(self, w):
        self.__n = 1
        self.w = w

        self.min = None
        self.max = None

        self.clusters = hash_table()
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
                x = self.min
            
            if x > self.max:
                self.max = x

            if self.w > 1:
                c = self.c(x)
                i = self.i(x)

                v = self.clusters.search(c)
                if v == None or v.min == None:
                    if self.summary == None:
                        self.summary = veb(self.w/2)
                    self.summary.add(c)

                if v == None:
                    v = veb(self.w/2)
                    self.clusters.add(pair(c, v))
                
                v.add(i)

                self.__n = self.__n + 1

    def successor(self, x):
        if x < self.min:
            return self.min

        if x >= self.max:
            return None

        c = self.c(x)
        i = self.i(x)
        v = self.clusters.search(c)

        if v != None and i < v.max:
            return self.compose(c, v.successor(i))

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

        if i > self.min and v != None and i <= v.max:
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
