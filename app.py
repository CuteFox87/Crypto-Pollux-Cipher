from flask import Flask, render_template, request
from pollux import pollux_encrypt, pollux_decrypt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '').strip()
        ciphertext = request.form.get('ciphertext', '').strip()
        key = request.form.get('key', '').strip()

        if not key or len(key) != 10 or not all(c in '.-x' for c in key):
            result['error'] = "Key must be exactly 10 characters long and consist of only '.', '-', and 'x'."
        elif plaintext:
            try:
                encrypted, process, key_map = pollux_encrypt(plaintext, key)
                decrypted, process2, key_map = pollux_decrypt(encrypted, key)
                result.update({
                    'mode': 'Encrypt',
                    'plaintext': plaintext,
                    'key': key,
                    'key_map': key_map,
                    'process': process,
                    'encrypted': encrypted,
                    'decrypted': decrypted
                })
            except Exception as e:
                result['error'] = f"Encryption error: {e}"
        elif ciphertext:
            try:
                decrypted, process2, key_map = pollux_decrypt(ciphertext, key)
                result.update({
                    'mode': 'Decrypt',
                    'ciphertext': ciphertext,
                    'key': key,
                    'key_map': key_map,
                    'process': process2,
                    'decrypted': decrypted,
                })
            except Exception as e:
                result['error'] = f"Decryption error: {e}"
        else:
            result['error'] = "Please provide either plaintext or ciphertext."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
