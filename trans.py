import numpy as np
import math
import pyaudio
from subprocess import call
import wave

def char_2_bits(character):

	"""returns the binary values of a given char
	"""

	#bin returns a binary string where the first two digits label it as binary
	bits = bin(ord(character))[2:]

	#0s must be added to the start of bits if it is less than 8 characters (a byte)
	bits = '00000000'[len(bits):] + bits

	return map(int, bits)


def str_2_bits(string):

	"""returns the binary values of a given string
	"""
	bits = []

	for c in string:
		byte = char_2_bits(c)
		bits.extend(byte)
	return bits


def bits_2_wave(bits, Fs):

	"""converts a string of bits into a 440hz wave with a zero amplitude equating 
	to a '0' bit value and .25 amplitude equating to a '1' bit value. Each bit
	plays for a .1 second increment of time.
	"""

	wave = []
	#begin wave with a unique starter freq to signal the start of a transmission
	wave.append(sine(800, 1, Fs))

	for bit in bits:
		if bit == 0:
			wave.append(sine(640,.1,Fs))
		elif bit == 1:
			wave.append(sine(440,.1,Fs))

	wave.append(sine(800, 1, Fs))
	wave = np.concatenate(wave)*0.25

	return wave

def sine(frequency, length, rate):
	"""creates a sine wave with a specified freq, length, and sampling rate
	"""
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return np.sin(np.arange(length) * factor)

def play_wave(samples, Fs, volume = 1):
	"""takes a wave in list form and converts into a sound file by writing it 
	to a PyAudio object
	"""
	p = pyaudio.PyAudio()

	stream = p.open(format=pyaudio.paFloat32,
	                channels=1,
	                rate=Fs,
	                output=True)
	stream.write(samples.astype(np.float32))

	stream.close()

	p.terminate()

	# stream.write(samples.astype(np.float32).tostring())

	wf = wave.open('test.wav', 'wb')
	wf.setnchannels(1)
	wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
	wf.setframerate(Fs)
	wf.writeframes(b''.join(samples.astype(np.float32).tostring()))
	wf.close()



def run_transmitter(input_string,Fs): 	

	"""turns on JACK port and creates and plays a wave based 
	upon an input string 
	"""

	call(["sudo", "jack_control", "start"])
	print str_2_bits(input_string)
	output_wave = bits_2_wave(str_2_bits(input_string),Fs)


	play_wave(output_wave,Fs)


run_transmitter("mica is super cool, JK",44100)