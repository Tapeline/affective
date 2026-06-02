# Effectful functions typing

We've covered the first component that defines the effect system:
the effects themselves, and slightly touched the second component:
effectful functions.

Effectful functions are (surprise-surprise!) functions that perform
effects. We've already seen one:

```
func ask_name():
    perform Console.write("What's your name?")
    name = perform Console.read()
    return name
```

Though we have omitted the type signature. Let's fix that:

```
func ask_name() -> str / { Console }:
    perform Console.write("What's your name?")
    name = perform Console.read()
    return name
```

We can see that it returns `str`, which is logical. Then we see a new 
construction: the effect signature. Following the slash, we can list
all the effects (capabilities) this function requires in the execution
context to be performed. 

This way we can track, which functions are pure (have signature
`T / {}`, where `T` is some type) or effectful (where set after the slash
is not empty). And we can track what effects exactly this function
performs. We will see how it comes in handy right in the next chapter.
