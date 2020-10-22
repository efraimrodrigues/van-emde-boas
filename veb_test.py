from veb import veb

import random


v = veb(64)

v.add(0)
v.add(1)
v.add(2)

v.add(5)

v.delete(6)

v.delete(5)

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

#Test successor and predecessor methods
#"""
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
#"""
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
        table.delete(predecessor)
        new_predecessor = table.predecessor(number)
        if new_predecessor == predecessor:
            print("Deletion predecessor testing error.")

        successor = table.successor(new_predecessor)
        if successor != number:
            print("Deletion successor testing error.")
    
    prev = number
