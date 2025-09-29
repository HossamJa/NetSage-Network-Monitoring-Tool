from PyQt5.QtWidgets import (QWidget,QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QHBoxLayout, QCheckBox)                             
from PyQt5.QtCore import Qt, QTimer
from gui.threads import speak_warning, SpeedTestWorker

class AutoTest(QWidget):
    def __init__(self):
        super().__init__()

        # Auto Speed Tests & Alerts
        self.AutoSpedTst_Alert_ttl = QLabel("Auto Speed Tests & Alerts", self)
        self.actv_auto_tst = QCheckBox("Activate Auto Speed Test", self)
        
        self.time_interval = QLineEdit(self)
        self.time_interval.setPlaceholderText("Time Interval (seconds)")
        
        self.download_threshold = QLineEdit(self)
        self.download_threshold.setPlaceholderText("Download Threshold (Mbps)")
        
        self.upload_threshold = QLineEdit(self)
        self.upload_threshold.setPlaceholderText("Upload Threshold (Mbps)")
        
        self.ping_threshold = QLineEdit(self)
        self.ping_threshold.setPlaceholderText("Ping Threshold (ms)")
        
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)

        self.auto_sped_tst = QLabel("Speed Test Results Will Appear Here", self)
        self.timer_label = QLabel("Next test in X seconds", self)
        self.timer = QTimer()

        # Alignments
        self.AutoSpedTst_Alert_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Auto speed tests & Alerts Widget
        autotest = QVBoxLayout()
        autotest.addWidget(self.AutoSpedTst_Alert_ttl)
        autotest.addWidget(self.actv_auto_tst)

        v_inputs = QHBoxLayout()
        v_inputs.addWidget(self.time_interval)
        v_inputs.addWidget(self.download_threshold)
        v_inputs.addWidget(self.upload_threshold)
        v_inputs.addWidget(self.ping_threshold)
        autotest.addLayout(v_inputs)

        v_buttons = QHBoxLayout()
        v_buttons.addWidget(self.start_button)
        v_buttons.addWidget(self.stop_button)
        autotest.addLayout(v_buttons)

        autotest.addWidget(self.auto_sped_tst)
        autotest.addWidget(self.timer_label)

        self.setLayout(autotest)

        # Connect checkbox to function
        self.actv_auto_tst.toggled.connect(self.toggle_auto_test_section)
        # Initially disable the section
        self.toggle_auto_test_section(False)

        # Trigers for Auto Test and Alerts
        self.start_button.clicked.connect(self.start_auto_test)
        self.stop_button.clicked.connect(self.stop_auto_test)
        
        # Create one voice thread instance at the class level
        self.say = None  
# +++++++++++++++++++++++++++++++ Auto Speed Tests Feature | Start +++++++++++++++++++++++++++++++++++++++ #
    
    # Active/disactive Auto Test Switch 
    def toggle_auto_test_section(self, checked):
        """Enable/Disable the auto test section based on checkbox state"""
        for widget in [self.time_interval, self.download_threshold, self.upload_threshold, 
                       self.ping_threshold, self.start_button, self.stop_button]:
            widget.setEnabled(checked)
        
        # Grey out when disabled
        opacity = "1" if checked else "0.5"
        self.AutoSpedTst_Alert_ttl.setStyleSheet(f"color: rgba(0, 0, 0, {opacity});")
        self.auto_sped_tst.setStyleSheet(f"color: rgba(0, 0, 0, {opacity});")
        self.timer_label.setStyleSheet(f"color: rgba(0, 0, 0, {opacity});")
        if not checked:
            self.stop_auto_test()
            self.auto_sped_tst.setText(" 🔏 Auto Speed Test Disactivated.")

    # Start Auto Speed Test       
    def start_auto_test(self):

        # Check if digit or float
        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
            
        # Validat user input values to be correct
        if not self.time_interval.text().isdigit():
            self.auto_sped_tst.setText("❌ <span style='color: red;'>Invalid Time Interval Value!</span>")
        
        elif not is_float(self.download_threshold.text()):
            self.auto_sped_tst.setText("❌ <span style='color: red;'>Invalid Download Threshold Value!</span>")
        
        elif not is_float(self.upload_threshold.text()):
            self.auto_sped_tst.setText("❌ <span style='color: red;'>Invalid Upload Threshold Value!</span>")
        
        elif not is_float(self.ping_threshold.text()):
            self.auto_sped_tst.setText("❌ <span style='color: red;'>Invalid Ping Threshold Value!</span>")
        
        else: # Starts the Auto test
            self.auto_sped_tst.setText(" ✅ Auto Speed Test is Running.")
            self.countdown = int(self.time_interval.text())
            self.timer.timeout.connect(self.update_countdown)
            self.timer.start(1000)  

    # Stop Auto Speed Test
    def stop_auto_test(self):
        self.timer.stop()
        self.timer_label.setText("⏹ Auto Speed Test Stopped.")
        if hasattr(self, 'worker') and self.worker.isRunning():
                self.worker.terminate()  
                self.worker.wait()

    def update_countdown(self):
        if self.countdown > 0:
            self.timer_label.setText(f"⏳ Next test in {self.countdown} seconds...")
            self.countdown -= 1
        else:
            self.timer.stop()
            self.timer_label.setText(f"🔄 Testing Internet Speed... ")            
            self.run_speed_test()
            self.countdown = int(self.time_interval.text())
    
    def run_speed_test(self):

        self.worker = SpeedTestWorker()
        self.worker.result_ready.connect(self.process_speed_results)
        self.worker.start()

    def process_speed_results(self, results):

        if "Error" in results:
            self.auto_sped_tst.setText(f"""
                <p style='color: red;'>❌ You Are Disconnected. Check Your Connection.</p>
                <p>Error:</p>
                <p>{results}</p>
            """)
            self.timer_label.setText(f"🔴Connection Issue! Start Again.")
                 
        else:
            download = results["Download"]
            upload = results["Upload"]
            ping = results["Ping"]

            # Default colors
            download_color = "green"
            upload_color = "green"
            ping_color = "green"
            dwn_stat = "<span style='color: green;'>✔ Fine</span>"
            up_stat = "<span style='color: green;'>✔ Fine</span>"
            png_stat = "<span style='color: green;'>✔ Fine</span>"

            # Convert threshold values
            dwn_thres = float(self.download_threshold.text()) if self.download_threshold.text() else 0
            up_thres = float(self.upload_threshold.text()) if self.upload_threshold.text() else 0
            ping_thres = float(self.ping_threshold.text()) if self.ping_threshold.text() else 0

        
            warning_message = None  # Store only one warning message

            if download < dwn_thres:
                dwn_stat = "<span style='color: red;'>⚠ Warning! Low Download Speed ⚠</span>"
                download_color = "red"
                warning_message = "Warning! Low download speed detected."

            if upload < up_thres:
                up_stat = "<span style='color: red;'>⚠ Warning! Low Upload Speed ⚠</span>"
                upload_color = "red"
                warning_message = "Warning! Low upload speed detected."

            if ping > ping_thres:
                png_stat = "<span style='color: red;'>⚠ Warning! High Latency Detected ⚠</span>"
                ping_color = "red"
                warning_message = "Warning! High latency detected."

            if warning_message:
                if self.say is None or not self.say.isRunning():
                    self.say = speak_warning(warning_message)
                    self.say.start()

            self.auto_sped_tst.setText(f"""
            <html>
                <b>📡 Internet Speed Test Results</b><br>
                ━━━━━━━━━━━━━━━━━━━━━━━━━━<br><br>

                ⬇ Download Speed: <span style='color: {download_color};'>{download:.2f} Mbps</span> {dwn_stat}<br>
                ⬆ Upload Speed: <span style='color: {upload_color};'>{upload:.2f} Mbps</span> {up_stat}<br>
                📶 Ping: <span style='color: {ping_color};'>{ping} ms</span> {png_stat}<br>
            </html>
            """)

            self.countdown = int(self.time_interval.text())  # Reset countdown
            self.timer.start(1000)
