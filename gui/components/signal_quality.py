
from PyQt5.QtWidgets import  QWidget,QVBoxLayout, QLabel                           
from PyQt5.QtCore import Qt, QTimer
from gui.threads import WifiSgnlQualty

class SgnlQuality(QWidget):
    def __init__(self):
        super().__init__()

        # Wifi Signal Strength Detector
        self.signal_ttl = QLabel("📡 Wi-Fi Signal Quality:", self)
        self.signal_quality = QLabel("〰 Signal Strength...", self)

        # Alignmets 
        self.signal_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.signal_quality.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Wifi Signal Quality Layout
        sgnl_Qlty = QVBoxLayout()

        sgnl_Qlty.addWidget(self.signal_ttl)
        sgnl_Qlty.addWidget(self.signal_quality)

        self.setLayout(sgnl_Qlty)

        # Create a QTimer for auto-refreshing 
        self.internet_timer = QTimer(self)
        self.internet_timer.setInterval(15000)  # 15 seconds
        self.internet_timer.timeout.connect(self.run_signal_chk)
        self.internet_timer.start()
 
    def run_signal_chk(self):
        self.sgnl_worker = WifiSgnlQualty()
        self.sgnl_worker.sgnl_ready.connect(self.show_sgnl_qlty)
        self.sgnl_worker.start()

    def show_sgnl_qlty(self, sgnl):
        sgnl_info = sgnl.replace("\n", "<br>")
        self.signal_quality.setText(f"""
            <html>
                <div style='font-size: 12px;'>
                    <span style='color: #007acc;'>{sgnl_info}</span>
                </div>
            </html>
        """)

