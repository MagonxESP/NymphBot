from Nymph.nymph import Nymph
from flask import Flask, request, Response


app = Flask(__name__)
nymph_bot = Nymph()


@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        nymph_bot.post(request.form['status'])
        return Response(response=None, status=200)
    else:
        return Response(response=None, status=405)


app.run(host='0.0.0.0')
