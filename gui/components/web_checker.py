from PyQt5.QtWidgets import ( QWidget,QVBoxLayout, QLabel,
                             QLineEdit, QPushButton)                             
from PyQt5.QtCore import Qt
from gui.threads import WebChecker

class WebCheckerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Website Checker elements
        self.website_checker_ttl = QLabel("🔎 Website Checker", self)
        self.input_url = QLineEdit(self)
        self.input_url.setPlaceholderText("Enter a URL to check")
        self.web_message = QLabel()
        self.website_statue = QLabel("Statues: ..", self)
        self.Check_web_button = QPushButton("Check Website Statues", self)

        # Alignmet
        self.website_checker_ttl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.web_message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Website Cheker Widget Layout
        web_checker = QVBoxLayout()
        web_checker.addWidget(self.website_checker_ttl)
        web_checker.addWidget(self.input_url)
        web_checker.addWidget(self.web_message)
        web_checker.addWidget(self.Check_web_button)
        web_checker.addWidget(self.website_statue)
        
        self.setLayout(web_checker)

        # Connect button
        self.Check_web_button.clicked.connect(self.run_web_checker)

    def run_web_checker(self):
        self.web_worker = WebChecker(self.input_url.text())
        self.web_worker.web_data_ready.connect(self.show_web_statu)
        self.web_worker.start()
        self.web_message.setText("🔄 Checking URL Status....")
    
    def show_web_statu(self, web_data):

        err_messge = "❌ No Internet, Please Check Your Connection"
        if err_messge in web_data:
            self.web_message.setText(err_messge)
            return    

        if web_data["domain_info"] is None:
            self.web_message.setText(web_data["status"])
            self.website_statue.setText("")
        else:
            self.web_message.setText("✔ Complet")

            formatted_ping = "<br>".join(web_data["ping"]) if isinstance(web_data["ping"], list) else web_data["ping"]
            domain = web_data['domain_info'].replace('\n', '<br>')

            self.website_statue.setText(f"""
                <html>
                    <div style="font-family:Calibri, sans-serif; font-size:13px; color:#222;">
                        <b>🔎 Website Status:</b><br>
                        <span style="color:green;">{web_data['status']}</span><br><br>

                        <b>⏱️ Response Time:</b> {round(web_data['response_time'], 2)} seconds<br><br>

                        <b>📄 Meta Title:</b><br>
                        <span>{web_data['meta_title']}</span><br><br>

                        <b>📝 Meta Description:</b><br>
                        <span>{web_data['meta_description']}</span><br><br>

                        <b>🔐 SSL Status:</b><br>
                        <span>{web_data['ssl_status']}</span><br><br>

                        <b>🌐 Server IP:</b> {web_data['server_ip']}<br><br>

                        <b>📶 Ping Result:</b><br>
                        <pre style="background-color:#f8f8f8; border:1px solid #ccc; padding:6px;">{formatted_ping}</pre><br>

                        <b>📜 Domain Info:</b><br>
                        <pre style="background-color:#f8f8f8; border:1px solid #ccc; padding:6px;">{domain}</pre>
                    </div>
                </html> """)
