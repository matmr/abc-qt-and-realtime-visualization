import sys

import pyaudio

import numpy as np

import scipy.signal as sig

from PyQt5 import QtCore, QtWidgets

import pyqtgraph as pg


_SAMPLING_RATE = 22050
_WINDOW_SIZE = 3*44100
_CHUNK_SIZE = 1000


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        graphics = pg.PlotWidget()
        self.plot = graphics.plot()
        
        self.layout.addWidget(graphics)
        
        self.sound_source = SoundTimeSeries()

        self.show_sound()

    def show_sound(self):
        """..."""
        def update_plot():
            data = self.sound_source.buffer
            time = np.arange(data.size) / _SAMPLING_RATE
            
            self.plot.setData(time, data)


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(update_plot)
        self.timer.start(80)
    

class SoundTimeSeries(pyaudio.PyAudio):
    """Acquires sound through the microphone and feeds
    it."""

    def __init__(self):
        super().__init__()

        def callback(in_data, frame_count, time_info, status):
            
            data = np.fromstring(in_data, np.float32)
            self.write_buffer(data)

            return (None, pyaudio.paContinue)

        self.stream = self.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=_SAMPLING_RATE,
            output=False,
            input=True,
            frames_per_buffer=_CHUNK_SIZE,
            stream_callback=callback
        )

        self.buffer = np.zeros(_WINDOW_SIZE)
        self.buffer_p = np.zeros(_WINDOW_SIZE)

    def write_buffer(self, data):
        self.buffer = np.roll(self.buffer, _CHUNK_SIZE)
        self.buffer[:_CHUNK_SIZE] = data

        chunk = self.buffer[:10*_CHUNK_SIZE]

    def stop(self):
        """Stop recording."""
        self.stream.stop_stream()
        self.stream.close()

        self.terminate()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())