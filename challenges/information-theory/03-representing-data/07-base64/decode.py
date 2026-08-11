import base64

with open("mystery.jpeg.base64", "r") as file:
    encoded_data = file.read()

decoded_data = base64.b64decode(encoded_data)

with open("mystery.jpeg", "wb") as file:
    file.write(decoded_data)