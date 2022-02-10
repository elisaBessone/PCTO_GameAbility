"""
read muse data
PCTO project of ITIS MARIO DELPOZZO CUNEO
"""

import numpy as np 
from pylsl import StreamInlet, resolve_byprop
import utils
import threading, queue
import time
from muselsl import stream, list_muses, view

#muselsl stream --ppg --acc --gyro

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

""" EXPERIMENTAL PARAMETERS """
BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = [0]

if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search and active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    #print(streams)
        
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()
    info = inlet.info()
    description = info.desc()
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
    band_buffer = np.zeros((n_win_test, 4))
        
    """ 3. GET DATA """
    try:
        while True:
                
            """prova per concentrazione"""
            #band_beta = 'STOP'
                
            #time.sleep(5)
            def muse(): #crea un thread che gestisce una coda, prendendo 5 valori di concentrazione, in base ad essi fa una media e percepisce se la persone è concentrata o meno
                eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
                filter_state = None  # for use with the notch filter
                q = queue.Queue()
                cnt = 0
                c = 0 
                command = 'ESCI'
                while (cnt < 5):
                    """ 3.1 ACQUIRE DATA """
                    eeg_data, timestamp = inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
                    ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
                    eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

                    """ 3.2 COMPUTE BAND POWERS """
                    data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
                    band_powers = utils.compute_band_powers(data_epoch, fs)
                    #print (band_powers)
                    band_beta = utils.compute_beta(data_epoch, fs)
                        
                    if(band_beta == 'W'):
                        c += 1
                    
                    q.put(band_beta) #mette il dato nella coda
                    cnt += 1
                    time.sleep(0.5)
                    
                if(c >= 3): #se in un campione di 5 dati la maggiorparte è W (concentrazione) restituisce come comando W (avanti)
                    command = 'W'
                    print(command)
                else:
                    command = 'ESCI' #altrimenti sta fermo (ESCI)
                    print(command)
                    
                time.sleep(1)    
                c = 0
                        
                def worker():
                    while True:
                        band_beta = q.get() #toglie gli elementi dalla coda
                        q.task_done()

                # turn-on the worker thread
                        
                threading.Thread(target=worker, daemon=True).start() #creazione del thread
                time.sleep(5)
                cnt = 0 
                    
                #print(f'Working on {item}')
                #print(f'Finished {item}')
                #print('All task requests sent\n', end='')

                # block until all tasks are done
                q.join()
                #print('All work completed')
                
                return command #ritorna il comando da fornire all'alphabot
            muse()

    #CTRL+C per stoppare
    except KeyboardInterrupt:
        print('Closing!')

