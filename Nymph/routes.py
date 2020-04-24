from Nymph import nymph_bot
from quart import request, Response
from Nymph import app


@app.route('/post', methods=['POST'])
async def post():
    if request.method == 'POST':
        nymph_bot.post((await request.form)['status'])
        return Response(response="", status=200)
    else:
        return Response(response="", status=405)
