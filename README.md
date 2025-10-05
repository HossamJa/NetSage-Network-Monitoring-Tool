# 🌐 NetSage — Network Monitoring Tool

**NetSage** (previously "TB Network Monitor") is a Python-based tool for monitoring, analyzing, and troubleshooting internet connections.  
It provides both a **Command-Line Interface (CLI)** and a **Graphical User Interface (GUI)** (PyQt5) for flexibility and ease of use.

---

## 📖 Background Story

This project is special because it’s the **first real project I built after learning programming**.  
I started it right after completing **CS50’s Introduction to Programming with Python** (along with some FreeCodeCamp and YouTube courses).  

- I began working on this in **February 2025**, and by April, I had a working version.  
- I built it as part of my **final project submission for CS50**.  
- Later, I paused the project to focus on more certificates and learning.  
- In **September 2025**, I came back to finalize it for GitHub and polish the GUI version.  

It is **not perfect** — there are potential bugs and architectural mistakes I can now recognize, but that’s part of my journey.  
The goal was to **practice and apply all the Python basics** I had just learned, and I’m proud that it works fully.  
I plan to **keep updating, upgrading, and eventually turning it into a full-stack application**.

---
## Demo:

<iframe width="560" height="315" src="https://www.youtube.com/embed/_gS_DNmrXtE?si=TlTDibBSdm4Hwdly" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 🚀 Features

- **Speed Test** (Download, Upload, Ping).
- **ISP & Location Info** (IP, ISP, Country, Region, City, Timezone).
- **Auto Test & Alerts** (set thresholds and get alerts if connection drops).
- **Wi-Fi Signal Quality** monitoring.
- **Internet Connection Status** with troubleshooting suggestions.
- **Website Checker** (status, meta info, domain info, SSL, server IP).
- **History & Data Visualization**:
  - CLI → tables.
  - GUI → interactive graphs (PyQtGraph).
- **Compare with Global/National Average Speeds**.

---

## 📂 Project Structure

```
TB_Network_Monitor/
│
├── backend/                # Core feature logic
│   ├── features.py
│   └── __init__.py
│
├── gui/                    # GUI implementation
│   ├── main_window.py
│   ├── styles.py
│   ├── threads.py
│   ├── components/         # Feature-specific widgets
│   │   ├── auto_test.py
│   │   ├── data_visualisation.py
│   │   ├── internet_statu.py
│   │   ├── signal_quality.py
│   │   ├── speed_test.py
│   │   ├── web_checker.py
│   │   └── __init__.py
│   └── __init__.py
│
├── cli.py                  # Command-line interface
├── main.py                 # Entry point (choose CLI or GUI)
├── requirements.txt        # Dependencies
├── tbnm.db                 # Local database
└── README.md               # This file
```

---

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/HossamJa/NetSage-Network-Monitoring-Tool.git
cd NetSage-Network-Monitoring-Tool
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)

pip install -r requirements.txt
```

### 3. Run in CLI Mode

```bash
python main.py --cli
```

### 4. Run in GUI Mode

```bash
python main.py --gui
```

---

## 🎨 GUI Preview

* Built with **PyQt5**.
* Styled with **QSS (styles.py)**.
* Uses **PyQtGraph** for interactive history charts in GUI.
* Uses **Plotly** for interactive charts in browser for CLI.

---

## 🔮 Future Plans

* Add system tray **background monitoring**.
* Add **desktop notifications** for alerts.
* Add **multi-language support**.
* Expand to a **full-stack app** with a web dashboard.

---

## ✅ Final Notes

This project is where my coding journey started.
It represents my **growth from a beginner who knew nothing about programming, to someone who can now design, structure, and build functional apps**.

It may not be perfect — but it’s working, and it’s just the **first step in a much bigger journey** 🚀.
