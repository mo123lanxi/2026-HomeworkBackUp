import sys
import os  
import pyttsx3
import json
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, 
                             QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout)
from PyQt5.QtMultimedia import QSound
from aip import AipSpeech

class SoundApp:
    def __init__(self):

        self.APP_ID = '8100361' 
        self.API_KEY = '2pHgyZOeePr8GHpJF4C7DvxO' 
        self.SECRET_KEY = 'SF85OIWanjlTPNXQeS0hjF9WqGIeoTpq' 
        
        self.TRANS_API_KEY = ""
        self.TRANS_SECRET_KEY = ""

        self.win = QWidget()
        self.win.setGeometry(400, 400, 500, 450) 
        self.win.setWindowTitle("语音合成工具")
        self.layout()

    def layout(self):
        main_layout = QVBoxLayout()
    
        main_layout.addWidget(QLabel('请输入文本：'))
        self.text_edit = QTextEdit()
        self.text_edit.setMaximumHeight(100)
        main_layout.addWidget(self.text_edit)

        h_layout1 = QHBoxLayout()
        bt1 = QPushButton('合成(pytts)')
        bt1.clicked.connect(lambda: self.tts(self.text_edit.toPlainText()))
        bt2 = QPushButton('播放(离线)')
        bt2.clicked.connect(lambda: self.playAudio('pytts.wav'))
        bt5 = QPushButton('打开文件')
        bt5.clicked.connect(self.openFile)
        h_layout1.addWidget(bt1)
        h_layout1.addWidget(bt2)
        h_layout1.addWidget(bt5)
        main_layout.addLayout(h_layout1)

        h_layout2 = QHBoxLayout()
        bt3 = QPushButton('合成(百度)')
        bt3.clicked.connect(lambda: self.baidu_to_audio(self.text_edit.toPlainText()))
        bt4 = QPushButton('播放(百度)')
        bt4.clicked.connect(lambda: self.playAudio('baidu.wav'))
        bt_recog = QPushButton('打开音频并识别')
        bt_recog.clicked.connect(self.recognize_audio)
        h_layout2.addWidget(bt3)
        h_layout2.addWidget(bt4)
        h_layout2.addWidget(bt_recog)
        main_layout.addLayout(h_layout2)

        h_layout3 = QHBoxLayout()
        h_layout3.addStretch(1) 
        bt_trans = QPushButton('翻译内容')
        bt_trans.clicked.connect(self.translate_text)
        h_layout3.addWidget(bt_trans)
        h_layout3.addStretch(1)
        main_layout.addLayout(h_layout3)

        self.lab_recog = QLabel('识别结果：')
        main_layout.addWidget(self.lab_recog)
        self.lab_trans = QLabel('翻译结果：')
        main_layout.addWidget(self.lab_trans)
        
        main_layout.addStretch(1)
        self.win.setLayout(main_layout)

    def playAudio(self, file):
        if not os.path.exists(file):
            print(f"播放失败，文件 {file} 不存在！请先点击合成按钮。")
            return
        self.audio = QSound(file)
        self.audio.play()

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
        
        try:
            client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
            result = client.synthesis(text, 'zh', 1, {"vol": 5, "spd": 4, "pit": 9, "per": 0, "aue": 6})
            
            if not isinstance(result, dict):
                with open('baidu.wav', 'wb') as f:
                    f.write(result)
                print("百度合成成功！已保存为 baidu.wav")
            else:
                print(f"百度合成失败，错误信息: {result}")
        except Exception as e:
            print(f"调用百度API时发生异常: {e}")

    def translate_text(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            return
            
        print("正在翻译...")
        token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.TRANS_API_KEY}&client_secret={self.TRANS_SECRET_KEY}"
        
        try:
            token = requests.get(token_url).json().get("access_token")
            
            fr, to = 'zh', 'en'
            if text[0].isalpha(): 
                fr, to = 'en', 'zh'
                
            url = f"https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token={token}"
            payload = json.dumps({"from": fr, "to": to, "q": text})
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            
            response = requests.post(url, headers=headers, data=payload)
            result = response.json()

            trans_result = result['result']['trans_result'][0]['dst']
            self.lab_trans.setText('翻译结果：' + trans_result)
            print("翻译成功:", trans_result)

            print("正在将翻译结果合成为语音...")
            client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

            audio_data = client.synthesis(trans_result, 'zh', 1, {"vol": 5, "spd": 4, "per": 0, "aue": 6})
            
            if not isinstance(audio_data, dict):

                with open('trans_audio.wav', 'wb') as f:
                    f.write(audio_data)
                print("翻译音频生成成功！正在播放...")

                self.playAudio('trans_audio.wav')
            else:
                print(f"翻译结果语音合成失败: {audio_data}")
                
        except Exception as e:
            print("翻译发生异常:", e)
            self.lab_trans.setText('翻译结果：API调用失败，请检查网络或Key')

    def recognize_audio(self):
        option, _ = QFileDialog.getOpenFileName(self.win, "选择要识别的音频", "./", "Audio Files (*.wav);;All Files (*)")
        if not option:
            return
            
        print("正在识别...")
        try:
            client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
            with open(option, 'rb') as fp:
                audio_data = fp.read()
            
            result = client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
            
            if result.get('err_no') == 0:
                text = result.get('result')[0]
                self.lab_recog.setText('识别结果：' + text)
                self.text_edit.setText(text)
                print("识别成功:", text)
            else:
                self.lab_recog.setText('识别失败：' + result.get('err_msg', '未知错误'))
        except Exception as e:
            print("识别发生异常:", e)

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
