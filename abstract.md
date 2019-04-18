Abstract
========

In this talk, we will discuss two papers:

1. "Type Preservation as a Confluence Problem" by Aaron Stump et al
2. "Confluence by decreasing diagrams" by Vincent van Oostrom

The first paper talks about proving the confluence of the type system for STLC,
STLC with fixed-points, and STLC with polymorphism. It does this by viewing the
type system as a small-step abstract reduction system instead of the more
typical big-step semantics. It then uses decreasing diagrams, introduced in the
next paper, to prove type preservation -- i.e. that the union of the abstract
reduction semantics with the conrete reduction semantics is confluent.

Confluence by decreasing diagram allows us to reduce proving global confluence
to proving local confluence and finding a partial order on a labeling 
of transitions such that each peak can be completed by a valley in a way that is
"consistent" with the partial order on the labels.

In this talk, we will use type preservation of STLC as a motivating example for
Confluence by Decreasing diagrams.
