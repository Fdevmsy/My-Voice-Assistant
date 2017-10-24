import pyaudio
import wave

class myRecord(object):
	def __init__(self):
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 16000
		self.CHUNK = 1024
		self.RECORD_SECONDS = 5
		self.WAVE_OUTPUT_FILENAME = "file.wav"
		 
		self.audio = pyaudio.PyAudio()
	 
	# start Recording
	def record(self):

		stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
		                rate=self.RATE, input=True,
		                frames_per_buffer=self.CHUNK)
		print "recording..."
		frames = []
		 
		for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
		    data = stream.read(self.CHUNK)
		    frames.append(data)
		print "finished recording"
		 
		 
		# stop Recording
		stream.stop_stream()
		stream.close()
		self.audio.terminate()
		 
		waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
		waveFile.setnchannels(self.CHANNELS)
		waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
		waveFile.setframerate(self.RATE)
		waveFile.writeframes(b''.join(frames))
		waveFile.close()