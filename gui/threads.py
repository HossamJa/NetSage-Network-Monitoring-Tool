
import pyttsx3
from backend.features import (check_speed, 
                            get_compareson, 
                            get_ISPndLoc_info, 
                            check_internet, 
                            check_Wifi_quality,
                            check_website_stat
                            )                        
from PyQt5.QtCore import QThread, pyqtSignal

class SpeedTestWorker(QThread):
    result_ready = pyqtSignal(dict)

    def run(self):
        # Call the Check_Speed function from the Backend
        results = check_speed()
        self.result_ready.emit(results) 

class IspWorker(QThread):
    info_ready = pyqtSignal(dict)

    def run(self):
        info = get_ISPndLoc_info()
        self.info_ready.emit(info) 

class AvgCompare(QThread):
    compare_ready = pyqtSignal(object)

    def run(self):
        compare = get_compareson()
        self.compare_ready.emit(compare) 

class NetStatChek(QThread):
    statu_ready = pyqtSignal(object)

    def run(self):
        statu = check_internet(use_color=False)
        self.statu_ready.emit(statu) 

class WifiSgnlQualty(QThread):
    sgnl_ready = pyqtSignal(object)
    def run(self):
        sgnl_qualty = check_Wifi_quality()
        self.sgnl_ready.emit(sgnl_qualty) 

class WebChecker(QThread):
    def __init__(self, url):
        super().__init__()
        self.url = url
    web_data_ready = pyqtSignal(dict)  

    def run(self):
        web_data = check_website_stat(self.url)
        self.web_data_ready.emit(web_data) 

class speak_warning(QThread):
    def __init__(self, message):
        super().__init__()
        self.message = message
    
    def run(self):
        self.run_speech(self.message)

    def run_speech(self, message):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if "english (united states)" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(message)
        engine.runAndWait()



