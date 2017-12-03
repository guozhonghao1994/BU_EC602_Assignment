#Copyright 2017 Zhonghao Guo gzh1994@bu.edu
#Copyright 2017 Muzi Li marlonli@bu.edu
#Copyright 2017 Runzhou Han rzhan@bu.edu

import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import numpy as np

def loudest_band(music,frame_rate,bandwidth):
	f_r = frame_rate
	N = len(music)
	f = np.arange(-f_r/2, f_r/2, f_r/N) 
	f_0_index = np.absolute(f).argmin()
	fft = np.fft.fftshift(np.fft.fft(music))
	fft_power = np.square(np.absolute(fft))
	
	window_width = int(bandwidth/(f_r/N))
	max_sum = 0
	max_sum_i = 0
	
	tmp_sum = np.sum(fft_power[f_0_index-1:f_0_index+window_width])

	for i in range(f_0_index, N-window_width): 
		tmp_sum = tmp_sum - fft_power[i-1] + fft_power[i+window_width-1]
		if tmp_sum > max_sum:
			max_sum = tmp_sum
			max_sum_i = i

	low_Hz  = (max_sum_i-f_0_index)*f_r/N
	high_Hz = (max_sum_i-f_0_index+window_width)*f_r/N
		
	H = np.zeros(N)
	for i in range(max_sum_i,max_sum_i+window_width+1):
		H[i] = 1
	for i in range(2*f_0_index-max_sum_i-window_width,2*f_0_index-max_sum_i+1):
		H[i] = 1
	
	fft_filtered = fft*H
	loudest = np.real(np.fft.ifft(np.fft.ifftshift(fft_filtered)))

	return (low_Hz, high_Hz, loudest)


def read_wave(filename,debug=False):
	frame_rate,music = wavfile.read(filename)
	if music.ndim>1:
		nframes,nchannels = music.shape
	else:
		nchannels = 1
		nframes = music.shape[0]
	if debug:
		print(frame_rate,type(music),music.shape,nframes)
	return music,frame_rate,nframes,nchannels

def plot_fft(tone, f_r, fmin, fmax):
	fft = np.fft.fft(tone)
	N = len(tone)
	f = np.arange(-f_r/2, f_r/2, f_r/N)
	
	plt.plot(f,np.fft.fftshift(np.absolute(fft)))
	ax = plt.subplot(111)
	ax.set_xlim(xmin=fmin, xmax=fmax)
	plt.xlabel('Frequency, Hz')
	plt.ylabel('|X|')
	plt.show()

def main():
	filename = ''	
	music, frame_rate, nframes, nchannels = read_wave(filename, False)
	(low, high, loudest) = loudest_band(music[:,0], frame_rate, 75)

	print("low:  ", low,  " Hz")
	print("high: ", high, " Hz")	
	
	loudest = loudest/np.max(loudest) 
	loudest = loudest.astype(np.float32) 
	wavfile.write('filtered.wav', frame_rate, loudest)
	
if __name__ == '__main__':
	main()
