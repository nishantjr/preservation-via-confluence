```k
require "substitution.k"
```

```k
module LAMBDA-SYNTAX
  imports DOMAINS

  syntax Type ::= "int" | "bool"
                | Type "->" Type
                | "(" Type ")"                 [bracket]
  syntax Exp ::= Exp "->" Exp                  [strict]

  syntax Val ::= Int | Bool
               | Id
               | "lambda" Id ":" Type "." Exp  [binder]
  syntax Exp ::= Val
               | Exp Exp                       [strict, left]
               | "(" Exp ")"                   [bracket]

  syntax KVariable ::= Id

  syntax Exp ::= Int | Bool
               | Exp "*" Exp          [strict, left]
               | Exp "/" Exp          [strict]
               > Exp "+" Exp          [strict, left]
               > Exp "<=" Exp         [strict]

  syntax Exp ::= "if" Exp "then" Exp "else" Exp                       [strict(1)]

  syntax Exp ::= "let" Id ":" Type "=" Exp "in" Exp
  rule let X : T = E in E' => (lambda X : T . E') E                   [macro]
  
  syntax Exp ::= "letrec" Id ":" Type Id ":" Type "=" Exp "in" Exp
               | "mu" Id ":" Type "." Exp                             [binder]
  rule letrec F : T1  X : T2 = E in E'
    => let F : T1 = mu F : T1 . lambda X : T2 . E in E'               [macro]
endmodule

module TYPES
  imports LAMBDA-SYNTAX
  imports SUBSTITUTION

  syntax KResult ::= Type
  syntax Exp ::= Type
  context if B then HOLE else E2
  context if B then E1   else HOLE

  rule _:Int => int
  rule _:Bool => bool
  rule int * int => int
  rule int / int => int
  rule int + int => int
  rule int <= int => bool

  rule lambda X : T . E => T -> (E[T/X])
  rule (T1 -> T2) T1 => T2

  rule if bool then T:Type else T => T

  rule mu X : T . E => (T -> T):Type (E[T/X])
endmodule
```

```k
module EXEC
  imports LAMBDA-SYNTAX
  imports SUBSTITUTION

  syntax KVariable ::= Id
  syntax KResult ::= Val

  rule (lambda X:Id : _:Type . E:Exp) V:Val => E[V / X]

  rule I1 * I2 => I1 *Int I2
  rule I1 / I2 => I1 /Int I2
  rule I1 + I2 => I1 +Int I2
  rule I1 <= I2 => I1 <=Int I2

  rule if true  then E else _ => E
  rule if false then _ else E => E

  rule mu X : T . E => E[(mu X : T . E) / X]
endmodule
```
