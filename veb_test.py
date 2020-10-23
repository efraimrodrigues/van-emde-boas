from veb import veb

import random

v = veb(4)

v.add(1)
v.add(2)
v.add(3)

v.delete(3)

v.add(4)
v.add(5)
v.add(6)
v.add(7)

v.delete(7)

v.add(8)
v.add(9)
v.add(10)
v.add(11)

v.delete(11)

v.add(12)
v.add(13)
v.add(14)

v.delete(13)

v.delete(9)

if v.predecessor(10) != 8:
    raise Exception("Predecessor error.")

if v.successor(2) != 4:
    raise Exception("Successor error.")

if v.predecessor(2) != 1:
    raise Exception("Predecessor error.")

v.successor(5)
v.predecessor(8)

v.successor(8)

v.successor(10)

v = veb(64)

v.add(8)
v.add(14)
v.add(24)
v.add(31)
v.add(41)
v.delete(31)
if v.predecessor(41) != 24:
    raise Exception("Predecessor error.")

v.add(49)

if v.predecessor(49) != 41:
    raise Exception("Predecessor error.")
v.delete(41)

if v.successor(24) != 49:
    raise Exception("Successor error.")

v.add(65)
v.delete(65)
v.add(71)
v.delete(71)
v.add(75)
v.delete(75)
v.add(78)
v.add(82)
if v.predecessor(82) != 78:
    raise Exception("Predecessor error.")

v.successor(41)

v.delete(24)
v.delete(14)
if v.predecessor(49) != 8:
    raise Exception("Predecessor error.")

v = veb(64)
v.add(2)
v.add(10)
v.add(17)
v.add(18)

v.delete(17)

v.successor(10)

#Test successor and predecessor methods
"""
table = veb(64)
n = 200
prev = 0
for i in range(n):
    number = random.randint(prev + 1, prev + 10)

    table.add(number)

    if table.successor(prev) != number:
        print("Successor error: ")

    predecessor = table.predecessor(number)
    if prev != 0 and predecessor != prev:
        print("Predecessor error: " + str(predecessor))
    
    prev = number
"""
print("Testing removals.")
#Let's test rmovals
table = veb(64)
n = 200
prev = 0
for i in range(n):
    number = random.randint(prev + 1, prev + 10)

    print(str(number))
    table.add(number)

    if table.successor(prev) != number:
        print("Successor error: ")

    predecessor = table.predecessor(number)
    if prev != 0 and predecessor != prev:
        print("Predecessor error: " + str(predecessor))

    #Let's test removing the predecessor
    if predecessor != None and random.randint(0, 1):
        print("Deleted " + str(predecessor))
        table.delete(predecessor)
        new_predecessor = table.predecessor(number)
        if new_predecessor != None and new_predecessor == predecessor:
            print("Deletion predecessor testing error.")

        successor = table.successor(new_predecessor)
        if successor != None and successor != number:
            print("Deletion successor testing error.")
    
    prev = number
