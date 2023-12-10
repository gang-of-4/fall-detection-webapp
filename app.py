from flask import Flask, Response, render_template, request
import queue
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
                
def format_sse(data: object, event=None) -> str:
    msg = f'data: {json.dumps(data)}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

announcer = MessageAnnouncer()

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/ping', methods=['POST'])
def ping():
    # Assuming the data is sent as JSON in the request body
    data = request.get_json()

    name = data.get('name', 'Unknown')
    age = data.get('age', 'Unknown')
    gender = data.get('gender', 'unknown')

    msg = format_sse(data={'name': name, 'age': age, 'gender': gender})
    announcer.announce(msg=msg)

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