import SimpleMFRC522

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()

print(r[1])
print("length: "+len(r[1]))
myReader.write("")
