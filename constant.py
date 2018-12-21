# Contains all constants used throughout the program
from panda3d.core import Vec4

# Colors
### Checkerboard colors
VANILLA = Vec4(0.953, 0.898, 0.671, 1)
WALNUT = Vec4(.416, 0.263, .177, 1)
### Pieces colors
# NOTE: pieces have alpha value that is used for moving pieces
WHITEP = Vec4(0.941, 0.871, 0.584, 0.5)
BLACKP = Vec4(0.1, 0.1, 0.1, 0.5)
### Colors used for highlighting squares
SELECT = Vec4(0, 1, 0.741, 1)
HIGHLIGHT = Vec4(0.224, 0.428, 0.518, 0.7)

WHITE = Vec4(1,1,1,1)
BLACK = Vec4(0,0,0,1)

HELPSTRING = "HELP\n\nRules:\n\t1. All standard rules of chess hold with the" +\
" following changes\n\t2. Kings and queens are \'big\' pieces that cannot" +\
" move into the upper board but can capture on both \n\t   boards (capturing t" +\
"wo pieces simultaneously is possible).\n\t3. All pieces can move and captu" +\
"re directly upward (with the exception of knights)\n\t4. Knights can mov" +\
"e in a now three dimensional \'L\' shape, allowing them to capture piece" +\
"s above \n\t   and to the side from them.\n\t5. All pieces (including knights) " +\
"from the upper \n\t   board can only capture pieces also on the upper board or " +\
"pieces directly below them.\n\t\ta. Kings and queens can only be attacke" +\
"d from the lower board.\n\t6. All pieces (except knights, kings, and que" +\
"ens) can now move vertically up/down.\n\t7. Pawns cannot promote to a qu" +\
"een from the upper board, and can capture pieces pieces directly above\n\t   " +\
" them when promoting to a queen from the lower board.\n\nControls:\n\t- Use" +\
" arrow keys to move horizontally\n\t- Use \'/\' to switch boards\n\t- Pre" +\
"ss enter to select a piece/move\n\t- Press shift or space to unselect a p" +\
"piece/cancel a move\n\t- Press \'h\' to show help screen"