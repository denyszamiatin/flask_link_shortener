import string
import random

import redis
from flask import Flask, render_template, request, redirect

import settings

app = Flask(__name__)


def get_redis_connect():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )


def get_random_code():
    return ''.join(
        random.choice(
            string.digits + string.ascii_letters
        ) for i in range(settings.CODE_LENGTH)
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set')
def set_code():
    r = get_redis_connect()

    while True:
        code = get_random_code()
        if r.setnx(code, request.args.get('href')):
            break
#    while True:
#        code = get_random_code()
#        if r.get(code) is None:
#            break

#    r.set(code, request.args.get('href'))
    return render_template(
        'set.html',
        url=request.args.get('href'),
        short_url=code
    )


@app.route('/<code>')
def re_direct(code):
    r = get_redis_connect()
    url = r.get(code)
    if url is None:
        return render_template('404.html')
    else:
        return redirect(url)


if __name__ == '__main__':
    app.run(debug=True)
