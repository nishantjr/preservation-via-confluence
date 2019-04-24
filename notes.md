\newcommand {\lfp}         {{\mu}}
\newcommand {\gfp}         {{\nu}}
\newcommand {\onext}       {{\bullet}}
\newcommand {\anext}       {{\circ}}
\newcommand {\always}      {{\square}}
\newcommand {\eventually}  {{\lozenge}}
\newcommand {\walways}     {{\square_w}}
\newcommand {\weventually} {{\lozenge_w}}
\newcommand {\alias}       {{\equiv}}
\newcommand {\INT}         {{\mathsf{INT}}}
\newcommand {\NAT}         {{\mathsf{NAT}}}

* $\onext$ one-path next
* $\anext$ all-path next

* Always:           $\always      \phi \alias \gfp X . \phi \land \anext X$
* eventually:       $\eventually  \phi \alias \lfp X . \phi \land \anext X$
* Weak always:      $\walways     \phi \alias \gfp X . \phi \lor (\anext X \land \onext \top)$
* Weak eventually:  $\weventually \phi \alias \gfp X . \phi \lor \onext X$

Preservation as a reachability formula:
$$ \forall t.\; \exists T{:}\mathsf{Type}.\; (t \Rightarrow_a^\exists T \land T \neq \mathsf{badType}) \longrightarrow t \Rightarrow_{ac}^\forall T $$

Preservation as a matching logic formula:
\begin{align*}
& \forall t.\; \exists T{:}\mathsf{Type}.\\
& \left( \bigwedge_{\varphi_1 \Rightarrow \varphi_2 \in A_a} \always(\varphi_1 \rightarrow \onext\weventually \varphi_2) \rightarrow (t \rightarrow (\weventually T \land T \neq \mathsf{badType})) \right) \\
\longrightarrow &\left( \bigwedge_{\varphi_1 \Rightarrow \varphi_2 \in A_{ac}} \always(\varphi_1 \rightarrow \onext\weventually \varphi_2) \rightarrow (t \rightarrow \walways T) \right)
\end{align*}

Example: Consider the following trivial rewrite system with the three rules (here $A_a = A_{ac}$):

* $a \Rightarrow \INT$
* $a \Rightarrow \NAT$
* $\NAT \Rightarrow \INT$

We want to prove $\forall t.\; \exists T.\; t \rightarrow \walways T$. The only non-trivial case is when $t$ is the term $a$, and here we instantiate $T$ to be $\INT$. So the goal becomes $a \rightarrow \walways \INT$.

Unfolding the fixpoint in $\walways$, this becomes $a \rightarrow \INT \lor (\anext \walways \INT \land \onext \top)$. Rearranging, it suffices to show $a \land \neg\INT \rightarrow \anext \walways \INT \land \onext \top$. Since $a \land \neg\INT \equiv a$, we have the equivalent formula $a \land \neg\INT \rightarrow \anext \walways \INT \land \onext \top$. Rearranging again, we get the following formula, representing the two goals we need to show:
$$ (a \rightarrow \anext\walways\INT) \land (a \rightarrow \onext \top) $$
The second conjunct signifying that $a$ is not stuck can be trivially discharged from either of the first two axioms from our operational semantics. For the first conjunct, we replace this with 2 goals for each of the rules that match $a$ on the left-hand side. These become
\begin{align*}
\INT \rightarrow \walways \INT \tag{trivially true} \\
\NAT \rightarrow \walways \INT
\end{align*}

For the second goal, we use the same unfolding we did above, and ultimately have the following formula:
$$ (\NAT \rightarrow \anext\walways\INT) \land (\NAT \rightarrow \onext \top) $$
Similar to before, the second conjunct can be trivially discharged from the third axiom in our operational semantics. And, as there is only one rule matching $\NAT$ on the LHS, the first conjunct is replaced with jsut the one goal of $\INT \rightarrow \walways \INT$, which is trivially true, and we are done.
