import SimpleMFRC522

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()
print("hello")
print(type(r))
print(r)

