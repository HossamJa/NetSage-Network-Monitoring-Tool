import sys
import pyttsx3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from backend.features import check_speed, creat_table, ftch_tst_rsults, export_tst_logs
from PyQt5.QtWidgets import (QApplication, QWidget,QVBoxLayout, QLabel, QScrollArea,
                             QLineEdit, QPushButton, QHBoxLayout, QCheckBox,
                             QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox)                             
from PyQt5.QtCore import QSize, Qt, QTimer, QThread, pyqtSignal

class NetworkMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # Test speed elements
        self.download_sped = QLabel("00 Mb/s", self)
        self.download_sped_ttl = QLabel("Download Speed", self)
        self.upload_sped = QLabel("00 Mb/s", self)
        self.upload_sped_ttl = QLabel("Upload Speed", self)
        self.ping_ttl = QLabel("Ping:", self)
        self.ping = QLabel("00ms", self)
        self.test_button = QPushButton("Start Speed Test", self)

        # Show ISP & Location Info
        self.ISP_ttl = QLabel("📊ISP:", self)
        self.ISP_info = QLabel("ISP info..", self)
        self.location_ttl = QLabel("📍 Location:", self)
        self.location_info = QLabel("Location info..", self)
        
        # Compare Speed to Global Average
        self.speed_compare_ttl = QLabel("Compare Speed to Global Average:", self)
        self.speed_compare = QLabel("Your internet Speed is above the Averge", self)

        # Website Checker elements
        self.website_checker_ttl = QLabel("Website Checker", self)
        self.input_url = QLineEdit("Enter a URL to check", self)
        self.website_statue = QLabel("Statues: ..", self)
        self.Check_web_button = QPushButton("Check Website Statues", self)

        # Internet Statues elements
        self.internet_stat_ttl = QLabel("Internet Statue Is:", self)
        self.internet_statue = QLabel("🟢 Online", self)
        self.Check_Internet_button = QPushButton("Check Internet Statues", self)

        # Troubleshooting Suggestions
        self.tr_sho_sugg_ttl = QLabel("🛠️Troubleshooting Suggestions:", self)
        self.tr_sho_sugg = QLabel("Suggestions.....", self)

        # Show Past Speed Test Results as a Graph
        self.graph_ttl = QLabel("📊 Speed Test History & Graph", self)
        self.toggle_switch = QPushButton("Show Table", self)
        self.toggle_switch.setCheckable(True)
        self.toggle_switch.clicked.connect(self.toggle)

        self.generat_logs_button = QPushButton("Generate & Download Logs", self)
        self.generat_logs_button.clicked.connect(self.export_pdf)
        self.txt_msg = QLabel()
        self.filter_box = QComboBox()
        self.canvas = None
        self.table_widget = None

        # Wifi Signal Strength Detector

        self.signal_ttl = QLabel("📡 Wi-Fi Signal Quality:", self)
        self.signal_quality = QLabel("GOOD", self)

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

        self.initUI()

    def initUI(self):

        #The Main Window
        self.setWindowTitle("TB Network Monitor")
        self.setFixedSize(QSize(1080, 650))
        
        main_layout = QVBoxLayout()

        #-----------The Top Section----------# 

        top_section = QHBoxLayout()

        # Website Cheker Widget
        web_checker = QVBoxLayout()
        web_checker.addWidget(self.website_checker_ttl)
        web_checker.addWidget(self.input_url)
        web_checker.addWidget(self.Check_web_button)
        web_checker.addWidget(self.website_statue)
        
        top_section.addLayout(web_checker, 1)

        # Test Speed widget
        tst_speed = QVBoxLayout()

        sped_data = QHBoxLayout()

        sped_data_1 = QVBoxLayout()
        sped_data_1.addWidget(self.download_sped)
        sped_data_1.addWidget(self.download_sped_ttl)
        sped_data.addLayout(sped_data_1)

        sped_data_2 = QVBoxLayout()
        sped_data_2.addWidget(self.upload_sped)
        sped_data_2.addWidget(self.upload_sped_ttl)
        sped_data.addLayout(sped_data_2)

        tst_speed.addLayout(sped_data)

        tst_speed.addWidget(self.ping_ttl)
        tst_speed.addWidget(self.ping)
        tst_speed.addWidget(self.test_button)

        sub_section = QHBoxLayout()

        sub_Vsection1 = QVBoxLayout()
        sub_Vsection1.addWidget(self.ISP_ttl)
        sub_Vsection1.addWidget(self.ISP_info)
        sub_Vsection1.addWidget(self.location_ttl)
        sub_Vsection1.addWidget(self.location_info)
        sub_section.addLayout(sub_Vsection1)

        sub_Vsection2 = QVBoxLayout()
        sub_Vsection2.addWidget(self.speed_compare_ttl)
        sub_Vsection2.addWidget(self.speed_compare)
        sub_section.addLayout(sub_Vsection2)

        tst_speed.addLayout(sub_section)

        top_section.addLayout(tst_speed, 2)

        # Internet Statues Widget
        internet_stat = QVBoxLayout()

        internet_stat.addWidget(self.internet_stat_ttl)
        internet_stat.addWidget(self.internet_statue)
        internet_stat.addWidget(self.Check_Internet_button)
        internet_stat.addWidget(self.tr_sho_sugg_ttl)
        internet_stat.addWidget(self.tr_sho_sugg)

        top_section.addLayout(internet_stat, 1)
      
        #-----------The Bottom Section----------# 
        bottom_section = QHBoxLayout()

        # Past Speed Test Results in Graph and Tables
        self.lay = QVBoxLayout()
        self.lay.insertWidget(0, self.graph_ttl)
        self.lay.insertWidget(1, self.toggle_switch)
        self.lay.insertWidget(2, self.filter_box)
        self.lay.insertWidget(5, self.generat_logs_button)
        self.lay.insertWidget(6, self.txt_msg)
        

        self.graph() # show graph by default

        bottom_section.addLayout(self.lay, 1)

        # Wifi Signal Quality
        sgnl_Qlty = QVBoxLayout()

        sgnl_Qlty.addWidget(self.signal_ttl)
        sgnl_Qlty.addWidget(self.signal_quality)

        # Auto speed tests & Alerts Widget

        sgnl_Qlty.addWidget(self.AutoSpedTst_Alert_ttl)
        sgnl_Qlty.addWidget(self.actv_auto_tst)

        v_inputs = QHBoxLayout()
        v_inputs.addWidget(self.time_interval)
        v_inputs.addWidget(self.download_threshold)
        v_inputs.addWidget(self.upload_threshold)
        v_inputs.addWidget(self.ping_threshold)
        sgnl_Qlty.addLayout(v_inputs)

        v_buttons = QHBoxLayout()
        v_buttons.addWidget(self.start_button)
        v_buttons.addWidget(self.stop_button)
        sgnl_Qlty.addLayout(v_buttons)

        sgnl_Qlty.addWidget(self.auto_sped_tst)
        sgnl_Qlty.addWidget(self.timer_label)

        bottom_section.addLayout(sgnl_Qlty, 1)

        # Adding top and bottom section to main_layout
        main_layout.addLayout(top_section)
        main_layout.addLayout(bottom_section)

        self.setLayout(main_layout)

        #++++++++++ Alignmet +++++++++++#

        self.website_checker_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_sped.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_sped.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ping.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_sped_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_sped_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ping_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.internet_stat_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.internet_statue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.signal_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.signal_quality.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.AutoSpedTst_Alert_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ++++++++ Style ++++++++ #

        # setting Labels
        self.download_sped.setObjectName("load_sped")
        self.upload_sped.setObjectName("load_sped")
        self.download_sped_ttl.setObjectName("download_sped_ttl")
        self.upload_sped_ttl.setObjectName("upload_sped_ttl")
        self.ping_ttl.setObjectName("ping_ttl")
        self.ping.setObjectName("ping")  
        self.test_button.setObjectName("test_button") 
        self.ISP_ttl.setObjectName("ISP_ttl")
        self.ISP_info.setObjectName("ISP_info")
        self.location_ttl.setObjectName("location_ttl")
        self.location_info.setObjectName("location_info")
        self.speed_compare.setObjectName("speed_compare") 
        self.website_checker_ttl.setObjectName("top_title") 
        self.input_url.setObjectName("input_url") 
        self.website_statue.setObjectName("website_statue") 
        self.Check_web_button.setObjectName("Check_web_button") 
        self.internet_stat_ttl.setObjectName("top_title") 
        self.internet_statue.setObjectName("internet_statue") 
        self.Check_Internet_button.setObjectName("Check_Internet_button") 
        self.tr_sho_sugg.setObjectName("tr_sho_sugg") 
        self.graph_ttl.setObjectName("top_title") 
        # the graph
        self.generat_logs_button.setObjectName("generat_logs_button") 
        self.signal_ttl.setObjectName("top_title") 
        self.signal_quality.setObjectName("signal_quality")
        self.AutoSpedTst_Alert_ttl.setObjectName("top_title")
        self.actv_auto_tst.setObjectName("auto_Sped_tst") 
        self.time_interval.setObjectName("tst_time_txt") 
        self.download_threshold.setObjectName("auto_tst_time") 
        self.start_button.setObjectName("activate_alert")
        self.stop_button.setObjectName("alert") 

        # Setting the Style 

        self.setStyleSheet("""
                QLabel, QPushButton{
                           font-family: calibri;
                }
                QLabel#load_sped{
                           font-size: 50px;
                           font-weight: bold;
                           }

                QLabel#top_title{
                           font-size: 15px;
                           font-weight: bold;
                           }

        """)

        # Connect checkbox to function
        self.actv_auto_tst.toggled.connect(self.toggle_auto_test_section)
        # Initially disable the section
        self.toggle_auto_test_section(False)

        # Trigers for Auto Test and Alerts
        self.start_button.clicked.connect(self.start_auto_test)
        self.stop_button.clicked.connect(self.stop_auto_test)
        
        # Create one voice thread instance at the class level
        self.say = None  

        # +++ For Data Visualisation in Graph and Table +++
        self.filter_box.addItem("Select Filter")
        self.filter_box.setCurrentIndex(0)
        self.filter_box.model().item(0).setEnabled(False)
        self.filter_box.addItems(["All", "Last 24 Hours", "Last 7 Days"])          
        # refresh when filter changes
        self.filter_box.currentTextChanged.connect(self.toggle)  

# ===================== Data Visualisation in Graph and Table ===================== #
    # Graph/Table Switch
    def toggle(self):
        if self.toggle_switch.isChecked():
            self.toggle_switch.setText("Show Graph")
            self.show_table()
        else:
            self.toggle_switch.setText("Show Table")
            self.show_graph()
    
    # Filters the data and returns the data to show in Table/Graph
    def get_filtered_results(self):
  
        all_results = ftch_tst_rsults()  # Get the Full data from DB
        selected = self.filter_box.currentText()

        if selected == "Last 24 Hours":
            cutoff = datetime.now() - timedelta(days=1)
        elif selected == "Last 7 Days":
            cutoff = datetime.now() - timedelta(days=7)
        else:
            return all_results

        filtered = []
        for row in all_results:
            ts = row[0]
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts.replace("Z", ""))
            elif isinstance(ts, (int, float)):
                ts = datetime.fromtimestamp(ts)
            
            if ts >= cutoff:
                filtered.append(row)
                
        return filtered

    def show_table(self):
        # Remove the graph if present
        if self.canvas:
            self.lay.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        # Remove any existing table
        if hasattr(self, "table_widget") and self.table_widget:
            self.lay.removeWidget(self.table_widget)
            self.table_widget.deleteLater()
            self.table_widget = None

        results = self.get_filtered_results()
        if not results:
            results = [(datetime.now(), "No Data", "No Data", "No Data")]

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(results))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Timestamp", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)"])
        # Manually set fixed column widths
        self.table_widget.setColumnWidth(0, 146)  
        self.table_widget.setColumnWidth(1, 105)  
        self.table_widget.setColumnWidth(2, 105)  
        self.table_widget.setColumnWidth(3, 70)

        # Make the table scrollable & responsive
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setMinimumHeight(300)  # Adjust as needed

        for row_idx, row in enumerate(results):
            timestamp = row[0]
            if "T" in str(timestamp):
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d / %H:%M:%S")
            else:
                timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d / %H:%M:%S")

            # Create table items
            items = [
                QTableWidgetItem(str(timestamp)),
                QTableWidgetItem(str(row[1])),
                QTableWidgetItem(str(row[2])),
                QTableWidgetItem(str(row[3]))
            ]

            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_idx, col, item)

        # Style and polish
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet("QTableWidget { border: 1px solid #ccc; background-color: #f9f9f9; }")

        # Insert at the same index where graph was inserted
        self.lay.insertWidget(3, self.table_widget)

    def show_graph(self):
        if self.table_widget:
            self.table_widget.setParent(None)

        self.graph()

    def graph(self):
        results = self.get_filtered_results()

        # Clear previous graph
        if self.canvas:
            self.lay.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.lay.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None

        if not results:
            self.no_data = QLabel("❗ No Test History To show Yet ❗")
            self.lay.insertWidget(3, self.no_data)
            ts = f"{datetime.now()}"
            results = [(ts.replace(" ", "T"), 0, 0, 0)]  # ensure it's a list of tuples

        # Process data
        timestamps, download, upload, ping = [], [], [], []
        for row in results:
            ts = row[0]
            if "T" in str(ts):
                ts = datetime.fromisoformat(ts.replace("Z", ""))
            else:
                ts = datetime.fromtimestamp(ts)
            timestamps.append(ts.strftime("%Y-%m-%d %H:%M:%S"))
            download.append(row[1])
            upload.append(row[2])
            ping.append(row[3])

        # Determine dynamic width based on data points
        base_width = 6
        extra_width = max(len(timestamps) // 5, 1)  # scale with more data
        fig_width = base_width + extra_width
        fig, ax1 = plt.subplots(figsize=(fig_width, 3))

        # Plotting
        dl_line, = ax1.plot(timestamps, download, label="Download (Mbps)", color='tab:blue', marker='o')
        ul_line, = ax1.plot(timestamps, upload, label="Upload (Mbps)", color='tab:green', marker='s')
        ax1.set_ylabel("Speed (Mbps)")
        ax1.set_xlabel("Date & Time")
        ax1.tick_params(axis='x', rotation=45)

        # Second y-axis for ping
        ax2 = ax1.twinx()
        ping_line, = ax2.plot(timestamps, ping, label="Ping (ms)", color='tab:red', marker='^')
        ax2.set_ylabel("Ping (ms)", color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

        # Tooltip
        cursor = mplcursors.cursor([dl_line, ul_line, ping_line], hover=True)

        @cursor.connect("add")
        def on_hover(sel):
            i = int(sel.index)
            if sel.artist == dl_line:
                sel.annotation.set_text(f"Download: {download[i]:.2f} Mbps")
            elif sel.artist == ul_line:
                sel.annotation.set_text(f"Upload: {upload[i]:.2f} Mbps")
            elif sel.artist == ping_line:
                sel.annotation.set_text(f"Ping: {ping[i]:.2f} ms")

        ax1.grid(True)
        fig.tight_layout()
        fig.autofmt_xdate()

        # Create canvas and scroll area
        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.resize(fig_width * 100, 300)  # width of plots canvas in pixels

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.canvas)

        # Insert graph with scroll into layout
        self.lay.insertWidget(3, self.scroll_area)

    # download Logs as PDF  
    def export_pdf(self):
        export = export_tst_logs() # Should return a success/fail message
        self.txt_msg.setText(export)
# ===================== End Data Visualisation in Graph and Table  ===================== #

    # ============ Geting data =====================#

    # +++ Starting Test speed +++ # 

    def get_speed_tst(self):
        print("yes")
        # Get the download/upload speed 
        ...

        # Get the ping


        # Get ISP info


        # Get Location info


        # Compare the speed with the averge
        ...

        # Wifi signal Quality 
        ...

    # +++ Website Checking +++ # 

    def get_website_stats(self):
        print("Website is Down")

    # +++  Internet Status +++ # 

    def get_internet_stats(self):
        print("Looking Good")
        # internet stats
        ...

        # get TroubleShooting suggestions if Error
        ...

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
            self.run_speed_test()
            self.timer_label.setText(f"🔄 Testing Internet Speed... ")
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

class SpeedTestWorker(QThread):
    result_ready = pyqtSignal(dict)

    def run(self):
        # Call the Check_Speed function from the Backend
        results = check_speed()
        self.result_ready.emit(results) 
        
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

# ++++++++++++++++++++ End Auto Speed Tests Feature ++++++++++++++++++++++++++++++++ #

def run_gui():
    app = QApplication(sys.argv)
    monitor_app = NetworkMonitor()
    monitor_app.show()
    sys.exit(app.exec_())
    
    # Creat the Database and the test history table
    creat_table()

if __name__ == "__main__":
    run_gui()