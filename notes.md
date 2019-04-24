\newcommand {\lfp}         {{\mu}}
\newcommand {\gfp}         {{\nu}}
\newcommand {\onext}       {{\bullet}}
\newcommand {\anext}       {{\circ}}
\newcommand {\always}      {{\square}}
\newcommand {\eventually}  {{\diamond}}
\newcommand {\walways}     {{\square_w}}
\newcommand {\weventually} {{\diamond_w}}
\newcommand {\alias}       {{\equiv}}

* $\onext$ one-path next
* $\anext$ all-path next

* Always:           $\always      \phi \alias \gfp X . \phi \and \anext X$
* eventually:       $\eventually  \phi \alias \lfp X . \phi \and \anext X$
* Weak always:      $\walways     \phi \alias \gfp X . \phi \or (\anext \X \and \onext \top)$
* Weak eventually:  $\weventually \phi \alias \gfp X . \phi \or \onext X$

