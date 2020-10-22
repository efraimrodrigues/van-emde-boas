from veb import veb

import random


v = veb(4)

v.add(0)
v.add(1)
v.add(2)

v.add(5)

v.add(8)
v.add(9)
v.add(10)
v.add(11)

v.predecessor(10)

v.successor(2)
v.predecessor(2)

v.successor(5)
v.predecessor(8)

v.successor(8)

v.successor(10)


print(v)



table = veb(32)

n = 200

prev = None
for i in range(n):
    
    table.add(i)

    if table.predecessor(i) != prev:
        print("Error")

    prev = i
