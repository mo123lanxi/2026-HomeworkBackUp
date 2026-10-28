import pyttsx3

def text_to_speech(text):

    engine = pyttsx3.init()

    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 0.8) 
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    engine.save_to_file(text, 'pytts.wav')
    
    engine.runAndWait()
    engine.stop()
    print("语音合成完毕，已保存为 pytts.wav")

if __name__ == '__main__':
    text = "这是一句测试"
    text_to_speech(text)
