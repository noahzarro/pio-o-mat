import SimpleMFRC522
import time

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()
print(r[1])
