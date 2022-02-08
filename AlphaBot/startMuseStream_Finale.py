"""
Starting a Stream

This example shows how to search for available Muses and
create a new stream
"""
from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_byprop
import utils
import time
import numpy as np

if __name__ == "__main__":
    
    BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
    EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
    OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
    INDEX_CHANNEL = [0]

    stream("00:55:da:b5:49:3e", ppg_enabled=True, acc_enabled=True, gyro_enabled=True)
    #print(stream("00:55:da:b5:49:3e"))
    streams_Gyro = resolve_byprop('type', 'Gyroscope', timeout=2)
    #creare un'altra stream per EEG
    streams_EEG = resolve_byprop('type', 'EEG', timeout=2)
    #print(streams_Gyro)
    #print(streams_EEG)
    #secondo inlet per EEG
    inlet_Gyro = StreamInlet(streams_Gyro[0], max_chunklen=12)
    info_Gyro = inlet_Gyro.info()
    #print(info.desc())
    
    inlet_EEG = StreamInlet(streams_EEG[0], max_chunklen=12)
    info_EEG  = inlet_EEG.info()  
    
    fs_Gyro = int(info_Gyro.nominal_srate())
    #fs2 per EEG
    fs_EEG = int(info_EEG.nominal_srate())
    #print(fs)
    
    
    
    while True:
            def museDxSx():
                """ 3.1 ACQUIRE DATA """
                # Obtain EEG data from the LSL stream
                gyro_data, timestamp = inlet_Gyro.pull_chunk(
                    timeout=1, max_samples=int(SHIFT_LENGTH * fs_Gyro))
                #print(eeg_data[-1])
                Theta = 0.5*(gyro_data[-1][2] + gyro_data[-2][2]) * 1/fs_Gyro #velocita in questo istante
                if(Theta > 0.1):
                    comando = 'A'
                    print(comando)
                elif(Theta < -0.1):
                    comando = 'D'
                    print(comando)
                else:
                    comando = 'W'
                    print(comando)
                    
                #print(Theta)
                #print(timestamp)
                return comando
            
            print("----------------------------------------------------------------")
            museDxSx();
            
            def museConcentrazione():
                eeg_buffer = np.zeros((int(fs_EEG * BUFFER_LENGTH), 1))
                filter_state = None  # for use with the notch filter
                EEG_data, timestamp = inlet_EEG.pull_chunk(
                    timeout=1, max_samples=int(SHIFT_LENGTH * fs_EEG))
                ch_data = np.array(EEG_data)[:, INDEX_CHANNEL]
                eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

                """ 3.2 COMPUTE BAND POWERS """
                data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs_EEG)
                band_powers = utils.compute_band_powers(data_epoch, fs_EEG)
                #print (band_powers)
                band_beta = utils.compute_beta(data_epoch, fs_EEG)
                
                #print(EEG_data[-1])
                #Beta = 0.5*(EEG_data[-1][2] + EEG_data[-2][2]) * 1/fs_EEG #velocita in questo istante
                #print(Beta)
                #time.sleep(1)
                """if(Beta > 8):
                    print('concentrato')
                else:
                    print('non concentrato')"""
                return band_beta
                
            museConcentrazione()
    
    """if not muses:
        print('No Muses found')
    else:
        stream("00:55:da:b5:49:3e", ppg_enabled=True, acc_enabled=True, gyro_enabled=True)"""

        # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
    print('Stream has ended')
