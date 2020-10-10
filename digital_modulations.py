import matplotlib.pyplot as plot
import numpy as np
import sys

class BaseClass:
	def __init__(self, file="image", freq=10):
		self.file = file
		self.m = 0.2
		self.freq = freq
		self.freqs = 2

		self.Fs = 150.0  # sampling rate
		self.Ts = 1.0/self.Fs # sampling interval
		self.t = np.arange(0, 2, self.Ts)
	
	def calculate_signal_properties(self, y):
		self.n = len(y) # length of the signal
		self.k = np.arange(self.n)
		self.T = self.n/self.Fs
		self.frq = self.k/self.T # two sides frequency range
		self.frq = self.frq[range(self.n//2)] # one side frequency range
		self.Y = np.fft.fft(y)/self.n # fft computing and normalization
		self.Y = self.Y[range(self.n//2)]
	
	def plot(self, y):
		fig, myplot = plot.subplots(2, 1)
		myplot[0].plot(self.t, y)
		myplot[0].set_xlabel('Time')
		myplot[0].set_ylabel('Amplitude')

		myplot[1].plot(self.frq, abs(self.Y),'r') # plotting the spectrum
		myplot[1].set_xlabel('Freq (Hz)')
		myplot[1].set_ylabel('|Y(freq)|')
		plot.savefig(self.file)
		plot.show()


class Ask(BaseClass):
	def __init__(self):
		super().__init__("ask")
		self.bit_arr = np.array([1, 0, 1, 1, 0]) # <- Input bit rate (original)
		#bit_arr = np.array([0, 0, 1, 0, 0]) # <- Input bit rate
		self.samples_per_bit = 2*self.Fs/self.bit_arr.size 
		self.dd = np.repeat(self.bit_arr, self.samples_per_bit)
		self.y = self.dd*np.sin(2 * np.pi * self.freq * self.t)
		super().calculate_signal_properties(self.y)
		super().plot(self.y)


class Fsk(BaseClass):
	def __init__(self):
		super().__init__("fsk")	
		self.bit_arr = np.array([3,2,7,5,-5])
		self.samples_per_bit = 2*self.Fs/self.bit_arr.size 
		self.dd = np.repeat(self.bit_arr, self.samples_per_bit)
		self.y = np.sin(2 * np.pi * (self.freq + self.dd) * self.t)
		super().calculate_signal_properties(self.y)
		super().plot(self.y)


class Psk(BaseClass):
	def __init__(self):
		super().__init__("psk")	
		self.bit_arr = np.array([180,180,0,180,0])
		self.samples_per_bit = 2*self.Fs/self.bit_arr.size 
		self.dd = np.repeat(self.bit_arr, self.samples_per_bit)
		self.y = np.sin(2 * np.pi * (self.freq) * self.t+(np.pi*self.dd/180))
		super().calculate_signal_properties(self.y)
		super().plot(self.y)
	

if __name__ == "__main__":
	print("\nWORKING...")
	if (len(sys.argv)>1):
		type=(sys.argv[1].lower())
		if type in ["ask", "fsk", "psk"]:
			if type == "ask":
				A = Ask()
			elif type == "fsk":
				F = Fsk()
			else:
				P = Psk()			
		else:
			print("We currently do not supprt that modulation")

		# WIP:
		#if (len(sys.argv)>2):
		#	freq=int(sys.argv[3])
		#if (len(sys.argv)>3):
		#	file=str(sys.argv[1])
	else:
		print("You need to pass the modulation type as the first argument [ask|fsk|psk|qam]")	
	print("...DONE")
