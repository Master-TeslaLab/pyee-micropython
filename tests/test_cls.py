import sys
sys.path.append('/workspace')
from pyee import *
from pyee.cls import evented, on

@evented
class Evented:
    @on("event")
    def event_handler(self, *args, **kwargs):
        print(self, args, kwargs)

evented_obj = Evented()

evented_obj.event_emitter.emit(
    "event", "hello world", numbers=[1, 2, 3]
)

help(evented_obj)