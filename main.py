import find_peaks

data, samplerate = find_peaks.read_file()
find_peaks.find_peaks(data, samplerate)