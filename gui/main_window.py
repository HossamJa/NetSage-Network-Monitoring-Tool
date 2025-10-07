import sys
from backend.features import creat_table, valid_api_tooken
from PyQt5.QtWidgets import (QApplication, QWidget,QVBoxLayout, QLabel, QScrollArea,
                              QHBoxLayout, QCheckBox, QMainWindow,
                             QTableWidget, QSizePolicy, QComboBox)                             
from PyQt5.QtCore import QSize, Qt, QTimer, QThread, pyqtSignal
from gui.components.speed_test import SpeedTestWidget
from gui.components.web_checker import WebCheckerWidget
from gui.components.internet_statu import InternetStatWidget
from gui.components.data_visualisation import DataVison
from gui.components.signal_quality import SgnlQuality
from gui.components.auto_test import AutoTest


class NetworkMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TB-Network Monitor")
        self.setFixedSize(1080, 650)

        # Create and set central widget
        central = QWidget()
        self.setCentralWidget(central)

        #----------- Add layouts ----------#
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)
        # The top Section
        top_section = QHBoxLayout()
        main_layout.addLayout(top_section)

        # The Bottom Section
        bottom_section = QHBoxLayout()
        main_layout.addLayout(bottom_section)

        # ------------ Add feature components ---------- #
        top_section.addWidget(WebCheckerWidget(), 1)
        top_section.addWidget(SpeedTestWidget(), 2)
        top_section.addWidget(InternetStatWidget(), 1)

        bottom_section.addWidget(DataVison(), 2)
        
        left_section = QVBoxLayout()
        left_section.addWidget(SgnlQuality())
        left_section.addWidget(AutoTest())

        bottom_section.addLayout(left_section, 1)




def run_gui():
    # Validate the API tooken
    valid_api_tooken(gui=True)
    # Creat the Database and the test history table
    creat_table()
    # Show the app window    
    app = QApplication(sys.argv)
    monitor_app = NetworkMonitor()
    monitor_app.show()
    sys.exit(app.exec_())
    


if __name__ == "__main__":
    run_gui()