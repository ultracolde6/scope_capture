import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
from PyTektronixScope import TektronixScope
import pandas as pd
import sys
import time
import h5py



def read_data(channel):
    osc.write(f':DAT:SOU CH{channel}')
    osc.write(':DAT:ENC BIN')
    # osc.write(':DAT:WID 1')  # number of bytes per waveform data point
    # prev = time.time()
    # waveform_preample = osc.query(':WFMP?')
    # print(sys.getsizeof(waveform_preample))
    # print(time.time() - prev)
    # print(waveform_preample)
    # osc.write(':CURV?')    # acquire the data
    # prev = time.time()

    prev = time.time()
    osc.write(':CURV?')
    data_str = osc.read()
    print(sys.getsizeof(data_str))
    print(time.time() - prev)
    # data_str = data_str.split(',')
    # waveform_preample = waveform_preample.split(';')
    print(data_str)

    # y_off = float(waveform_preample[-2])
    # y_zero = float(waveform_preample[-3])
    # y_mult = float(waveform_preample[-4])
    #
    # x_incr = float(waveform_preample[-8])
    # x_zero = float(waveform_preample[-6])
    #
    #
    # data_lst = np.array([int(d) for d in data_str]) * y_mult

    # return data_lst, y_off, y_zero, x_incr, x_zero

    return data_str






if __name__ == '__main__':

    rm = visa.ResourceManager()
    instrument_resource_name = rm.list_resources()[0]
    print(instrument_resource_name)
    osc = rm.open_resource(instrument_resource_name)
    # osc.write(':DATALOG:DURA ')
    osc.write(':DATALOG:STATE OFF')
    osc.write(':TRIG FORC')

    osc.read_raw()


"""
    osc.write(':ACQ:STATE RUN')
    osc.write(':ACQ:MOD SAM')
    osc.write(':ACQ:STOPA SEQ')
 
    while True:
        trigger_status = osc.query(':TRIG:STATE?')
        if trigger_status == 'SAVE\n':
            # osc.write(':ACQ:STATE STOP')
            prev = time.time()
            data_lst, y_off, y_zero, x_incr, x_zero = read_data(1)
            print(time.time() - prev)
            print(len(data_lst))

            plt.plot(data_lst)
            plt.show()
            print(y_off)
            osc.write(':ACQ:STATE RUN')    # needed because else no new data will be saved
            osc.write(':ACQ:MOD SAM')
            osc.write(':ACQ:STOPA SEQ')    # stop after a single trigger if acquisition mode is in sample
        time.sleep(1)
"""

    #
    # while True:
    #     osc.write(':TRIG:STATE?')
    #     trigger_status = osc.read()
    #     if trigger_status == 'STOP':
    #         print('hi')
    #     time.sleep(1)
    # data_lst = read_data()[0]
    # plt.plot(data_lst)
    # plt.show()



    # while True:
    #     trigger_status = osc.visa_ask(':TRIG:STAT?')
    #     if trigger_status == 'STOP':
    #
    #         # read the
    #         mem_depth = int(osc.visa_ask(':ACQ:MDEP?'))
    #         print(mem_depth)
    #         data_lst, t_increment, t_origin, t_reference = read_memory(mem_depth)
    #         # save_as_d5()
    #         plt.plot(data_lst)
    #         plt.show()
    #         osc.visa_write(':SING') # set trigger mode to single
    #     time.sleep(1)



