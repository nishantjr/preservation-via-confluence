```k
requires "substitution.k"
```

```k
module LAMBDA-SYNTAX
  imports DOMAINS

  syntax Type ::= "int" | "bool"
                | Type "->" Type               [klabel(tyArrow), prefer]
                | "(" Type ")"                 [bracket]

  syntax Val ::= Int | Bool
               | Id
               | "lambda" Id ":" Type "." Exp  [binder]
  syntax Exp ::= Val
               | Exp Exp                       [left]
               | "(" Exp ")"                   [bracket]

  syntax KVariable ::= Id

  syntax Exp ::= Int | Bool
               | Exp "*" Exp          [left]
               | Exp "/" Exp
               > Exp "+" Exp          [left]
               > Exp "<=" Exp

  syntax Exp ::= "if" Exp "then" Exp "else" Exp

  syntax Exp ::= "let" Id ":" Type "=" Exp "in" Exp
  rule let X : T = E in E' => (lambda X : T . E') E                   [macro]

  syntax Exp ::= "letrec" Id ":" Type Id ":" Type "=" Exp "in" Exp
               | "mu" Id ":" Type "." Exp                             [binder]
  rule letrec F : T1  X : T2 = E in E'
    => let F : T1 = mu F : T1 . lambda X : T2 . E in E'               [macro]

  syntax Exp ::= "#hole"

  syntax Exp ::= Type
  syntax Exp ::= Exp "->" Exp [klabel(expArrow)]
endmodule

module LAMBDA-CONFIGURATION
  syntax K ::= "emptyProgram"
  configuration <lambda>
                  <k> $PGM </k>
                  <exec> emptyProgram ~> .K </exec>
                  <type> emptyProgram ~> .K </type>
                </lambda>
endmodule

module EXEC-STRICTNESS
  imports LAMBDA-SYNTAX
  imports LAMBDA-CONFIGURATION

  rule <exec> E1 E2 => E1 ~> #hole E2 ... </exec>
    requires notBool isVal(E1)
  rule <exec> V1:Val E2 => E2 ~> V1 #hole ... </exec>
    requires notBool isVal(E2)
  rule <exec> V1:Val ~> #hole E2 => V1 E2 ... </exec>
  rule <exec> V2:Val ~> V1 #hole => V1 V2 ... </exec>

  rule <exec> E1 + E2 => E1 ~> #hole + E2 ... </exec>
    requires notBool isVal(E1)
  rule <exec> V1:Val + E2 => E2 ~> V1 + #hole ... </exec>
    requires notBool isVal(E2)
  rule <exec> V1:Val ~> #hole + E2 => V1 + E2 ... </exec>
  rule <exec> V2:Val ~> V1 + #hole => V1 + V2 ... </exec>

  rule <exec> E1 * E2 => E1 ~> #hole * E2 ... </exec>
    requires notBool isVal(E1)
  rule <exec> V1:Val * E2 => E2 ~> V1 * #hole ... </exec>
    requires notBool isVal(E2)
  rule <exec> V1:Val ~> #hole * E2 => V1 * E2 ... </exec>
  rule <exec> V2:Val ~> V1 * #hole => V1 * V2 ... </exec>

  rule <exec> E1 / E2 => E1 ~> #hole / E2 ... </exec>
    requires notBool isVal(E1)
  rule <exec> V1:Val / E2 => E2 ~> V1 / #hole ... </exec>
    requires notBool isVal(E2)
  rule <exec> V1:Val ~> #hole / E2 => V1 / E2 ... </exec>
  rule <exec> V2:Val ~> V1 / #hole => V1 / V2 ... </exec>

  rule <exec> E1 <= E2 => E1 ~> #hole <= E2 ... </exec>
    requires notBool isVal(E1)
  rule <exec> V1:Val <= E2 => E2 ~> V1 <= #hole ... </exec>
    requires notBool isVal(E2)
  rule <exec> V1:Val ~> #hole <= E2 => V1 <= E2 ... </exec>
  rule <exec> V2:Val ~> V1 <= #hole => V1 <= V2 ... </exec>

  rule <exec> if P then E1 else E2 => P ~> if #hole then E1 else E2 ... </exec>
    requires notBool(isVal(P))
  rule <exec> V:Val ~> if #hole then E1 else E2
           => if V then E1 else E2
              ...
       </exec>
endmodule

module TYPE-STRICTNESS
  imports LAMBDA-SYNTAX
  imports LAMBDA-CONFIGURATION
  imports EXEC-STRICTNESS

  rule <type> E1 E2 => E1 ~> #hole E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type E2 => E2 ~> T1 #hole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #hole E2 => T1 E2 ... </type>
  rule <type> T2:Type ~> T1 #hole => T1 T2 ... </type>

  rule <type> E1 + E2 => E1 ~> #hole + E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type + E2 => E2 ~> T1 + #hole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #hole + E2 => T1 + E2 ... </type>
  rule <type> T2:Type ~> T1 + #hole => T1 + T2 ... </type>

  rule <type> E1 * E2 => E1 ~> #hole * E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type * E2 => E2 ~> T1 * #hole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #hole * E2 => T1 * E2 ... </type>
  rule <type> T2:Type ~> T1 * #hole => T1 * T2 ... </type>

  rule <type> E1 / E2 => E1 ~> #hole / E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type / E2 => E2 ~> T1 / #hole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #hole / E2 => T1 / E2 ... </type>
  rule <type> T2:Type ~> T1 / #hole => T1 / T2 ... </type>

  rule <type> E1 <= E2 => E1 ~> #hole <= E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type <= E2 => E2 ~> T1 <= #hole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #hole <= E2 => T1 <= E2 ... </type>
  rule <type> T2:Type ~> T1 <= #hole => T1 <= T2 ... </type>

  rule <type> if P then E1 else E2
           => P ~> if #hole then E1 else E2 ... </type>
    requires notBool isType(P)
  rule <type> if P:Type then E1 else E2
           => E1 ~> if P then #hole else E2 ...
       </type>
    requires notBool isType(E1)
  rule <type> if P:Type then E1:Type else E2
           => E2 ~> if P then E1 else #hole ...
       </type>
    requires notBool isType(E2)
  rule <type> T:Type ~> if #hole then E1 else E2
           => if T then E1 else E2
              ...
       </type>
  rule <type> T1:Type ~> if T then #hole else E2
           => if T then T1 else E2
              ...
       </type>
  rule <type> T2:Type ~> if T then T1 else #hole
           => if T then T1 else T2
              ...
       </type>

  rule <type> expArrow(E1, E2)
           => E1 ~> expArrow(#hole -> E2)
              ...
       </type>
    requires notBool isType(E1)
  rule <type> expArrow(T1:Type, E2)
           => E2 ~> expArrow(T1, #hole)
              ...
       </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> expArrow(#hole, E2)
           => T1 -> E2
              ...
       </type>
  rule <type> T2:Type ~> expArrow(T1, #hole)
           => expArrow(T1, T2)
              ...
       </type>
endmodule

module TYPE-FUNCTION
  imports LAMBDA-SYNTAX
  imports LAMBDA-CONFIGURATION
  imports EXEC-STRICTNESS
  imports SUBSTITUTION

  rule <k> PGM => emptyProgram  </k>
       <type> emptyProgram => #type(PGM) </type>
    requires PGM =/=K emptyProgram

  syntax Type ::= "#badType"
  syntax Type ::= #type(Exp) [function]

  rule #type(E1 E2) => #type(#type(E1) E2)
    requires notBool isType(E1)
  rule #type(T1:Type E2) => #type(T1 #type(E2))
    requires notBool isType(E2)

  rule #type(E1 + E2) => #type(#type(E1) + E2)
    requires notBool isType(E1)
  rule #type(T1:Type + E2) => #type(T1 + #type(E2))
    requires notBool isType(E2)

  rule #type(E1 * E2) => #type(#type(E1) * E2)
    requires notBool isType(E1)
  rule #type(T1:Type * E2) => #type(T1 * #type(E2))
    requires notBool isType(E2)

  rule #type(E1 / E2) => #type(#type(E1) / E2)
    requires notBool isType(E1)
  rule #type(T1:Type / E2) => #type(T1 / #type(E2))
    requires notBool isType(E2)

  rule #type(E1 <= E2) => #type(#type(E1) <= E2)
    requires notBool isType(E1)
  rule #type(T1:Type <= E2) => #type(T1 <= #type(E2))
    requires notBool isType(E2)

  rule #type(if P then E1 else E2) => #type(if #type(P) then E1 else E2)
    requires notBool isType(P)
  rule #type(if P:Type then E1 else E2) => #type(if P then #type(E1) else E2)
    requires notBool isType(E1)
  rule #type(if P:Type then E1:Type else E2) => #type(if P then E1 else #type(E2))
    requires notBool isType(E2)

  rule #type(expArrow(E1, E2)) => #type(expArrow(#type(E1), E2))
    requires notBool isType(E1)
  rule #type(expArrow(T1:Type, E2)) => #type(expArrow(T1, #type(E2)))
    requires notBool isType(E2)

  rule #type(_:Int) => int
  rule #type(_:Bool) => bool
  rule #type(int * int) => int
  rule #type(int / int) => int
  rule #type(int + int) => int
  rule #type(int <= int) => bool

  rule #type(expArrow(T1:Type, T2:Type)) => tyArrow(T1, T2)

  rule #type(lambda X : T . E) => #type(expArrow(T, (E[T/X]):Exp))
  rule #type(tyArrow(T1, T2) T1:Type) => T2
  rule #type(if bool then T:Type else T) => T

  rule #type(mu X : T . E) => #type((tyArrow(T, T) (E[T/X])):Exp)

  rule #type(E) => #badType [owise]
endmodule

module LAMBDA-SUBSTITUTION
  imports LAMBDA-SYNTAX
  imports LAMBDA-CONFIGURATION
  imports LAMBDA-CONFIGURATION
  imports SUBSTITUTION

  syntax Exp ::= subst(Exp, Exp, Id)
  rule <exec> subst(E, T, V) => T ~> subst(E, #hole, V) ... </exec>
    requires notBool isVal(T)
  rule <type> subst(E, T, V) => T ~> subst(E, #hole, V) ... </type>
    requires notBool isType(T)

  rule <exec> T:Val  ~> subst(E, #hole, V) => E[T / V] ... </exec>
  rule <type> T:Type ~> subst(E, #hole, V) => E[T / V] ... </type>
endmodule

module EXEC
  imports LAMBDA-SYNTAX
  imports LAMBDA-SUBSTITUTION
  imports EXEC-STRICTNESS

  rule <k> PGM => emptyProgram  </k>
       <exec> emptyProgram => PGM </exec>
    requires PGM =/=K emptyProgram

  syntax KVariable ::= Id

  rule <exec> (lambda X:Id : _:Type . E:Exp) V:Val => E[V / X] ... </exec>

  rule <exec> I1 * I2 => I1 *Int I2 ... </exec>
  rule <exec> I1 / I2 => I1 /Int I2 ... </exec>
  rule <exec> I1 + I2 => I1 +Int I2 ... </exec>
  rule <exec> I1 <= I2 => I1 <=Int I2 ... </exec>

  rule <exec> if true  then E else _ => E ... </exec>
  rule <exec> if false then _ else E => E ... </exec>

  rule <exec> mu X : T . E => E[(mu X : T . E) / X] ... </exec>
endmodule

module TYPES
  imports LAMBDA-SYNTAX
  imports LAMBDA-SUBSTITUTION
  imports TYPE-STRICTNESS
  imports TYPE-FUNCTION
  imports EXEC

  rule <type> expArrow(T1:Type, T2:Type)
           => tyArrow(T1, T2)
              ...
       </type>

  rule <exec> PGM => emptyProgram  </exec>
       <type> emptyProgram => PGM </type>
    requires PGM =/=K emptyProgram

  rule <type> _:Int => int ... </type>
  rule <type> _:Bool => bool ... </type>
  rule <type> int * int => int ... </type>
  rule <type> int / int => int ... </type>
  rule <type> int + int => int ... </type>
  rule <type> int <= int => bool ... </type>

  rule <type> lambda X : T . E => expArrow(T, (E[T/X]):Exp) ... </type>
  rule <type> tyArrow(T1, T2) T1:Type => T2 ... </type>

  rule <type> if bool then T:Type else T => T ... </type>

  rule <type> mu X : T . E => (tyArrow(T, T) (E[T/X])):Exp ... </type>
endmodule
```
