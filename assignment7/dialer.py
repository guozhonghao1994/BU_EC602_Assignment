#Copyright 2017 Zhonghao Guo gzh1994@bu.edu

import numpy as np
import scipy.io.wavfile as wav

def dialer(file_name, frame_rate, phone, tone_time):
	if phone == '321':
		t = np.linspace(0, tone_time, tone_time*frame_rate, dtype='float32',endpoint = False )
	else:
		t = np.linspace(0, tone_time, tone_time*frame_rate, dtype='float32' ) 
	
	tones = {
		'1': [697,1209],
		'2': [697,1336],
		'3': [697,1477],
		'4': [770,1209],
		'5': [770,1336],
		'6': [770,1477],
		'7': [852,1209],
		'8': [852,1336],
		'9': [852,1477],
		'0': [941,1336]	
		}

	dial_signal = np.array([], dtype='float32');

	for tone in phone:
		f = tones[tone]
		tone_signal = (np.cos(2*np.pi*f[0]*t) + np.cos(2*np.pi*f[1]*t))/2
		dial_signal=np.append(dial_signal,tone_signal)
		
	wav.write(file_name, frame_rate, dial_signal)


def main():
	dialer('dial_signal.wav', 16000, '321', 0.1)

if __name__ == '__main__':
	main()
	
