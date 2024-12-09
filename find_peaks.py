import numpy
import numpy as np
import os
import pathlib
import pandas as pd
import math

DIR = pathlib.Path(os.curdir)

def save_peak(peak_id, array_id, peak_nr, sample, time, baseline, abs_amplitude, rel_amplitude, fwhm):
    filepath = DIR / "data" / "peak_results.csv"

    if filepath.exists() and filepath.is_file() and filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
    else:
        df = pd.DataFrame(columns=["peak_id", "array_id", "peak_nr", "sample", "time", "baseline", "abs_amplitude", "rel_amplitude", "fwhm"])

    new_row = pd.DataFrame({"peak_id": peak_id,
               "array_id": array_id,
               "peak_nr": peak_nr,
               "sample": sample,
               "time": time,
               "baseline": baseline,
               "abs_amplitude": abs_amplitude,
               "rel_amplitude": rel_amplitude,
               "fwhm": fwhm})

    pd.concat([df, new_row])
    df.to_csv(filepath, index=False)

def find_peaks(data, samplerate):

    for row in data:
        baseline = get_baseline(row)
        std = numpy.std(row)

        for sample in row:
            if is_peak(sample, baseline, std):
                peak_id = 0
                array_id = 0
                peak_nr = 0
                sample_nr = 0
                time = samplerate * sample_nr
                abs_amplitude = sample
                rel_amplitude = abs_amplitude - baseline

                fwhm = get_fwhm(sample, abs_amplitude)
                save_peak(peak_id, array_id, peak_nr, sample_nr, time, baseline, abs_amplitude, rel_amplitude, fwhm)



