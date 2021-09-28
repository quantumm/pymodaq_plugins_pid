import numpy as np
from pymodaq.daq_utils.daq_utils import gauss2D

class BeamSteeringController:

    Nactuators = 2
    axis = ['H', 'V']
    Nx = 256
    Ny = 256
    offset_x = 128
    offset_y = 128
    coeff = 0.01
    drift = False

    def __init__(self, positions=None, wh=(40, 50), noise=0.1, amp=10):
        super().__init__()
        if positions is None:
            self.current_positions = dict(zip(self.axis, [0. for ind in range(self.Nactuators)]))
        else:
            assert isinstance(positions, list)
            assert len(positions) == self.Nactuators
            self.current_positions = positions

        self.amp = amp
        self.noise = noise
        self.wh = wh
        self.data_mock = None

    def check_position(self, axis):
        return self.current_positions[axis]

    def move_abs(self, position, axis):
        self.current_positions[axis] = position

    def move_rel(self, position, axis):
        self.current_positions[axis] += position


    def get_xaxis(self):
        return np.linspace(0, self.Nx, self.Nx, endpoint=False)

    def get_yaxis(self):
        return np.linspace(0, self.Ny, self.Ny, endpoint=False)

    def set_Mock_data(self):
        """
        """
        x_axis = self.get_xaxis()
        y_axis = self.get_yaxis()
        if self.drift:
            self.offset_x += 0.1
            self.offset_y += 0.05
        self.data_mock = self.gauss2D(x_axis, y_axis,
                                 self.offset_x + self.coeff * self.current_positions['H'],
                                 self.offset_y + self.coeff * self.current_positions['V'])
        return self.data_mock

    def gauss2D(self, x, y, x0, y0):
        Nx = len(x) if hasattr(x, '__len__') else 1
        Ny = len(x) if hasattr(y, '__len__') else 1
        data = self.amp * gauss2D(x, x0, self.wh[0], y, y0, self.wh[1], 1) + self.noise * np.random.rand(Nx, Ny)

        return np.squeeze(data)

    def get_data_output(self):
        if self.data_mock is None:
            self.set_Mock_data()
        return self.data_mock[128, 128]

