```
# For arithmetic expressions
<Aexpr> ::= <Aexpr> + <Aterm>
	      | <Aexpr> - <Aterm>
		  | <Aterm>

<Aterm> ::= <Aterm> * <Afactor>
		  | <Aterm> / <Afactor>
		  | <Afactor>

<Afactor> ::= ( <Aexpr> )
		    | - <Afactor>
		    | <NUM>
		    | <ID>
		    | <Fappl>    # Function application

# For boolean expressions
<Bexpr> ::= <Bexpr> || <Bterm>
		  | <Bterm>

<Bterm> ::= <Bterm> && <Bfact>
		  | <Bfact>

<Bfact> ::= ( <Bexpr> )
		  | ! <Bfact>
		  | <BOOL>
		  | <ID>
		  | <Fappl>

# For comparisons
<Cexpr> ::= <Cexpr> > <Cterm>
		  | <Cexpr> >= <Cterm>
		  | <Cexpr> < <Cterm>
		  | <Cexpr> <= <Cterm>
		  | <Cexpr> = <Cterm>
		  | <Cexpr> != <Cterm>
		  | <Cterm>

<Cterm> ::= ( <Cexpr> )
		  | <expr>

# Literals
<NUM>
<ID>
<BOOL> ::= true | false
```