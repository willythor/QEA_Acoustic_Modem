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




def freq_listener(duration):
	"""opens the wav file saved in get_audio() and searches it for a binary signal
	"""
	# try:
	binary_vals = []

	real_binary_vals = [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1]


	#creates and saves an audio recording 
	get_audio(25)

	#reads said audio file
	fs, data = wavfile.read('test2.wav') 
	
	a = data

	yo = 0

	#how is this normalization? 
	b = [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
	
	listening = False	
	starter_ender_freq_found = False
	binary_vals = []

	for i in range(177):
	
		# if listening:
		# 	# section = b[int(i * 4400) : int((i +1) * 4400)]
		# else:

		section = b[int(i * 4400/10) : int((i + 1) * 4400/10)]

		sect_fft = fft(section) # calculate fourier transform (complex numbers list)
	
		maxPosition = np.argmax(abs(sect_fft[:])) 

		freq = maxPosition*100
		
		if freq > 750:
			binary_section = b[int(i * 4400/10) + 44000:]
			break

			


	for m in range(200):

 		section = binary_section[int(m * 4400) : int((m +1) * 4400)]

 		sect_fft = fft(section) # calculate fourier transform (complex numbers list)
	
		maxPosition = np.argmax(abs(sect_fft[:])) 

		freq = maxPosition*10

		print freq
		
		if freq > 550 and freq < 750:
			binary_vals.append(0)
		elif freq > 350 and freq < 450:
			binary_vals.append(1)
		elif freq > 750:
			break
			


		
	
		
	
	return binary_vals
		

   

binary_list = freq_listener(22)  
print len(binary_list)
binary_list = ''.join(str(e) for e in binary_list)


print ' '.join([binary_list[i:i+8] for i in range(0, len(binary_list), 8)])
