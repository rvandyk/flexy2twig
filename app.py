from flask import Flask, render_template, request
from twigparse import parse

app = Flask(__name__)



@app.route('/data', methods=["POST"])
def data():
    flexy = str(request.form.get('flexycode'))
    print(flexy)

    parsed = parse(flexy)
    return render_template('cp.html', res=parsed, flex=flexy)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cp')
def cp():
    return render_template('cp.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1',debug = True,port=80)
