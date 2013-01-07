from unittest import TestCase

from signals import Signal, Signal0, Signal1


class SignalTestCase_listeners(TestCase):
    def setUp(self):
        self.baseSignal = Signal()

    def tearDown(self):
        self.baseSignal = None

    def test_default_length_zero(self):
        self.assertEqual(0, self.baseSignal.get_length())

    def test_listener_is_added(self):
        self.baseSignal.add(self.listenerOne)
        self.assertEqual(1, self.baseSignal.get_length())

    def test_add_listener_is_callable(self):
        self.assertRaises(ValueError, self.baseSignal.add, 10)

    def test_listener_is_added_once(self):
        self.baseSignal.add(self.listenerOne)
        self.assertEqual(1, self.baseSignal.get_length())

    def test_add_once_listener_is_callable(self):
        self.assertRaises(ValueError, self.baseSignal.addOnce, 10)

    def test_listener_is_removed(self):
        self.baseSignal.add(self.listenerOne)
        self.baseSignal.remove(self.listenerOne)
        self.assertEqual(0, self.baseSignal.get_length())

    def test_all_listeners_are_removed(self):
        self.baseSignal.add(self.listenerOne)
        self.baseSignal.add(self.listenerTwo)
        self.baseSignal.removeAll()
        self.assertEqual(0, self.baseSignal.get_length())

    def listenerOne(self):
        pass

    def listenerTwo(self):
        pass


class SignalTestCase_dispatching(TestCase):
    def setUp(self):
        self.signal = Signal0()
        self.listenerOneCount = 0

    def tearDown(self):
        self.signal = None
        self.listenerOneCount = None

    def test_single_added_listener_called_on_multiple_dispatch(self):
        self.signal.add(self.listener)
        self.signal.dispatch()
        self.signal.dispatch()
        self.signal.dispatch()
        self.assertEqual(3, self.listenerOneCount)

    def test_multiple_added_listeners_called_on_single_dispatch(self):
        self.signal.add(self.listener)
        self.signal.add(self.listener)
        self.signal.add(self.listener)
        self.signal.dispatch()
        self.assertEqual(3, self.listenerOneCount)

    def test_single_once_added_listener_called_once_on_multiple_dispatch(self):
        self.signal.addOnce(self.listener)
        self.signal.dispatch()
        self.signal.dispatch()
        self.signal.dispatch()
        self.assertEqual(1, self.listenerOneCount)

    def test_multiple_once_added_listeners_all_called_on_single_dispatch(self):
        self.signal.addOnce(self.listener)
        self.signal.addOnce(self.listener)
        self.signal.addOnce(self.listener)
        self.signal.dispatch()
        self.assertEqual(3, self.listenerOneCount)

    def listener(self):
        self.listenerOneCount += 1


class Signal1TestCase(TestCase):
    def setUp(self):
        self.value = set
        self.signal = Signal1(self.value)
        self.valuesReceived = []

    def tearDown(self):
        self.value = None
        self.signal = None
        self.valuesReceived = None

    def test_values_are_passed_from_constructor(self):
        receivedValue = self.signal.values[0]
        self.assertEqual(self.value, receivedValue)

    def test_values_dispatched(self):
        valueOne = {"valueOne"}
        valueTwo = {"valueTwo"}
        self.signal.add(self.listener)
        self.signal.dispatch(valueOne)
        self.signal.dispatch(valueTwo)
        self.assertEqual(valueOne, self.valuesReceived[0], "valueOne not as expected")
        self.assertEqual(valueTwo, self.valuesReceived[1], "valueTwo not as expected")

    def test_incorrect_value_raises_ValueError(self):
        self.signal.add(self.listener)
        self.assertRaises(ValueError, self.signal.dispatch, 45)

    def listener(self, first):
        self.valuesReceived.append(first)

