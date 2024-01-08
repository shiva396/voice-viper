import pyaudio
import struct
import pyautogui  
# to press a button to play the game

# below are the four wake word's path that you have generated earlier
key1 = 'go-down_en_windows_v2_2_0.ppn'
key2 = 'go-left_en_windows_v2_2_0.ppn'
key3 = 'go-right_en_windows_v2_2_0.ppn'
key4 = 'go-upside_en_windows_v2_2_0.ppn'
# D:\Programming\Python\Voice Viper\go-down_en_windows_v2_2_0.ppn

# this is the library path that you can fnd inside Porcupine -> lib -> system(windows or linux or mac) -> os type( 64 or 32 bit)
library_path = '/Porcupine/lib/windows/amd64/libpv_porcupine.dll' 

# this is model file path can be find inside Porcupine -> lib -> common
model_file_path = '/Porcupine/lib/common/porcupine_params.pv'
keyword_file_paths = [key1, key2, key3, key4]
sensitivities = [0.5,0.5,0.5,0.5]
handle = pyporcupine(library_path, model_file_path, keyword_file_paths=keyword_file_paths, sensitivities=sensitivities)

def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=handle.frame_length,input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm

while True:
    pcm = get_next_audio_frame()
    keyword_index = handle.process(pcm)
    if keyword_index==1:
        print(keyword_index)
        pyautogui.press('up')
    if keyword_index==3:
        print(keyword_index)
        pyautogui.press('left')
    if keyword_index==2:
        print(keyword_index)
        pyautogui.press('right')
    if keyword_index==0:
        print(keyword_index)
        pyautogui.press('down')