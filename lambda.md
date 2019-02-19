```k
require "substitution.k"
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
endmodule

module LAMBDA-CONFIGURATION
  configuration <lambda>
                  <k> $PGM </k>
                  <exec> .K </exec>
                  <type> .K </type>
                </lambda>
endmodule

module EXEC-STRICTNESS
  imports LAMBDA-SYNTAX
  imports LAMBDA-CONFIGURATION

  syntax Exp ::= "#hole"

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

  syntax Exp ::= "#tyHole"
  syntax Exp ::= Type

  rule <type> E1 E2 => E1 ~> #tyHole E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type E2 => E2 ~> T1 #tyHole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #tyHole E2 => T1 E2 ... </type>
  rule <type> T2:Type ~> T1 #tyHole => T1 T2 ... </type>

  rule <type> E1 + E2 => E1 ~> #tyHole + E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type + E2 => E2 ~> T1 + #tyHole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #tyHole + E2 => T1 + E2 ... </type>
  rule <type> T2:Type ~> T1 + #tyHole => T1 + T2 ... </type>

  rule <type> E1 * E2 => E1 ~> #tyHole * E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type * E2 => E2 ~> T1 * #tyHole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #tyHole * E2 => T1 * E2 ... </type>
  rule <type> T2:Type ~> T1 * #tyHole => T1 * T2 ... </type>

  rule <type> E1 / E2 => E1 ~> #tyHole / E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type / E2 => E2 ~> T1 / #tyHole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #tyHole / E2 => T1 / E2 ... </type>
  rule <type> T2:Type ~> T1 / #tyHole => T1 / T2 ... </type>

  rule <type> E1 <= E2 => E1 ~> #tyHole <= E2 ... </type>
    requires notBool isType(E1)
  rule <type> T1:Type <= E2 => E2 ~> T1 <= #tyHole ... </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> #tyHole <= E2 => T1 <= E2 ... </type>
  rule <type> T2:Type ~> T1 <= #tyHole => T1 <= T2 ... </type>

  rule <type> if P then E1 else E2
           => P ~> if #tyHole then E1 else E2 ... </type>
    requires notBool isType(P)
  rule <type> if P:Type then E1 else E2
           => E1 ~> if P then #tyHole else E2 ...
       </type>
    requires notBool isType(E1)
  rule <type> if P:Type then E1:Type else E2
           => E2 ~> if P then E1 else #tyHole ...
       </type>
    requires notBool isType(E2)
  rule <type> T:Type ~> if #tyHole then E1 else E2
           => if T then E1 else E2
              ...
       </type>
  rule <type> T1:Type ~> if T then #tyHole else E2
           => if T then T1 else E2
              ...
       </type>
  rule <type> T2:Type ~> if T then T1 else #tyHole
           => if T then T1 else T2
              ...
       </type>

  syntax Exp ::= Exp "->" Exp [klabel(expArrow)]
  rule <type> expArrow(E1, E2)
           => E1 ~> expArrow(#tyHole -> E2)
              ...
       </type>
    requires notBool isType(E1)
  rule <type> expArrow(T1:Type, E2)
           => E2 ~> expArrow(T1, #tyHole)
              ...
       </type>
    requires notBool isType(E2)
  rule <type> T1:Type ~> expArrow(#tyHole, E2)
           => T1 -> E2
              ...
       </type>
  rule <type> T2:Type ~> expArrow(T1, #tyHole)
           => expArrow(T1, T2)
              ...
       </type>
       
  rule <type> expArrow(T1:Type, T2:Type)
           => tyArrow(T1, T2)
              ...
       </type>
endmodule

module TYPES
  imports LAMBDA-SYNTAX
  imports SUBSTITUTION
  imports TYPE-STRICTNESS

  rule <k> PGM   => .K  </k>
       <type> .K => PGM </type>

  rule <type> _:Int => int ... </type>
  rule <type> _:Bool => bool ... </type>
  rule <type> int * int => int ... </type>
  rule <type> int / int => int ... </type>
  rule <type> int + int => int ... </type>
  rule <type> int <= int => bool ... </type>

  rule <type> lambda X : T . E => T -> (E[T/X]):Exp ... </type>
  rule <type> tyArrow(T1, T2) T1:Type => T2 ... </type>

  rule <type> if bool then T:Type else T => T ... </type>

  rule <type> mu X : T . E => (tyArrow(T, T) (E[T/X])):Exp .. </type>
endmodule
```

```k
module EXEC
  imports LAMBDA-SYNTAX
  imports SUBSTITUTION
  imports EXEC-STRICTNESS

  rule <k> PGM => .K  </k>
       <exec> .K => PGM </exec>

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
```
