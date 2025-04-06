from flask import Flask, render_template, request
from pollux import pollux_encrypt, pollux_decrypt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        key = request.form.get('key')

        if not plaintext or not key or len(key) != 10:
            result['error'] = "Please enter a plaintext and a 10-character key (only '.', '-', 'x')."
        else:
            try:
                encrypted, morse_text, key_map = pollux_encrypt(plaintext, key)
                decrypted = pollux_decrypt(encrypted, key)
                result = {
                    'plaintext': plaintext,
                    'key': key,
                    'morse_text': morse_text,
                    'key_map': key_map,
                    'encrypted': encrypted,
                    'decrypted': decrypted
                }
            except Exception as e:
                result['error'] = f"Error: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
