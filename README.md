# Van Emde Boas implemented with simple tabulation hashing with linear probing, doubling, and halving.

A Van Emde Boas data structure implementation.

# How to use it
You can either import the veb.py file and use the class' methods or run it by passsing a input file as argument.

If you choose to give it an input file. Make sure each line has one of the following commands:

INC:x (Inserts x)

REM:x (Removes x)

PRE:x (Returns x's predecessor)

SUC:x (Returns x's successor)

Input file example:

```txt
INC:10
INC:20
INC:30
INC:37
SUC:10
SUC:15
PRE:42
REM: 37
PRE:42
```

Here's an example of how you can do it if your input file is named input.txt: 

`python3 veb.py input.txt`

A file named output.txt with predecessors's and successors's values will be generated once you run it.
