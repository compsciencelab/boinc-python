print("HELLO FROM THE PAYLOAD")
import os
os.mkdir("output")

f=open( os.path.join( "output", "output.log" ), "w" );
print("HELLO RESULTS", file=f );
f.close()
