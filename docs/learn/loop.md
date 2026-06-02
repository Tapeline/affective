# Effect loop

The last part that finishes the effect system is the effect handler and effect
handling loop.

When an effect is performed, the function just spits it out together with a
continuation to be called later. The actual implementation of the effect lies
on the **effect handler**.

```
name = 
    handle ask_name() with:
        Console.write(text) -> resume with print(text)
        Console.read() -> resume with input()
        return x -> return x

```

This is a very simple handler (that assumes that we have some impure functions
in our language. But this is a tutorial for a **Python** library, after all (: ).

When function performs an effect, the handler receives it and decides what to do.
`resume with X` calls the continuation that was passed 