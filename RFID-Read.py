import SimpleMFRC522
import time

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()
print(type(r[1]))
print(r[1])

myReader.write("gitter")

time.sleep(3)

r=myReader.read()
print(type(r[1]))
print(r[1])