import SimpleMFRC522

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()

print("Pio Card:")
print(r[1])
print("length: "+ str(len(r[1])))
print(type(r[1]))

r=myReader.read_swiss_pass()

print("Swiss Pass Card:")
print(r[1])
print("length: "+ str(len(r[1])))
print(type(r[1]))