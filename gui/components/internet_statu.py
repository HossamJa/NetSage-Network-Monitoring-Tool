from PyQt5.QtWidgets import QWidget,QVBoxLayout, QLabel, QPushButton                          
from PyQt5.QtCore import Qt, QTimer
from gui.threads import NetStatChek


class InternetStatWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Internet Statues elements
        self.internet_stat_ttl = QLabel("Live Internet Statue", self)
        self.internet_statue = QLabel("🟦 Statue", self)
        self.net_check_btn = QPushButton("Check Net Status")  
        self.net_check_btn.setCheckable(True)
        self.net_check_btn.clicked.connect(self.toggle)

        # Troubleshooting Suggestions
        self.tr_sho_sugg_ttl = QLabel("🛠️Troubleshooting Suggestions", self)
        self.tr_sho_sugg = QLabel("💡 Suggestions.....", self)
        
        # Alignmet
        self.internet_stat_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.internet_statue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tr_sho_sugg_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Internet Statues Widget Layout
        internet_stat = QVBoxLayout()

        internet_stat.addWidget(self.internet_stat_ttl)
        internet_stat.addWidget(self.internet_statue)
        internet_stat.addWidget(self.net_check_btn )
        internet_stat.addWidget(self.tr_sho_sugg_ttl)
        internet_stat.addWidget(self.tr_sho_sugg)

        self.setLayout(internet_stat)

        # Create a QTimer for auto-refreshing the status
        self.internet_timer = QTimer(self)
        self.internet_timer.setInterval(15000)  # 15 seconds
        self.internet_timer.timeout.connect(self.run_stt_chk)

    def toggle(self):
        if self.net_check_btn.isChecked():
            self.net_check_btn.setText("⏹ Stop Monitoring")
            self.run_stt_chk()              
            self.internet_timer.start()
        else:
            self.net_check_btn.setText("▶ Start Monitoring")
            self.internet_timer.stop()             

    def run_stt_chk(self):
        self.NST_worker = NetStatChek()
        self.NST_worker.statu_ready.connect(self.show_NetStatu)
        self.NST_worker.start()
    
    def show_NetStatu(self, statu):
        internet_data = statu
        internet_statu = internet_data["net_status"]
        trblshoting_suggs = internet_data["suggests"]

        formatted_suggestions = trblshoting_suggs.replace("\n", "<br>")
        internet_status = internet_statu.replace("\n", "<br>")

        self.internet_statue.setText(f"""
            <html>
                <div style='font-size: 14px;'>
                    <span style='color: #007acc;'>{internet_status}</span>
                </div>
            </html>
        """)

        self.tr_sho_sugg.setText(f"""
            <html>
                <div style='font-size: 13px; margin-top: 10px;'>
                    <span>{formatted_suggestions}</span>
                </div>
            </html>
        """)


