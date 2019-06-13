import SimpleMFRC522

# empty card
empty_card = "                                                "

# master_id
master_id =  "piopiopiopiopiopiopiopiopiopiopiopiopiopiopiopio"


myReader = SimpleMFRC522.SimpleMFRC522()
id, pio_text = myReader.read()

id, swiss_text = myReader.read_swiss_pass()

if len(swiss_text) == 0:
    print("Pio Card")
    try:
        pio_id = int(pio_text)
    except:
        pio_id = 0
        if pio_text == empty_card:
            print("Empty Card")

        if pio_text == master_id:
            print("Master Card")

    print("Id = " + str(pio_id))

else:
    print("Swiss Pass")
    print("Id = " + swiss_text.decode('latin_1'))