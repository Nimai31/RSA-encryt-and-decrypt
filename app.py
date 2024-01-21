from flask import Flask, render_template, request, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("The modular inverse does not exist")
    else:
        return x % m

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = mod_inverse(e, phi)
    return ((n, e), (n, d))

def encrypt(public_key, plaintext):
    n, e = public_key
    encrypted = [pow(char, e, n) for char in plaintext]
    return encrypted

def decrypt(private_key, encrypted):
    n, d = private_key
    decrypted = [chr(pow(char, d, n)) for char in encrypted]
    return ''.join(decrypted)

p = 61  # Prime number 1
q = 53  # Prime number 2
public_key, private_key = generate_keypair(p, q)

@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    try:
        user_input = request.form['encrypt_message']
        ascii_message = [ord(char) for char in user_input]
        encrypted_message = encrypt(public_key, ascii_message)
        return jsonify({'result': encrypted_message})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        user_input = request.form['decrypt_message']
        encrypted_message = [int(char) for char in user_input.split()]
        decrypted_message = decrypt(private_key, encrypted_message)
        return jsonify({'result': decrypted_message})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)