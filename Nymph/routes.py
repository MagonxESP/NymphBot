from Nymph.nymph import Nymph
from flask import request, Response
from Nymph import app


@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        nymph_bot = Nymph()
        nymph_bot.post(request.form['status'])
        return Response(response=None, status=200)
    else:
        return Response(response=None, status=405)
