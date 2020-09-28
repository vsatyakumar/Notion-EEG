
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pylsl import StreamInlet, resolve_stream
import time
import json
import matplotlib.animation as animation


def show_stream(data_stream):
    fig, ax = plt.subplots(8, dpi=100)
    data_array = []
    time_array = []
    for d in data_stream:
        data_array.append(d['sample'])
        time_array.append(d['timestamp'])

    data_array = np.array(data_array)
    for i in range(8):
        ax[i].plot(time_array, np.array(data_array[:, i]))
        ax[i].set(xlabel="Electrode -" + str(i), ylabel="Signal")
    plt.show()
    return

data_stream = []
try:
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    start = None
    stop = None
    while True:
        if not start:
            start = time.time()
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)
        data_stream.append({"timestamp":timestamp,
                            "sample":sample})

except KeyboardInterrupt as e:
    print("Ending program")
    if len(data_stream) > 0:
        stop = time.time()
        #fig, ax = plt.subplots(8, dpi=100)
        #show_stream(data_stream)

        print('saving data')
        filename = 'data' + '_S_' + str(start).split('.')[0] + '_E_' + str(stop).split('.')[0] + '.json'
        with open(filename, 'w') as f:
            json.dump(data_stream, f)
    raise e

