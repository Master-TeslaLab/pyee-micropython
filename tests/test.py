import sys
sys.path.append('/workspace')
from pyee import *

ee = EventEmitter()

@ee.on('event')
def event_handler():
    print('BANG BANG')

ee.emit('event')
