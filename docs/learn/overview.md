# Overview of effect-oriented programming

When writing usual imperative code, you encounter **side effects**
here and there: functions from Unit (no arguments), functions to Unit 
(no return, returns None), functions that actually transform input data 
and do something else behind your back. In such environments it's very 
easy to do unwanted side effects and cause errors in your programs.

When writing usual functional code, every function is pure. This means it
has no side effects, it cannot write to console, cannot to HTTP requests,
read/write files, communicate with database — i.e. in no way can it modify
the **state**, the environment the program is running in. 

But to write useful programs, you **need** to modify the state: save users,
fetch posts and comments, integrate with existing APIs, save files, etc.
Traditional approach with functional programming is *monads*. Albeit they
provide a way to safely manage these side effects, they have a big problem:
they do not compose. If you have two monads, say IO and Maybe, you cannot
naturally compose them into Maybe(IO(...)), you need to define operations
again and again for each composition.

Effect-oriented programming offers what you can name a "golden middle"
between these two approaches. It is safe and every effect is tracked just
like functional approach, but it's easily composable too. 
