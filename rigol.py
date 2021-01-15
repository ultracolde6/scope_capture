import pyvisa as visa
import rigol1000z  # on website it's import Rigol1000z, this doesn't work"
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import warnings
import h5py
from pathlib import Path
import datetime
import pandas as pd


def read_screen():
    osc.visa_write(':WAV:SOUR CHAN1')
    osc.visa_write(':WAV:MODE NORM')
    osc.visa_write(':WAV:FORM ASC')
    data_str = osc.visa_ask(':WAV:DATA?')
    # data_str = osc.visa_read()
    header_len = 11
    data_str = data_str[header_len:].split(',')
    data_lst = np.array([float(d) for d in data_str])

    # unit is seconds, t_increment is timescale/100
    t_increment = osc.visa_ask(':WAV:XINC?')
    t_origin = osc.visa_ask(':WAV:XOR?')
    t_reference = osc.visa_ask(':WAV:XREF?')
    return data_lst, t_increment, t_origin, t_reference


# reading from all four channels take about 1.5s
def read_memory(mem_depth, channel):

    osc.visa_write(f':WAV:SOUR CHAN{channel}')
    osc.visa_write(':WAV:MODE RAW')
    osc.visa_write(':WAV:FORM ASC')
    osc.visa_write(':WAV:STAR 1')
    osc.visa_write(f':WAV:STOP {mem_depth}')    # set the number of data points to be read
    data_str = osc.visa_ask(':WAV:DATA?')    # takes about 0.35 s, runtime limited by this line
    header_len = 11
    data_str = data_str[header_len:].split(',')
    try:
        data_lst = np.array([float(d) for d in data_str])
    except ValueError:
        data_lst = []
    # print(f'data is {data_lst}')
    return data_lst


def save_as_h5(path, data_lst, t_increment, t_origin, data_read_time):


    hf = h5py.File(str(path), 'w')

    length = len(data_lst[0])
    t_lst = np.linspace(t_origin, (length-1)*t_increment, length)

    hf.create_dataset('time', data=t_lst)
    for idx, d_lst in enumerate(data_lst):
        hf.create_dataset(f'CH{idx+1}', data=d_lst)
    data_read_time_str = data_read_time.strftime('%Y-%m-%d %H:%M:%S %f')
    hf.attrs['timestamp'] = data_read_time_str
    hf.close()

def make_daily_data_path():
    today = datetime.datetime.today()
    year = f'{today.year:4d}'
    month = f'{today.month:02d}'
    day = f'{today.day:02d}'
    daily_data_path = Path(year, month, day, 'data')
    return daily_data_path




if __name__ == '__main__':

    root_path = Path('Y:/', 'smalldata-e6')
    scope_name = 'scope_00'
    run_name = 'test_run'
    data_folder_name = f'{scope_name}'


    rm = visa.ResourceManager()
    print(rm.list_resources())
    # change the index to connect to different devices
    osc_resource = rm.open_resource(rm.list_resources()[0])
    osc_resource.read_termination = '\n'
    osc = rigol1000z.Rigol1000z(osc_resource)
    print(osc.visa_ask('*IDN?'))




    # mem_depth = 120000

    time_scale = osc.visa_ask(':TIM:SCAL?')  # set the time scale
    time_offset = 6. * float(time_scale)  # move the trigger to the very left of the oscilloscope screen
    osc.visa_write(f':TIM:OFFS {time_offset}')

    osc.visa_write(':SING')  # set trigger mode to single and start the scope running
    for channel in [1,2,3,4]:
        osc.visa_write(f':CHAN{channel}:PROB 1')    # set the probe ratio of every channel to 1

    count = 0
    while True:
        prev = time.time()
        all_channel_data = []

        trigger_status = osc.visa_ask(':TRIG:STAT?')
        if trigger_status == 'STOP':
            mem_depth = osc.visa_ask(':ACQ:MDEP?')
            if mem_depth == 'AUTO' or int(mem_depth) > 30000:
                warnings.warn(
                    f"Mem Depth {mem_depth} maybe larger than the maximum allowed value for ASCII for 4 channels(30000), full screen may not be recorded.")

            for channel in [1, 2, 3, 4]:
                one_channel_data = read_memory(mem_depth, channel)
                all_channel_data.append(one_channel_data)
                # plt.plot(one_channel_data)
            data_read_time = datetime.datetime.now()
            # plt.show()

            t_increment = float(osc.visa_ask(':WAV:XINC?'))
            t_origin = float(osc.visa_ask(':WAV:XOR?'))
            t_reference = float(osc.visa_ask(':WAV:XREF?'))    # never used


            daily_data_path = make_daily_data_path()
            data_path = Path(root_path, daily_data_path, run_name, data_folder_name)
            h5_file_name = scope_name + f'_{count:05d}.h5'

            data_path.mkdir(parents=True, exist_ok=True)
            file_path = Path(data_path, h5_file_name)
            save_as_h5(file_path, all_channel_data, t_increment, t_origin, data_read_time)

            print(f"file saved at time : {datetime.datetime.today()}; count == {count}")
            count += 1
            # print(osc.visa_ask(':TRIG:STAT?'))
            osc.visa_write(':SING') # set trigger mode to single
            time.sleep(0.3)
            # print(osc.visa_ask(':TRIG:STAT?'))
        # print(time.time() - prev)
    # data_lst, t_increment, t_origin, t_reference = read_screen()
    # data_str2 = read_screen()[0]





    """ code for setting time scale and memory depth : 
    
    ### set time_scale and offset
    # time_scale ranges from 5ns to 50s in 1-2-5 step
    time_scale = 20e-3   # unit is second
    mem_depth = 120000    # must be in [12000, 120000]


    osc.visa_write(f':TIM:SCAL {time_scale}')    # set the time scale
    time_offset = 6 * time_scale    # move the trigger to the very left of the oscilloscope screen
    osc.visa_write(f':TIM:OFFS {time_offset}')
    osc.visa_write(f':ACQ:MDEP {mem_depth}')  # set the memory depth
    print('waiting......')
    time.sleep(10)  # wait until new data is stored in oscillosscope internal mem or when trigger is fired 
    data_str = read_memory(120000)[0]
    """




    # print(sys.getsizeof(data_lst[0]) * len(data_lst))




