import sys
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import read
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QFileDialog
from aip import AipSpeech

class SoundApp:
    def __init__(self):
        self.win = QWidget()
        self.win.setGeometry(400, 400, 400, 600)
        self.win.setWindowTitle("语音合成工具")
        self.layout()

    def layout(self):
        lab1 = QLabel(self.win)
        lab1.setText('请输入文本：')
        lab1.move(10, 20)

        self.text_edit = QTextEdit(self.win)
        self.text_edit.resize(350, 100)
        self.text_edit.move(10, 40)

        bt1 = QPushButton(self.win)
        bt1.setText('合成(pytts)')
        bt1.move(30, 150)
        bt1.clicked.connect(lambda: self.tts(self.text_edit.toPlainText()))

        bt2 = QPushButton(self.win)
        bt2.setText('播放(离线)')
        bt2.move(150, 150)
        bt2.clicked.connect(lambda: self.playAudio('pytts.wav'))

        bt5 = QPushButton(self.win)
        bt5.setText('打开文件')
        bt5.move(250, 150)
        bt5.clicked.connect(self.openFile)

        bt3 = QPushButton(self.win)
        bt3.setText('合成(百度)')
        bt3.move(30, 400)
        bt3.clicked.connect(lambda: self.baidu_to_audio(self.text_edit.toPlainText()))

        bt4 = QPushButton(self.win)
        bt4.setText('播放(百度)')
        bt4.move(150, 400)
        bt4.clicked.connect(lambda: self.playAudio('baidu.wav'))

    def tts(self, text):
        if not text.strip():
            return
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.save_to_file(text, 'pytts.wav')
        engine.runAndWait()
        engine.stop()
        print("离线合成成功！")

    def baidu_to_audio(self, text):
        if not text.strip():
            return
        print("正在请求百度API合成语音...")
        APP_ID =''
        API_KEY = ''
        SECRET_KEY =''
        
        try:
            client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
            result = client.synthesis(text, 'zh', 1, {"vol": 5, "spd": 4, "pit": 9, "per": 0, "aue": 6})
            
            if not isinstance(result, dict):
                with open('baidu.wav', 'wb') as f:
                    f.write(result)
                print("百度合成成功！已保存为 baidu.wav")
            else:
                print(f"百度合成失败，错误信息: {result}")
        except Exception as e:
            print(f"调用百度API时发生异常: {e}")

    def playAudio(self, file):
        try:
            fs, data = read(file)
            sd.play(data, fs)
            sd.wait()
        except Exception as e:
            print(f"播放失败，请检查文件是否存在：{e}")

    def openFile(self):
        option, _ = QFileDialog.getOpenFileName(self.win, "选取文件", "./", "Text Files (*.txt);;All Files (*)")
        if option:
            with open(option, 'r', encoding='utf-8') as f:
                txt = f.read()
                self.text_edit.setText(txt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SoundApp()
    ex.win.show() 
    sys.exit(app.exec_())
