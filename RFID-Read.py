import SimpleMFRC522

# empty card
empty_card = "                                                "

# master_id
master_id = "piopiopiopiopiopiopiopiopiopiopiopiopiopiopiopio"


myReader = SimpleMFRC522.SimpleMFRC522()

# read pio part
id = None
while id is None:
    id, pio_text = myReader.read_no_block()

# read swiss pass part
id = None
while id is None:
    id, swiss_text = myReader.read_no_block_swiss_pass()

if len(swiss_text) == 0:
    print("Pio Card")
    try:
        pio_id = int(pio_text)
    except BaseException:
        pio_id = 0
        if pio_text == empty_card:
            print("Empty Card")

        elif pio_text == master_id:
            print("Master Card")

        else:
            print("Unwritten Card")

    print("Id = " + str(pio_id))

else:
    print("Swiss Pass")
    print("Id = " + swiss_text.decode("latin_1"))
