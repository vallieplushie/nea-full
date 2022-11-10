#!/bin/bash

PGFDIR=~/code/tex/pgf/

HEADER='--------------------------------------------------------------------------------------------------
------ This file is a copy of some part of PGF/Tikz.
------ It has been copied here to provide :
------  - compatibility with older PGF versions
------  - availability of PGF contributions by Christian Feuersaenger
------    which are necessary or helpful for pgfplots.
------
------ For reasons of simplicity, I have copied the whole file, including own contributions AND
------ PGF parts. The copyrights are as they appear in PGF.
------
------ Note that pgfplots has compatible licenses.
------ 
------ This copy has been modified in the following ways:
------  - nested \input commands have been updated
------  
--
-- Support for the contents of this file will NOT be done by the PGF/TikZ team. 
-- Please contact the author and/or maintainer of pgfplots (Christian Feuersaenger) if you need assistance in conjunction
-- with the deployment of this patch or partial content of PGF. Note that the author and/or maintainer of pgfplots has no obligation to fix anything:
-- This file comes without any warranty as the rest of pgfplots; there is no obligation for help.
----------------------------------------------------------------------------------------------------'

HEADER="$HEADER\n-- Date of this copy: `date` ---\n\n\n"

DIR=$PGFDIR/generic/pgf/libraries/luamath
FILES=(\
	pgf/luamath/functions.lua \
	pgf/luamath/parser.lua \
)

# copy pgf/luamath/functions.lua
# ->   pgfplotsoldpgfsupp/luamath/functions.lua

for A in "${FILES[@]}"; do
	echo "creating compatibility version for $A ... " 
	NEWLOCATION=pgfplotsoldpgfsupp/${A#pgf/}

	#sed 's/local \([a-z]*\) = \([a-z]*\) or {}/local \1 = {} -- or \2 (backw. compat: override)/' | \

	mkdir -p `dirname $NEWLOCATION`
	echo -e "$HEADER" | \
		cat - "$DIR/$A" | \
		sed 's/require("\(pgf\|tikz\)\.\(.*\)/require("pgfplotsoldpgfsupp.\2/' | \
		cat > $NEWLOCATION \
		|| exit 1
done

