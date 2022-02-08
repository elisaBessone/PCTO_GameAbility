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
def muse():
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
        """muses = list_muses()
        print(muses)
        stream(muses[0]['address'], ppg_enabled=True, acc_enabled=True, gyro_enabled=True)
        print(streams)"""
        
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')
        print("Start acquiring data")
        inlet = StreamInlet(streams[0], max_chunklen=12)
        eeg_time_correction = inlet.time_correction()
        info = inlet.info()
        description = info.desc()
        fs = int(info.nominal_srate())

        """ 2. INITIALIZE BUFFERS """
        eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
        filter_state = None  # for use with the notch filter
        n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
        band_buffer = np.zeros((n_win_test, 4))
        
        """ 3. GET DATA """
        q = queue.Queue()
        cnt = 0
        c = 0 
        command = 'ESCI'
        try:
            while True:
                
                """prova per concentrazione"""
                #band_beta = 'STOP'
                
                #time.sleep(5)
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
                
                    q.put(band_beta)
                    cnt += 1
                    time.sleep(0.5)
                
                if(c >= 3):
                    command = 'W'
                    print(command)
                else:
                    command = 'ESCI'
                    print(command)
                
                time.sleep(1)    
                c = 0
                       
                def worker():
                    while True:
                        band_beta = q.get()
                        q.task_done()

                # turn-on the worker thread
                    
                threading.Thread(target=worker, daemon=True).start()
                time.sleep(5)
                cnt = 0 
                #cnt -= 1
                
                #print(f'Working on {item}')
                #print(f'Finished {item}')
                #print('All task requests sent\n', end='')

                # block until all tasks are done
                q.join()
                #print('All work completed')
                
                #band_beta = utils.compute_beta(data_epoch, fs)
                #print(band_beta)
                
                #band_alpha = utils.compute_alpha(data_epoch, fs)

        except KeyboardInterrupt:
            print('Closing!')
    return command #band_beta in una media di 5
muse()
