import SimpleMFRC522
import json

master_id = "piopiopiopiopiopiopiopiopiopiopiopiopiopiopiopio"

myReader = SimpleMFRC522.SimpleMFRC522()
r = myReader.read()

print(r[1])

myReader.write(master_id)
with open("test", "w") as list_file:
    json.dump(r[1], list_file)
