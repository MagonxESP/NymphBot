from Nymph.nymph import Nymph
from flask import Flask, request

app = Flask(__name__)
nymph_bot = Nymph()


@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        nymph_bot.post(request.form['status'])


app.run(host='0.0.0.0')
