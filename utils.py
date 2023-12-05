import queue
import json

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