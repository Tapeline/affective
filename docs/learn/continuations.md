# Continuations

In order to understand how effect systems are even possible, we need to
introduce the concept of **delimited continuations**.

> Delimited continuation is a part of a computational sequence, which can
> be resumed at any time later.

Imagine we have a program (pseudocode, imaginary language):

```
func f():
    print(1)
    yield
    print(2)
    yield
    print(3)
```

These `yield`s mark points were our program will pause and return a continuation
to be resumed later:

```
>>> cont1 = f()
1
>>> cont2 = cont1()
2
>>> cont3 = cont2()
3
>>> cont3
EndOfExecution(None)
```

This may seem like to you like Python's generators. In fact, you are partially
right: delimited continuations are a generalisation of generators (but not 
only of them!). However, Python generators are one-shot, whereas true
delimited continuations are almost always multi-shot. This means that we can
resume many times from the same point:

```
>>> cont1 = f()
1
>>> cont2A = cont1()
2
>>> cont2B = cont1()  # resuming another time!
2
>>> cont3A = cont2A()
3
>>> cont3B = cont2B()
3
>>> cont3A
EndOfExecution(None)
>>> cont3B
EndOfExecution(None)
```

Python generators do not allow that. More generally, in Python the only safe
way to achieve multi-shot continuations is by using the Continuation
Passing Style, which we won't cover in this document. You can find out more
online.

Now that you know that we can pause and resume computations, we can move
onto the next topic.
