import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from datetime import datetime, timedelta
from backend.features import ftch_tst_rsults, export_tst_logs
from PyQt5.QtWidgets import (QWidget,QVBoxLayout, QLabel, QPushButton, QToolTip,
                             QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox)                             
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class DataVison(QWidget):
    def __init__(self):
        super().__init__()

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

        #Alignment
        self.graph_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Past Speed Test Results in Graph and Tables
        self.lay = QVBoxLayout()
        self.lay.insertWidget(0, self.graph_ttl)
        self.lay.insertWidget(1, self.toggle_switch)
        self.lay.insertWidget(2, self.filter_box)
        self.lay.insertWidget(5, self.generat_logs_button)
        self.lay.insertWidget(6, self.txt_msg)
        
        self.setLayout(self.lay)
        self.graph() # show graph by default

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
        if hasattr(self, 'graph_widget') and self.graph_widget:
            self.lay.removeWidget(self.graph_widget)
            self.graph_widget.deleteLater()
            self.graph_widget = None

        if not results:
            self.no_data = QLabel("❗ No Test History To Show Yet ❗")
            self.lay.insertWidget(3, self.no_data)
            ts = f"{datetime.now()}"
            results = [(ts.replace(" ", "T"), 0, 0, 0)]

        # Prepare data
        timestamps, download, upload, ping = [], [], [], []
        for row in results:
            ts = row[0]
            if "T" in str(ts):
                ts = datetime.fromisoformat(ts.replace("Z", ""))
            else:
                ts = datetime.fromtimestamp(ts)
            timestamps.append(ts.timestamp())  # Float for plotting
            download.append(row[1])
            upload.append(row[2])
            ping.append(row[3])

        # Setup plot
        self.graph_widget = pg.PlotWidget(title="📊 Speed Test History")
        self.graph_widget.setBackground("w")
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)
        self.graph_widget.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graph_widget.setLabel("bottom", "Date & Time")
        self.graph_widget.setLabel("left", "Speed (Mbps)")

        # Setup legend
        legend = self.graph_widget.addLegend(offset=(10, 10))
        
        # Set bottom X-axis as date & time
        axis = pg.DateAxisItem(orientation='bottom')
        self.graph_widget.setAxisItems({'bottom': axis})

        # Right axis for ping
        right_axis = pg.AxisItem('right')
        right_axis.setLabel("Ping (ms)")
        self.graph_widget.getPlotItem().layout.addItem(right_axis, 2, 2)
        ping_viewbox = pg.ViewBox()
        right_axis.linkToView(ping_viewbox)
        self.graph_widget.scene().addItem(ping_viewbox)
        ping_viewbox.setXLink(self.graph_widget)

        def sync_views():
            ping_viewbox.setGeometry(self.graph_widget.getViewBox().sceneBoundingRect())
        self.graph_widget.getViewBox().sigResized.connect(sync_views)

        # Plot Download & Upload
        dl_plot = self.graph_widget.plot(
            timestamps, download, pen=pg.mkPen((0, 122, 255), width=2),
            symbol='o', symbolBrush=(0, 122, 255), name="Download (Mbps)"
        )
        ul_plot = self.graph_widget.plot(
            timestamps, upload, pen=pg.mkPen((0, 200, 100), width=2),
            symbol='s', symbolBrush=(0, 200, 100), name="Upload (Mbps)"
        )

        # Plot ping on right ViewBox
        ping_line = pg.PlotDataItem(
            timestamps, ping, pen=pg.mkPen((200, 50, 50), width=2), name="Ping (ms)"
        )
        # This scatter is only to give a y value to the hover
        ping_scatter = pg.ScatterPlotItem(
            x=timestamps, y=ping,
            symbol='t', size=9,
            brush=pg.mkBrush(200, 50, 50, 160),
            pen=pg.mkPen(None)
        )

        ping_viewbox.addItem(ping_line)
        ping_viewbox.addItem(ping_scatter)
        legend.addItem(ping_line, "Ping (ms)")

        # Hover Tooltip
        def hover_event(event):
            if event.isExit():
                return
            pos = event.pos()
            x = pos.x()
            idx = min(range(len(timestamps)), key=lambda i: abs(timestamps[i] - x))
            date = datetime.fromtimestamp(timestamps[idx]).strftime("%Y-%m-%d %H:%M:%S")

            d = download[idx]
            u = upload[idx]
            p = ping[idx]

            text = (f"🕒 {date}\n"
                    f"📥 Download: {d:.2f} Mbps\n"
                    f"📤 Upload:   {u:.2f} Mbps\n"
                    f"📶 Ping:     {p:.2f} ms")

            QToolTip.showText(QCursor.pos(), text)

        ping_scatter.hoverEvent = hover_event
        self.graph_widget.setCursor(Qt.PointingHandCursor)

        # Add this graph to layout
        self.lay.insertWidget(3, self.graph_widget)

    # download Logs as PDF  
    def export_pdf(self):
        export = export_tst_logs() # Should return a success/fail message
        self.txt_msg.setText(export)
# ===================== End Data Visualisation in Graph and Table  ===================== #
