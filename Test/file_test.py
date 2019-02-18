with open("gitter.txt","a") as f:

    ssid="niki"
    passwort="1234"

    f.write("\nnetwork={\n   ssid\"="+ssid+"\"\n   psk=\""+passwort+"\"\n}")

with open("gitter.txt", "w") as write_file:
    write_file.write("asdf\u00e4")


