import base64
from io import BytesIO

import requests
from PIL import Image
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/preds", methods=['POST'])
def submit():
    cloth = request.files['cloth']
    model = request.files['model']

    ## replace the url from the ngrok url provided on the notebook on server.
    url = "http://2c58-34-147-107-125.ngrok.io/api/transform"
    print("sending")
    response = requests.post(url=url, files={"cloth": cloth.stream, "model": model.stream})
    content = BytesIO(response.content)
    op = Image.open(content)

    buffer = BytesIO()
    op.save(buffer, 'png')
    buffer.seek(0)

    data = buffer.read()
    data = base64.b64encode(data).decode()

    return render_template('index.html', op=data)
    # return render_template('index.html', test=True)


if __name__ == '__main__':
    app.run(debug=True)
