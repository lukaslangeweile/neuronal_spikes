import numpy
import numpy as np
import os
import pathlib
import pandas as pd
import math
import pickle
import matplotlib.pyplot as plt

DIR = pathlib.Path(os.curdir)


def save_peak(peak_id, array_id, peak_nr, sample, time, baseline, abs_amplitude, rel_amplitude, fwhm):
    filepath = DIR / "data" / "peak_results.csv"

    # Ensure the directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Prepare the new row as a DataFrame
    new_row = pd.DataFrame([{
        "peak_id": peak_id,
        "array_id": array_id,
        "peak_nr": peak_nr,
        "sample": sample,
        "time": time,
        "baseline": baseline,
        "abs_amplitude": abs_amplitude,
        "rel_amplitude": rel_amplitude,
        "fwhm": fwhm
    }])

    # Append to the file, writing headers only if the file does not exist
    new_row.to_csv(filepath, mode='a', header=not filepath.exists(), index=False)

def find_peaks(data, samplerate):
    # set filepath for result file
    filepath = DIR / "data" / "peak_results.csv"

    if filepath.exists() and filepath.is_file() and filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
        if not df.empty:
            peak_id = df["peak_id"].iloc[-1] + 1  # Use the last value in the column
            array_id = df["array_id"].iloc[-1] +1
        else:
            # When the DataFrame is empty
            peak_id = 0
            array_id = 0
    else:
        # When the file doesn't exist or isn't a CSV
        peak_id = 0
        array_id = 0

    data = np.array(data)
    print(data.shape)

    for col in range(data.shape[1]):
        column_data = data[:, col]  # extract data from columns

        # get baseline and standard deviation from every array (row)
        baseline = calculate_baseline(column_data)
        print(baseline)
        std = numpy.std(column_data)
        print(std)

        # set peak_nr zero at the beginning of every array check
        peak_nr = 0
        sample_list = []

        for index, sample in enumerate(column_data):
            if is_above_threshold(sample, baseline, std):

                sample_list.append(sample)

            elif is_above_threshold(column_data[index-1], baseline, std) and not is_above_threshold(sample, baseline, std)\
                    or is_above_threshold(column_data[index-1], baseline, std) and index == len(column_data)-1:
                peak_value = max(sample_list)
                peak_index = index - (len(sample_list) - sample_list.index(peak_value))

                # calculate time, amplitudes and fwhm
                time = peak_index / samplerate
                abs_amplitude = peak_value
                rel_amplitude = abs_amplitude - baseline
                fwhm = calculate_fwhm(peak_index, column_data, baseline)

                # save data in result file
                save_peak(peak_id, array_id, peak_nr, index, time, baseline, abs_amplitude, rel_amplitude, fwhm)

                peak_id += 1  # increase peak_id after every newly identified peak
                peak_nr += 1
                sample_list = []


        array_id += 1 # increase array_id after every completed array


def calculate_fwhm(peak_index, row, baseline):
    """
    Berechnet die Halbwertsbreite (FWHM) für einen gegebenen Peak.

    Parameter:
    - y: Array mit den y-Werten (die x-Werte ergeben sich durch den Index).

    Rückgabe:
    - fwhm_list: Liste mit den berechneten FWHM-Werten für jeden gefundenen Peak.
    - peaks: Indizes der Peaks im y-Array.
    """
    # Umwandlung von y in ein NumPy-Array, falls es eine Liste ist
    row = np.array(row)

    fwhm_list = []  # Speichert die FWHM-Werte

    rel_amplitude = row[peak_index] - baseline
    half_height = rel_amplitude / 2  # Halbe Höhe des aktuellen Peaks

    # Linke Grenze: Werte links vom Peak <= Halbwert
    left_indices = np.where((row[:peak_index] - baseline) <= half_height)[0]
    if len(left_indices) > 0:
        left_index = left_indices[-1]
    else:
        left_index = 0  # Falls kein Punkt gefunden wird, ist die Grenze der Start des Arrays.

    # Rechte Grenze: Werte rechts vom Peak <= Halbwert
    right_indices = np.where((row[peak_index:] - baseline) <= half_height)[0]
    if len(right_indices) > 0:
        right_index = right_indices[0] + peak_index
    else:
        right_index = len(row) - 1  # Falls kein Punkt gefunden wird, ist die Grenze das Ende des Arrays.

    # FWHM berechnen
    fwhm = right_index - left_index
    
    return fwhm

def read_file(file_name = "MembranePotential.pkl"):
    current_dir = pathlib.Path.cwd()
    file_path = next(current_dir.rglob(file_name))

    with open(file_path, 'rb') as fh:   # Daten aus der Pickle-Datei laden
        data, sampling_freq = pickle.load(fh)
    return data, sampling_freq


def is_above_threshold(sample, baseline, std):
    threshold = baseline + 3 * std
    if sample > threshold:
        return True
    else:
        return False


def calculate_baseline(numbers):
    if numbers is None:
        return None
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements in the list must be numbers.")

    return sum(numbers) / len(numbers)

  
def analyze_and_plot_peaks(data, sampling_freq, channel_index=0, peak_height=0, peak_distance=10):
    # Extract the specified channel and create a time vector
    membrane_potential = data[:, channel_index]
    time = np.arange(len(membrane_potential)) / sampling_freq
    
    # Detect peaks in the membrane potential
    peaks, properties = find_peaks(membrane_potential, height=peak_height, distance=peak_distance)
    
    # Isolate peaks
    peak_times = time[peaks]
    peak_values = membrane_potential[peaks]
    
    # Display results
    print("Detected Peaks:")
    print("Times (s):", peak_times)
    print("Values (mV):", peak_values)
    
    # Plot the data and peaks
    plt.figure(figsize=(12, 6))
    plt.plot(time, membrane_potential, label='Membrane Potential')
    plt.plot(peak_times, peak_values, 'rx', label='Peaks')  # Mark peaks with red 'x'
    plt.title(f'Membrane Potential (Channel {channel_index}) with Peaks')
    plt.xlabel('Time (s)')
    plt.ylabel('Membrane Potential (mV)')
    plt.legend()
    plt.grid()
    plt.show()
    
    # Return the processed data
    return membrane_potential, time, peak_times, peak_values

def calculate_slopes(y, peak_index, left_index, right_index):
    """
    Berechnet die Steigungen links und rechts eines Peaks basierend auf den Indizes.
    """
    left_slope = (y[peak_index] - y[left_index]) / (peak_index - left_index)
    right_slope = (y[right_index] - y[peak_index]) / (right_index - peak_index)
    return left_slope, right_slope
