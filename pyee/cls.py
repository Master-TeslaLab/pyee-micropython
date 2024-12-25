from functools import wraps

from pyee import EventEmitter


class Handler:
    # dataclass
    def __init__(self, event: str, method):
        self.event = event
        self.method = method

class Handlers:
    def __init__(self):
        self._handlers = []

    def append(self, handler):
        self._handlers.append(handler)

    def __iter__(self):
        return iter(self._handlers)

    def reset(self):
        self._handlers = []


_handlers = Handlers()

def on(event: str):
    """
    Register an event handler on an evented class. See the `evented` class
    decorator for a full example.
    """

    def decorator(method):
        _handlers.append(Handler(event=event, method=method))
        return method

    return decorator


def _bind(self, method):
    @wraps(method)
    def bound(*args, **kwargs):
        return method(self, *args, **kwargs)

    return bound

def evented(cls):
    """
    Configure an evented class.

    Evented classes are classes which use an EventEmitter to call instance
    methods during runtime. To achieve this without this helper, you would
    instantiate an `EventEmitter` in the `__init__` method and then call
    `event_emitter.on` for every method on `self`.

    This decorator and the `on` function help make things look a little nicer
    by defining the event handler on the method in the class and then adding
    the `__init__` hook in a wrapper:

    ```py
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
    ```

    The `__init__` wrapper will create a `self.event_emitter: EventEmitter`
    automatically but you can also define your own event_emitter inside your
    class's unwrapped `__init__` method. For example, to use this
    decorator with a `TwistedEventEmitter`::

    ```py
    @evented
    class Evented:
        def __init__(self):
            self.event_emitter = TwistedEventEmitter()

        @on("event")
        async def event_handler(self, *args, **kwargs):
            await self.some_async_action(*args, **kwargs)
    ```
    """
    handlers = list(_handlers)
    _handlers.reset()

    if hasattr(cls, "__init__"):
        og_init = cls.__init__
    else:
        og_init = None

    @wraps(cls.__init__ if og_init else lambda *args, **kwargs: None)
    def init(self, *args, **kwargs):
        if og_init:
            og_init(self, *args, **kwargs)
        if not hasattr(self, "event_emitter"):
            self.event_emitter = EventEmitter()

        for h in handlers:
            self.event_emitter.on(h.event, _bind(self, h.method))

    cls.__init__ = init

    return cls
