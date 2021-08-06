import numpy as np
import matplotlib.pyplot as plt


def sine_wave(f):
    """ Generate sine wave signal with the following parameters
    Parameters:
        f : frequency of sine wave in Hertz
    Returns:
        (t,x) : time base (t) and the signal x(t) as tuple
    """
    f_s = 1024  # Sampling rate, or number of measurements per second

    t = np.linspace(0, 2, f_s)
    x = np.sin(f * np.pi * t)
    return t, x  # return time base and signal g(t) as tuple


if __name__ == '__main__':
    data = np.zeros((1024, 4))
    ts = []
    for i in range(4):
        t, sine = sine_wave(i+1)
        ts.append(t)
        sine = np.array(sine).T
        data[:, i] = sine

    freqs = np.fft.fftfreq(len(data[:, 0])) * 1024
    for channel in data.T:
        X = np.fft.fft(channel)

        fig, ax = plt.subplots()

        ax.stem(freqs, np.abs(X))
        ax.set_xlabel('Frequency in Hertz [Hz]')
        ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
        ax.set_xlim(-1024 / 2, 1024 / 2)
        ax.set_ylim(-5, 600)
        plt.show()
        print(np.argmax(np.abs(X)))
