import pyaudio 
import wave
import numpy as np
from subprocess import call
import matplotlib.pyplot as plt
from scipy.fftpack import fft, rfft
from scipy.io import wavfile # get the api
from time import sleep
import timeit

def get_audio(RECORD_SECONDS):
	"""records a segment of audio for a specified amount of time
	"""

	CHUNK = 1000
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44000
	WAVE_OUTPUT_FILENAME = "test2.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	listening = True


	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()



def binary_conversion(binary_list):
	"""
	converts a list of binary vals to a str
	"""

	print binary_list

	asci = np.packbits(binary_list)

	char_vals = ''.join(map(chr,asci))

	return char_vals


def freq_listener(duration):
	"""opens the wav file saved in get_audio() and searches it for a binary signal
	"""

	binary_vals = []

	#used to check agains the demodulated binary vals
	real_binary_vals = [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]


	#creates and saves an audio recording 
	# get_audio(20)

	#reads said audio file
	fs, data = wavfile.read('this_works.wav') 



	print 'data', data
	
	a = data

	yo = 0

	#how is this normalization? 
	b = [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)

	binary_vals = []

	plt.plot(b,'r') 
	plt.show()

	for i in range(6000):
	

		section = b[int(i * 4400/10) : int((i + 1) * 4400/10)]

		sect_fft = (fft((section))) # calculate fourier transform (complex numbers list)
		
		maxPosition = np.argmax(abs(sect_fft[:])) 

		freq = maxPosition*100
		print freq
		if freq > 750 and freq < 850 and np.amax(abs(sect_fft[:])) > 100:
		
			binary_section = b[int(i * 4400/10) + int(44000*1):]
			print 'we found the starter freq'
			break

		
	fft_avg = []	

	for n in range(8,15):

 		section = binary_section[int(n * 4400) : int((n +1) * 4400)]	

 		sect_fft = fft(section) # calculate fourier transform (complex numbers list)

		max_y_val = np.amax(abs(sect_fft[:]))	

		fft_avg.append(max_y_val)


	print fft_avg
	fft_thresh = ((np.amin(fft_avg) + np.amax(fft_avg)))/2

	z = 0

	for m in range(2000):
		print 'this is m: ' + str(m)

		print 'this is thresh' + str(fft_thresh)


 		section = binary_section[int(m * 4400) : int((m +1) * 4400)]

 		sect_fft = fft(section) # calculate fourier transform (complex numbers list)
	
		maxPosition = np.argmax(abs(sect_fft[:])) 

		# plt.plot(abs(sect_fft[:1000]),'r') 
		# plt.show()

		freq = maxPosition*10
		print 'commencing binary analysis'
		print m
		print z
		print freq

		if freq > 750 and m != 0:
			plt.plot(abs(sect_fft[:1000]),'r') 
			plt.show()
			break
		elif freq > 750 and m == 0:
			z = z + 1
			continue
		
		if freq > 550 and freq < 750:
			if np.amax(abs(sect_fft[:])) < fft_thresh:
										
										   
				binary_vals.append(0)

			else:
				binary_vals.append(1)
		else:
			binary_vals.append(0)
								
		# print real_binary_vals[m-z]
		# print m-z

		# # print binary_vals
		# if real_binary_vals[m-z] != binary_vals[m-z]:
		# 	yo = yo + 1
		# 	print 'YOOOO!'
		# 	print real_binary_vals[m-z]
		# 	print np.amax(abs(sect_fft[:]))
		# 	plt.plot(abs(sect_fft[:1000]),'r') 
		# 	plt.show()
		# else:
		# 	print 'weee goood'
		# 	print np.amax(abs(sect_fft[:]))
		# 	print binary_vals[m-z]

	return binary_conversion(binary_vals)
		

print freq_listener(22)  
