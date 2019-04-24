\newcommand {\lfp}         {{\mu}}
\newcommand {\gfp}         {{\nu}}
\newcommand {\onext}       {{\bullet}}
\newcommand {\anext}       {{\circ}}
\newcommand {\always}      {{\square}}
\newcommand {\eventually}  {{\lozenge}}
\newcommand {\walways}     {{\square_w}}
\newcommand {\weventually} {{\lozenge_w}}
\newcommand {\alias}       {{\equiv}}

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
