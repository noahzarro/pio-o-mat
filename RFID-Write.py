import SimpleMFRC522
import json

to_write = input("Was schriebe?: ")

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()

print(r[1])
print(type(to_write))
myReader.write(to_write)
with open("test","w") as list_file:
    json.dump(r[1],list_file)