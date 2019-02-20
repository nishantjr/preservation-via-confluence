```k
module CONFLUENCE-SPEC
  imports LAMBDA-COMBINED
  rule <k> .K </k>
       <exec> E:Exp => .K </exec>
       <type> .K => #type(E) </type>
    requires #type(E) =/=K #badType
endmodule
```
