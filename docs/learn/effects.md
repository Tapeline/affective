# Effects

Effects can essentially be understood as orders to do something to the
environment or as capabilities to do so.

Let's define an effect for communicating via console:

```
effect Console:
    read() -> str
    write(text: str) -> None
```

This effect defines two operations. In Affective we treat effects as 
capabilities that group together related actions. 

Here's the catch, when we **perform** an effect, the computation
pauses at this moment and returns the effect with the continuation
to be called with the effect's result after the effect is handled:

```
func ask_name():
    perform Console.write("What's your name?")
    name = perform Console.read()
    return name
    
>>> eff, then = ask_name()
(Console.write("What's your name?"), Continuation)
>>> eff, then = then(None)
(Console.read(), Continuation)
>>> eff, then = then("Mark")
(None, EndOfExecution("Mark"))
```

A quite cool thing rises from this behaviour. As we've already
separated the call time and response time, our program automatically
became asynchronous!


