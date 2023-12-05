from flask import Flask, Response, render_template, request
from utils import announcer, format_sse

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/ping')
def ping():
    msg = format_sse(data={
        'name': request.args.get('name', 'Alaa'),
        'age': request.args.get('age', 22),
        'gender': request.args.get('gender', 'male')
    })
    announcer.announce(msg=msg)
    return {}, 200

@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)