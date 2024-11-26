from pydub import AudioSegment
import numpy as np
from scipy.signal import butter, lfilter
from io import BytesIO

def normalize_audio(audio: AudioSegment) -> AudioSegment:
    """
    Normalize the audio to -1 dBFS.
    
    :param audio: The input audio segment.
    :return: Normalized audio segment.
    """
    return audio.apply_gain(-audio.max_dBFS - 1)

def increase_sample_rate(audio: AudioSegment, new_sample_rate: int) -> AudioSegment:
    """
    Increase the sample rate of the audio.
    
    :param audio: The input audio segment.
    :param new_sample_rate: Desired sample rate in Hz.
    :return: Audio segment with increased sample rate.
    """
    # Resample the audio
    return audio.set_frame_rate(new_sample_rate)

def butter_highpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order)
    y = lfilter(b, a, data)
    return y

def apply_high_pass_filter(audio: AudioSegment, cutoff_freq: float) -> AudioSegment:
    """
    Apply a high-pass filter to the audio.
    
    :param audio: The input audio segment.
    :param cutoff_freq: Cutoff frequency for the high-pass filter in Hz.
    :return: Audio segment with high-pass filter applied.
    """
    # Convert the audio to a numpy array of samples
    samples = np.array(audio.get_array_of_samples())
    
    # Apply high-pass filter (scipy-based filtering)
    fs = audio.frame_rate  # Sample rate of the audio
    filtered_samples = highpass_filter(samples, cutoff_freq, fs)
    
    # Convert the filtered samples back to a pydub AudioSegment
    filtered_samples = np.array(filtered_samples, dtype=np.int16)
    filtered_audio = AudioSegment(
        filtered_samples.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )
    
    return filtered_audio

def process_audio(input_file: str, output_file: str) -> None:
    """
    Process the audio file to improve its quality.
    
    :param input_file: Path to the input audio file.
    :param output_file: Path to save the processed audio file.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Normalize the audio
    audio = normalize_audio(audio)
    
    # Increase sample rate
    new_sample_rate = 44100  # Example: CD quality sample rate
    audio = increase_sample_rate(audio, new_sample_rate)
    
    # Apply high-pass filter
    cutoff_freq = 300.0  # Example cutoff frequency in Hz
    audio = apply_high_pass_filter(audio, cutoff_freq)
    
    # Export the processed audio
    audio.export(output_file, format="wav")
    print(f"Processed audio saved to {output_file}")
    
# Define input and output file paths
input_file = "input_audio.mp3"  # Path to your input audio file
output_file = "output_audio.wav"  # Path to save the output audio file

process_audio(input_file, output_file)
  
