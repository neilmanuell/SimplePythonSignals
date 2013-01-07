__author__ = 'revisual.co.uk'


class Signal:
    def __init__(self):
        self.__listener_map__ = []
        self.__addOnce_listener_map__ = []
        self.values = []

    def dispatch(self):
        def callListener(listener):
            listener()

        self._loopThruMap(callListener)

    def addOnce(self, listener):
        self.add(listener)
        self.__addOnce_listener_map__.append(listener)

    def add(self, listener):
        if callable(listener):
            self.__listener_map__.append(listener)
        else:
            raise ValueError("listener object passed is not callable")

    def remove(self, listener):
        self.__listener_map__.remove(listener)

    def removeAll(self):
        self.__listener_map__ = []

    def get_length(self):
        return len(self.__listener_map__)

    def _removeIfAddedOnce(self, listener):
        if len(self.__addOnce_listener_map__) > 0 and listener in self.__addOnce_listener_map__:
            self.remove(listener)
            return True
        else:
            return False

    def _loopThruMap(self, callListener):
        count = 0
        while count < len(self.__listener_map__):
            listener = self.__listener_map__[count]
            callListener(listener)
            if not self._removeIfAddedOnce(listener):
                count += 1


class Signal0(Signal):
    pass


class Signal1(Signal):
    def __init__(self, firstValue):
        Signal.__init__(self)
        self.values.append(firstValue)

    def dispatch(self, first):
        if not isinstance(first, self.values[0]):
            raise ValueError(
                "param incorrect type: " + str(self.values[0]) + "expected" + " but received " + str(type(first))
            )

        def callListener(listener):
            listener(first)

        self._loopThruMap(callListener)
