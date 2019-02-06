import SimpleMFRC522

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()


print(r[1])
print("length: "+ str(len(r[1])))
print(type(r[r]))