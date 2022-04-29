import sys

from past.builtins import execfile
someFile2= open( "out.txt", "w" )
someFile2.close()

for i in range(100):
    someFile2= open( "out.txt", "a" )
    sys.stdout = someFile2
    execfile( "game.py" )
    someFile2.close()

