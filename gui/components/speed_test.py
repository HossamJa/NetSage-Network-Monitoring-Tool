
from gui.threads import SpeedTestWorker, IspWorker, AvgCompare
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton                                                     
from PyQt5.QtCore import Qt


class SpeedTestWidget(QWidget):
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
        
        self.st_message = QLabel()
        self.isp_message = QLabel()
        self.cpr_message = QLabel()

        # Show ISP & Location Info
        self.ISP_ttl = QLabel("🌐 ISP & Location", self)
        self.ISP_info = QLabel("""
        <html>
            <b>🔸 Public IP:</b> <span style="color:#999;">_</span><br>
            <b>🏢 ISP:</b> <span style="color:#999;">_</span><br>
            <b>📍 Location:</b> <span style="color:#999;">_</span><br>
            <b>📮 Postal Code:</b> <span style="color:#999;">_</span><br>
            <b>🕓 Timezone:</b> <span style="color:#999;">_</span>
        </html>
        """, self)

        self.ISP_info.setStyleSheet("font-size: 10px;")
        self.ISP_info.setWordWrap(True)

        # Compare Speed to Global Average
        self.speed_compare_ttl = QLabel("""<html>
            <b>🌍 Avg Net Speed in <span style="color:#007acc;">Your Country</span>:</b>
            </html>""", self)
        
        self.speed_compare = QLabel("""<html>
            <b>⬇ Avg Download:</b> <span style="color:#555;">_ Mb/s</span><br>
            <b>📊 Comparison:</b> <span style="color:#888;">_</span><br><br>
            <b>⬆ Avg Upload:</b> <span style="color:#555;">_ Mb/s</span><br>
            <b>📊 Comparison:</b> <span style="color:#888;">_</span><br><br>
            <b>📶 Avg Ping:</b> <span style="color:#555;">_ ms</span><br>
            <b>📊 Comparison:</b> <span style="color:#888;">_</span>
        </html>
        """, self)

        # Alignment
        self.download_sped.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_sped.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ping.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_sped_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_sped_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ping_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ISP_ttl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ISP_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.speed_compare_ttl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Layout
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
        sub_section.addLayout(sub_Vsection1)

        sub_Vsection2 = QVBoxLayout()
        sub_Vsection2.addWidget(self.speed_compare_ttl)
        sub_Vsection2.addWidget(self.speed_compare)
        sub_section.addLayout(sub_Vsection2)

        tst_speed.addLayout(sub_section)

        self.setLayout(tst_speed)

        # Connect Button
        self.test_button.clicked.connect(self.show_data)

    def show_data(self):
        self.sped_worker = SpeedTestWorker()
        self.sped_worker.result_ready.connect(self.handle_speed_done)
        self.sped_worker.start()
   
    def handle_speed_done(self, speed_result):
        self.show_sped_test(speed_result) 

        self.isp_worker = IspWorker()
        self.isp_worker.info_ready.connect(self.handle_isp_done)
        self.isp_worker.start()

    def handle_isp_done(self, isp_info):
        self.show_isp_info(isp_info) 

        self.cpr_worker = AvgCompare()
        self.cpr_worker.compare_ready.connect(self.show_avg_compare)
        self.cpr_worker.start()

    country = None
    def show_sped_test(self, results):
        
        if "Error" in results:
            self.st_message.setText(f"""
                <p style='color: red;'>❌ You Are Disconnected. Check Your Connection.</p>
                <p>Error:</p>
                <p>{results}</p>
            """)
        else:
            self.st_message.setText("")
            download = results["Download"]
            upload = results["Upload"]
            ping = results["Ping"]
            self.country = results["Country_gui"]

            self.download_sped.setText(f"{download}")
            self.upload_sped.setText(f"{upload}")
            self.ping.setText(f"{ping}")

    def show_isp_info(self, info):

        if "Error" in info:
            self.isp_message.setText(f"""
                <p style='color: red;'>{info["Error"]}</p>
            """)
        else:    
            self.ISP_info.setText(f""" 
            <html>                          
                <b>🔸 Public IP:</b> <span style="color:#2a9df4;">{info['IP']}</span><br>
                <b>🏢 ISP:</b> <span style="color:#2a9d8f;">{info['ISP']}</span><br>
                <b>📍 Location:</b> <span style="color:#555;">{info['City']}, {info['Region']}, {info['Country_cli']}</span><br>
                <b>📮 Postal Code:</b> <span style="color:#555;">{info['Postal']}</span><br>
                <b>🕓 Timezone:</b> <span style="color:#555;">{info['TimeZone']}</span>
            </html>""")

    def show_avg_compare(self, compare):
        if "No" in compare or "Error" in compare:
            self.cpr_message.setText(compare)
            return
        else:
            self.cpr_message.setText("")
            down_compare, averge_down_sped, up_compare, averge_up_sped, ping_compare, averge_ping = compare
            self.speed_compare_ttl.setText(f"""
            <html> 
                <b>🌍 Avg Net Speed in <span style="color:#007acc;">{self.country}</span>:</b><br><br>
            </html> """)

            self.speed_compare.setText(f"""
            <html> 
                <b>⬇ Avg Download:</b> <span style="color:#2e8b57;">{averge_down_sped} Mb/s</span><br>
                <b>{down_compare}</span><br>
                <b>⬆ Avg Upload:</b> <span style="color:#2e8b57;">{averge_up_sped} Mb/s</span><br>
                <b>{up_compare}</span><br>
                <b>📶 Avg Ping:</b> <span style="color:#2e8b57;">{averge_ping} ms</span><br>
                <b>{ping_compare}</span>
            </html> """)

