import pandas as pd
from datetime import datetime
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import h5py

def send_ecg(filename):
    bpm = 0
    on_spike = False
    last_spike_date = None
    last_spike_delta = None
    matrix = []

    try:
        df = pd.read_hdf(filename, 'raw')
    except:
        print('key not found')
        return 0

    for column in df:
        serie = df[column]

    duration = 1000 if len(serie) > 1000 else len(serie)

    if duration == 1000:
        max_spike = min(max(serie.iloc[-duration : int(- 3 * duration / 4)]), 
            max(serie.iloc[int(- 3 * duration / 4) : int(- 2 * duration / 4)]),
            max(serie.iloc[int(- 2 * duration / 4) : int(- 1 * duration / 4)]),
            max(serie.iloc[int(- 1 * duration / 4) : -1]))
    else:
        max_spike = max(serie.iloc[-duration : -1])

    print(max_spike)
    for index, seq in enumerate(serie.iloc[-duration:-1]):
        if not on_spike and seq > 0.7 * max_spike:
            bpm += 1
            on_spike = True
            if last_spike_date:
                last_spike_delta = serie.keys()[index] - last_spike_date
            last_spike_date = serie.keys()[index]
        if on_spike and seq < 0.7 * max_spike:
            on_spike = False
        matrix.append(seq)

    # print ecg
    # xaxis = np.array(matrix)
    # plt.plot(xaxis)
    # plt.show()

    return bpm * 6000 / duration, 60 / last_spike_delta.total_seconds()


def send_eeg(filename):
    try:
        df = pd.read_hdf(filename, 'raw')
    except:
        print('key not found')
        return 0
    for column in df:
        serie = df[column]
        print(df[column])
    
    duration = 1000 if len(serie) > 1000 else len(serie)
    duration = len(serie)
    matrix = []
    for index, seq in enumerate(serie.iloc[-duration:-1]):
        matrix.append([seq])

    xaxis = np.array(matrix)

    plt.plot(xaxis)
    plt.show()


def eeg_label(filename):
    try:
        events = pd.read_hdf(filename, 'events')
        df = pd.read_hdf(filename, 'raw')
    except:
        print('key not found')
        return 0

    for column in df:
        df_serie = df[column]
    
    for column in events:
        events_serie = events[column]

    events_date = []
    for i in range(len(events_serie)):
        events_date.append(events_serie.keys()[i])

    event_index  = 0
    df_events = []
    for index, seq in enumerate(df_serie):
        if event_index < len(events_date) and df_serie.keys()[index] > events_date[event_index]:
            start = index - 100 if index - 100 > 0 else 0
            df_events.append(df_serie.iloc[start:index+150])
            event_index += 1

            # print events
            matrix = []
            for event_seq in df_serie.iloc[start:index+150]:
                matrix.append([event_seq])
            xaxis = np.array(matrix)
            plt.plot(xaxis)
            plt.show()

    print(len(df_events))
    # hf = h5py.File('none_label.hdf5', 'w')
    # for index, data in enumerate(df_events):
    #     hf.create_dataset(f'right{index}', data=data)
    # hf.close()
    # return df_events

def read_hdf5(filename):
    # f = h5py.File(filename, 'r')
    # for key in f.keys():
    #     print(key)
    #     for column in f[key]:
    #         print(column)

    try:
        events = pd.read_hdf(filename, 'events')
        df = pd.read_hdf(filename, 'raw')
    except:
        print('key not found')
        return 0

    print(df)
    # for column in df:
    #     df_serie = df[column]
    
    # for index, seq in enumerate(df_serie):
    #     print(df_serie.keys()[index])

if __name__ == '__main__':
    ecg_filename = 'ecg.hdf5'
    eeg_filename = 'eeg.hdf5'
    eeg_label_right = 'right.hdf5'
    eeg_label_left = 'left.hdf5'
    eeg_label_none = 'none.hdf5'
    # print(send_ecg(ecg_filename))
    # send_eeg(eeg_filename)
    # test = eeg_label(eeg_label_left)
    # print(test)
    read_hdf5('left.hdf5')
