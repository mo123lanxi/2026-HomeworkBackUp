from aip import AipSpeech
def baidu_to_audio(self,text):
        APP_ID =''
        API_KEY = ''
        SECRET_KEY =''
        client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
        file = 'baidu.wav' 
        synth_context=client.synthesis(text,'zh',1,
                {"vol":5, "spd":4,"pit":9,"per":0,"aue":6})
        with open(file,'wb') as f:
            f.write(synth_context) 
        f.close()
