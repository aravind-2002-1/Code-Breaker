from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode_decode', methods=['POST'])
def encode_decode():
    key = request.form['private_key']
    message = request.form['message']
    mode = request.form['mode']

    if mode == 'e':
        result = Encode(key, message)
    elif mode == 'd':
        result = Decode(key, message)
    else:
        result = 'Invalid Mode'

    return render_template('result.html', result=result)

# function to encode
def Encode(key, message):
    enc = []
    for char in message:
        key_c = key[len(enc) % len(key)]
        encoded_char = chr(ord(char) + ord(key_c))
        enc.append(encoded_char)

    encoded_str = "".join(enc)
    encoded_bytes = encoded_str.encode("utf-8")
    encoded_base64 = base64.urlsafe_b64encode(encoded_bytes).decode("utf-8")
    return encoded_base64

# function to decode
def Decode(key, message):
    dec = []
    decoded_base64 = base64.urlsafe_b64decode(message).decode("utf-8")
    for char in decoded_base64:
        key_c = key[len(dec) % len(key)]
        decoded_char = chr(ord(char) - ord(key_c))
        dec.append(decoded_char)

    return "".join(dec)

if __name__ == '__main__':
    app.run(debug=True)
