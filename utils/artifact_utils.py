import os
import mne
import numpy as np
import matplotlib.pyplot as plt
import csv

def edf_raw_convertor(file_path):
    if os.path.isfile(file_path):
        extension = os.path.splitext(file_path)[-1].lower()
        if extension == '.edf':
            eeg_data_raw = mne.io.read_raw_edf(file_path, preload=True)
        else:
            print (f"This file does not have an .edf extension. It has {extension} extension.")
    else:
        print("The given path does not belong to a file.")
    return eeg_data_raw

def filter_bp_notch(eeg_raw_data):
    notch_filtered_raw = eeg_raw_data.copy().notch_filter(freqs = 50, notch_widths = 3)
    bp_filtered_raw = notch_filtered_raw.copy().filter(l_freq=1, h_freq=45)    
    return bp_filtered_raw
    
#def csv_numpy_convertor(data,):
    
def sliced_window_rawtoarray(filtered_raw_data, begin=None, end=None): #TypeError: slice indices must be integers or None or have an __index__ method
    "begin and end are in seconds where the window opens and closes"
    if begin != None and end !=None:
        start_time, stop_time = filtered_raw_data.time_as_index([begin, end])
        eeg_slice_array, time_slice_array = filtered_raw_data[:, start_time:stop_time]
    else:
        eeg_slice_array, time_slice_array = filtered_raw_data[:,:]
    return eeg_slice_array, time_slice_array

def gradient_eeg(eeg_slice_array):
    gradient_slice_array = np.diff(eeg_slice_array, n=1, axis=-1,append=0)/0.004 #-1 axis is row
    return gradient_slice_array

def bad_segments(filtered_array, gradient_array,gradient_limit, amplitude_limit):
    bad_indices = []
    for index in range(len(filtered_array[0,:])):
        # if index < len(filtered_array)-1:
        #     gradient = (filtered_array[:,index+1] - filtered_array[:,index])/0.004
        # else:
        #     gradient = 0
        
        #bad amplitude
        if max(abs(filtered_array[:,index]))>amplitude_limit or max(abs(gradient_array[:,index]))>gradient_limit:
            bad_indices.append(index)  
    return bad_indices

def bad_annotator(bad_indices,bp_filtered_raw,sfreq):    
    count = 0
    bad_segment_collection=[]
    for bad_index in bad_indices:
        current_time = bad_index/sfreq
        bad_label="BAD_"
        if count!=0 and bad_indices[count]-bad_indices[count-1]<51: #50*0.004sec = 0.2sec
            previous_entry=bad_segment_collection[len(bad_segment_collection)-1]
            previous_time = previous_entry[0]
            duration = current_time-previous_time
            bad_segment_collection[len(bad_segment_collection)-1]=(previous_time,duration,bad_label)
        else:
            duration = 1/sfreq
            bad_segment_collection.append((current_time, duration,bad_label))
        count +=1
    annotations = mne.Annotations(onset=[segment[0] for segment in bad_segment_collection],
                                  duration=[segment[1] for segment in bad_segment_collection],
                                  description = [segment[2] for segment in bad_segment_collection])
    
    annotated_raw = bp_filtered_raw.copy().set_annotations(annotations)
    return annotated_raw, annotations, bad_segment_collection   

def create_csv(data_with_multiple_rows, filename='Trial', participant='Nameless'):
    # New CSV file path
    cwd = os.getcwd()
    print(f"\nCurrent directory path: {cwd}")        
    if not os.path.exists(os.path.join(cwd,participant)):
        os.makedirs(participant)
    os.chdir("./" + participant)
    filename = filename + ".csv"
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(data_with_multiple_rows)
        print(f"\n{filename} file created at {os.path.join(cwd,participant)}")
    else:
        print("\nSorry a file with the same name already exists.\n"
              "Either change the directory or choose a different filename.")
    return

def plot_fft(eeg_filtered_raw):
    # Set epoch duration to 1 second
    epoch_duration = 1.0

    # Create events every 1 second
    events = mne.make_fixed_length_events(eeg_filtered_raw, duration=epoch_duration)

    # Create epochs
    epochs = mne.Epochs(eeg_filtered_raw, events, tmin=0, tmax=epoch_duration, baseline=None, preload=True)

    # Select a channel for FFT (you can modify this as needed)
    channels = ['O1', 'O2']

    # Sampling frequency and frequency bins for FFT
    sfreq = eeg_filtered_raw.info['sfreq']
    freqs = np.fft.rfftfreq(int(sfreq * epoch_duration), 1 / sfreq)

    # Plot setup
    plt.figure(figsize=(10, 6))

    # Compute and plot FFT for each channel
    for channel in channels:
        fft_results = []
        for epoch in epochs.get_data():
            channel_index = eeg_filtered_raw.ch_names.index(channel)
            fft_epoch = np.fft.rfft(epoch[channel_index])
            fft_results.append(fft_epoch)

        # Compute the average FFT across all epochs
        avg_fft = np.mean(np.abs(fft_results), axis=0)

        # Plot the FFT
        plt.plot(freqs, avg_fft, label=f'FFT of {channel}')

    # Finalizing the plot
    plt.title('FFT of Multiple Channels')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

    
if __name__ == "__main__":
    eeg_raw = edf_raw_convertor('./40hz_freq.edf')
    eeg_filtered_raw = filter_bp_notch(eeg_raw)
    eeg_array, _ = sliced_window_rawtoarray(eeg_filtered_raw)
    grad_eeg_array = gradient_eeg(eeg_array)
    bad_indices = bad_segments(eeg_array, grad_eeg_array, gradient_limit=4500e-6, amplitude_limit=200e-6)
    annotated_raw, annotations_mne, bad_segment_collection = bad_annotator(bad_indices,eeg_filtered_raw,sfreq=250)

    plot_fft(eeg_filtered_raw)

    participant_name = input("What is the name of the participant?\nDefault is 'Nameless'\n")
    file_title = input("Name of the file in which you want to save the artifact onset and duration:\n"
                     "Default is 'Trial'\n")
    
    if participant_name.isalpha():
        if file_title.isalpha():
            create_csv(bad_segment_collection, filename=file_title, participant=participant_name)
        else:
            create_csv(bad_segment_collection, participant=participant_name)
    elif file_title.isalpha():
        create_csv(bad_segment_collection,filename=file_title)
    else:
        create_csv(bad_segment_collection)
