import h5py
import pandas as pd
import matplotlib.pyplot as plt


filename = "./that.h5"
with h5py.File(filename, "r") as f:
    # print(f"Keys : {f.keys()}")
    ch1 = list(f['CH1'])
    ch2 = list(f['CH2'])
    ch3 = list(f['CH3'])
    ch4 = list(f['CH4'])
    t_lst = list(f['time'])

# print(data)
plt.plot(t_lst, ch1)
plt.plot(t_lst, ch2)
plt.plot(t_lst, ch3)
plt.plot(t_lst, ch4)

plt.show()
print(len(ch1))
print(len(ch2))
print(len(ch3))
print(len(ch4))
print(len(t_lst))




