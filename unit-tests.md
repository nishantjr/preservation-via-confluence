In this file, we test the three semantics (Exection, typing via rewrites and
typing via the `#type` function) in isolation. This is to assure ourselves of
their individual correctness.

```k
module UNIT-TESTS-SPEC
    imports LAMBDA-COMBINED
```

```k
    syntax Id ::= "a" [token] | "b" [token] | "c" [token] | "d" [token]
                | "f" [token]
                | "x" [token] | "y" [token] | "z" [token]
```

Execution reduction semantics
===============

```k
    rule <exec> 1/(2/3)
             => 1 / 0
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> (1 + 2 * 3) / 4 <= 1
             => true
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> letrec f : (int -> int) x : int
                     = if   x <= 1
                       then 1 else (x * (f (x + -1)))
                  in (f 10)
             => 3628800
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> (mu f : int -> int . lambda x : int . if x <=1 then x else ((f (x + -1)) + (f (x + -2)))) 7
             => 13
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> a (((lambda x:int.lambda y:int.x) y) z)
             => ( a y )
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> lambda x : int . x
             => lambda x : int . x
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> if 2<=1 then 3/0 else 10
             => 10
         </exec>
         <k> .K </k>
         <type> .K </type>

    rule <exec> let a : int = 1 in
                  let b : int = 2 in
                    let c : int = 3 in
                      let d : int = 4 in
                        ((a+b*c)/d <= a)
             => true
         </exec>
         <k> .K </k>
         <type> .K </type>
```

Typing reduction semantics
==========================

```k
    rule <type> 1 + (3 <= 4)
             => int + bool
         </type>
         <k> .K </k>
         <exec> .K </exec>

    rule <type> letrec f : int->int x:int = if x <= 1 then 1 else (x * (f (x + -1)))
                in (f 10)
             => int
         </type>
         <k> .K </k>
         <exec> .K </exec>

    rule <type> let x:bool = true
                in let x:int = if x then 1 else 2
                   in x
             => int
         </type>
         <k> .K </k>
         <exec> .K </exec>
```

Type Function tests
===================

```k
    rule <k> #type(1 + (3 <= 4))
          => #badType
         </k>
         <type> .K </type>
         <exec> .K </exec>

    rule <k> #type( letrec f : int->int x:int = if x <= 1 then 1 else (x * (f (x + -1)))
                    in (f 10)
                  )
             => int
         </k>
         <type> .K </type>
         <exec> .K </exec>

    rule <k> #type( let x:bool = true
                    in let x:int = if x then 1 else 2
                       in x
                  )
             => int
         </k>
         <type> .K </type>
         <exec> .K </exec>
```

Combined reduction semantics
============================

```k
    rule <exec> 1/(2/3)
             => .K
         </exec>
         <type> .K => int </type>
         <k> #moveExecToType => .K </k>

    rule <exec> (1 + 2 * 3) / 4 <= 1
             => .K
         </exec>
         <type> .K => bool </type>
         <k> #moveExecToType => .K </k>

    rule <exec> letrec f : (int -> int) x : int
                     = if   x <= 1
                       then 1 else (x * (f (x + -1)))
                  in (f 10)
             => .K
         </exec>
         <type> .K => int </type>
         <k> #moveExecToType => .K </k>

    rule <exec> (mu f : int -> int .
                    lambda x : int .
                        if x <=1
                        then x
                        else ((f (x + -1)) + (f (x + -2))))
                7
             => .K
         </exec>
         <type> .K => int </type>
         <k> #moveExecToType => .K </k>

    rule <exec> lambda x : int . x
             => .K
         </exec>
         <type> .K => int -> int </type>
         <k> #moveExecToType => .K </k>

    rule <exec> if 2<=1 then 3/0 else 10
             => .K
         </exec>
         <type> .K => int </type>
         <k> #moveExecToType => .K </k>

    rule <exec> let a : int = 1 in
                  let b : int = 2 in
                    let c : int = 3 in
                      let d : int = 4 in
                        ((a+b*c)/d <= a)
             => .K
         </exec>
         <type> .K => bool </type>
         <k> #moveExecToType => .K </k>
```

```k
endmodule
```
