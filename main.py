import argparse
from cli import run_cli
from gui.main_window import run_gui

def parse_args():
    parser = argparse.ArgumentParser(description="📡 NetMon - Network Monitoring Tool")
    parser.add_argument('--cli', action='store_true', help="Run the app in CLI mode")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.cli:
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()
