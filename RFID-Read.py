import SimpleMFRC522

myReader = SimpleMFRC522.SimpleMFRC522()
r=myReader.read()

print("Pio Card:")
print(r[1].decode('latin_1'))
print("length: "+ str(len(r[1])))
print(type(r[1]))

r=myReader.read_swiss_pass()

print("Swiss Pass Card:")
print(r[1].decode('latin_1'))
print("length: "+ str(len(r[1])))
print(type(r[1]))

id = None

while id == None:
    id, text = myReader.read_no_block_middle()

print("Swiss Middle:")
print(text.decode('latin_1'))
print("length: "+ str(text))
print(type(text))