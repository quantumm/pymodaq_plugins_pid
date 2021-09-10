from time import perf_counter
from PyQt5.QtCore import QObject
from numpy.random import random

class BoilerController(QObject):
    _current_temperature = 20.
    _current_power = 0.
    _ellapsed_time = 0.

    _noise = 0.1

    def __init__(self, ):
        super().__init__()
        self.startTimer(10)


    def timerEvent(self, event):
        dt = perf_counter() - self._ellapsed_time
        self._ellapsed_time += dt

        self._current_temperature += 1 * self._current_power * dt + self._noise * (random() - 0.5)
        # some heat dissipation
        self._current_temperature -= 0.2 * dt

    def check_position(self):
        return self._current_power

    def move_abs(self, value):
        self._current_power = value


    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, noise):
        self._noise = noise

    def move_rel(self, value):
        self._current_power += value

    def grab(self):
        return self._current_temperature
