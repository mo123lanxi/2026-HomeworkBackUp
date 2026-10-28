import sounddevice as sd
from scipy.io.wavfile import write, read

def record_audio(file_path, seconds=4, fs=16000):
    print(f"开始录音，请对着麦克风说话（{seconds}秒）...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  
    write(file_path, fs, myrecording)  
    print(f"录音结束，已保存为 {file_path}")

def play_audio(file_path):
    print("开始播放...")
    fs, data = read(file_path)  
    sd.play(data, fs)           
    sd.wait()                   
    print("播放结束")

if __name__ == '__main__':
    wav_file = 'test.wav'
    record_audio(wav_file)  
    play_audio(wav_file)    
