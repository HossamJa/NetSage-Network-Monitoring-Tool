import os
import platform
import sys
import time
import threading
import socket
from datetime import datetime
from colorama import init, Fore, Style
init(autoreset=True)
from backend.features import (check_speed, get_ISPndLoc_info, get_compareson, check_internet,
                      check_website_stat, check_Wifi_quality, auto_tst_alert, delet_rsults,
                      tst_hstry_graph, tst_hstry_table, export_tst_logs, creat_table
                      )

def run_cli():
    show_dashboard()

    while True:
        try:
            cmd = input(Fore.BLUE + "\nNetwork Monitor>>> " + Style.RESET_ALL).strip().lower()
            
            if cmd == "exit" or cmd == "xt":
                print("\n👋 Exiting TB-NetMon CLI. See you!\n")
                break
            elif cmd == "help":
                clear_terminal()
                command_list()
   
            elif cmd == "speed-test" or cmd == "st":
                clear_terminal()
                run_speed_cli()

            elif cmd == "auto-test" or cmd == "at":
                clear_terminal()
                run_auto_test()    

            elif cmd == "status" or cmd == "stts":
                clear_terminal()
                internet_stat()

            elif cmd == "compare-global" or cmd == "cg":
                clear_terminal()
                compare_global()

            elif cmd == "signal" or cmd == "sgnl":
                clear_terminal()
                signal_qulty()

            elif cmd == "isp":
                clear_terminal()
                isp_info() 

            elif cmd == "url-info" or cmd == "url":
                clear_terminal()
                url_info()

            elif cmd == "table-history" or cmd == "th":
                clear_terminal()
                show_table()

            elif cmd == "graph-history" or cmd == "gh": 
                clear_terminal()   
                show_graph()

            elif cmd == "export" or cmd == "xprt":
                clear_terminal()
                export_logs()

            elif cmd == "delet" or cmd == "dlt":
                clear_terminal()
                delet_data()

            else:
                print(Fore.RED + "❌ Unknown command." + Style.RESET_ALL + "Type 'help' to see available options.")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting TB-NetMon CLI. See you!\n")
            break


# ====================== Tools ================ #

# Running animation
def spinner(message, running_flag):
    i = 0
    dots = ["⏳", "⏳.", "⏳..", "⏳...", "⏳...."]
    while running_flag[0]:  # using list for mutability
        sys.stdout.write(f"\r-- {message} {dots[i % len(dots)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.6)

# Clear the terminal
def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Check if digit or float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Gives thye filter date range 
def filter_date():

    print(Fore.CYAN + "\n🕓 Choose the test history range:\n" + Style.RESET_ALL)
    print("  1️⃣  Last 24 Hours")
    print("  2️⃣  Last 7 Days")
    print("  3️⃣  Last 30 Days")
    print("  4️⃣  Show All Data\n")

    choice = input(Fore.YELLOW + "⏱️  Enter your choice (1–4) >> " + Style.RESET_ALL).strip()
    print("")  # Spacer line
    
    range_type = None

    if choice == "1":
        range_type = "24h"
    elif choice == "2":
        range_type = "7d"
    elif choice == "3":
        range_type = "30d"
    else:
        range_type = "all"
    
    return range_type

# ====================== Dashboard Components ================ #
def show_dashboard():
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    hostname = socket.gethostname()
    version = "v1.0.0"

    print(Style.BRIGHT + Fore.CYAN + "\n" + "═" * 70)
    print(Fore.MAGENTA + "📡  TB-NetMon CLI – Your Network Monitoring Assistant".center(70))
    print(Fore.CYAN + "═" * 70 + Style.RESET_ALL)

    print(Fore.LIGHTBLACK_EX + f"🖥️  Host: {hostname}    📅  {now}     🧩 Version: {version}" + Style.RESET_ALL)
    # show commands 
    command_list()
    
    print(Fore.CYAN + "\n💡 Tip: Type " + Style.BRIGHT + "'help'" + Style.NORMAL + " at any time to redisplay this dashboard.")
    print("════════════════════════════════════════════════════════════════════\n" + Style.RESET_ALL)

def command_list():
    print(Fore.YELLOW + "\n🧭  Available Commands:\n")

    print(Fore.GREEN + "  speed-test      / st   " + Fore.WHITE + "- Run network speed test")
    print(Fore.GREEN + "  auto-test       / at   " + Fore.WHITE + "- Run automatic speed tests every X seconds")
    print(Fore.GREEN + "  status          / stts " + Fore.WHITE + "- Live internet status")
    print(Fore.GREEN + "  compare-global  / cg   " + Fore.WHITE + "- Compare your speed to global average")
    print(Fore.GREEN + "  signal          / sgnl " + Fore.WHITE + "- Wi-Fi strength + troubleshooting tips")
    print(Fore.GREEN + "  isp                    " + Fore.WHITE + "- Show ISP & location info")
    print(Fore.GREEN + "  url-info        / url  " + Fore.WHITE + "- Get info about a website or URL")
    print(Fore.GREEN + "  table-history   / th   " + Fore.WHITE + "- Show past results in a table")
    print(Fore.GREEN + "  graph-history   / gh   " + Fore.WHITE + "- Show past results as graph")
    print(Fore.GREEN + "  export          / xprt " + Fore.WHITE + "- Export logs to PDF")
    print(Fore.GREEN + "  delet           / dlt  " + Fore.WHITE + "- Delete all saved test history")
    print(Fore.GREEN + "  exit or Ctrl+C  / xt   " + Fore.WHITE + "- Exit the application")

# ====================== Feature Callers ================ #

def run_speed_cli():

    print(Fore.MAGENTA + "\n🚀 TB-NetMon: Internet Speed Test.\n" \
                        "═════════════════════════════════════════════\n" + Style.RESET_ALL)
    
    running = [True]
    thread = threading.Thread(target=spinner, args=("⚡ Testing Internet Speed", running))

    try:
        thread.start()
        results = check_speed()
    finally:
        running[0] = False
        thread.join()

        print()  # Add spacing

        if "Error" in results:
            print(Fore.RED + "\n❌ Failed to run the speed test!" + Style.RESET_ALL)
            print(Fore.YELLOW + f"\nError: {results['Error']}\n" + Style.RESET_ALL)
        else:
            print(Fore.MAGENTA + "\n📡 TB-NetMon Speed Report\n" \
                            "════════════════════════════════════" + Style.RESET_ALL)
            print(f"📥  Download Speed : {Fore.GREEN}{results['Download']} Mbps{Style.RESET_ALL}")
            print(f"📤  Upload Speed   : {Fore.GREEN}{results['Upload']} Mbps{Style.RESET_ALL}")
            print(f"📶  Ping           : {Fore.GREEN}{results['Ping']} ms{Style.RESET_ALL}")
            print(Fore.MAGENTA + "════════════════════════════════════" + Style.RESET_ALL)

            # Add helpful tip
            print(Fore.BLUE + "\n💡 Tip: Type 'compare-global' to check how your speed compares to the global average." + Style.RESET_ALL)

def run_auto_test():
    print(Fore.MAGENTA + "\n📡 TB-NetMon: Auto Speed Testing & Alerts\n" \
          "══════════════════════════════════════════════════════════════\n" + Style.RESET_ALL)
    print(Fore.CYAN + "⚙️  Configure thresholds and test interval below:\n" + Style.RESET_ALL)

    download_threshold = input("⬇️  Download Threshold (Mbps): ")
    upload_threshold = input("⬆️  Upload Threshold (Mbps): ")
    ping_threshold = input("📶 Ping Threshold (ms): ")
    time_interval = input("⏲️  Test Every (Seconds): ")

    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
          "ℹ Press Ctrl+C anytime to stop Auto Testing." + Style.RESET_ALL)

    # Validate input
    if not time_interval.isdigit():
        print(Fore.RED + "\n❌ Invalid ⏲ Time Interval! Please enter a number." + Style.RESET_ALL)
        return

    if not is_float(download_threshold):
        print(Fore.RED + "\n❌ Invalid ⬇ Download Threshold! Must be a number." + Style.RESET_ALL)
        return

    if not is_float(upload_threshold):
        print(Fore.RED + "\n❌ Invalid ⬆ Upload Threshold! Must be a number." + Style.RESET_ALL)
        return

    if not is_float(ping_threshold):
        print(Fore.RED + "\n❌ Invalid 📶 Ping Threshold! Must be a number." + Style.RESET_ALL)
        return

    print(Fore.GREEN + "\n✅ Auto Speed Test Started! Monitoring Every " + time_interval + "s 🔄" + Style.RESET_ALL)
    auto_tst_alert(
                    int(time_interval),
                    float(download_threshold),
                    float(upload_threshold),
                    float(ping_threshold)
                    )

def internet_stat():
    try:
        while True:
            internet_data = check_internet()
            internet_status = internet_data["net_status"]
            trblshoting_suggs = internet_data["suggests"]

            clear_terminal()  # clears the terminal before updating 

            print(Fore.MAGENTA + "\n🌐 TB-NetMon: Live Internet Monitor")
            print("════════════════════════════════════" + Style.RESET_ALL)

            print(f"{Fore.CYAN}📶 Internet Status: {Style.RESET_ALL}{internet_status}")

            print("\n" + Fore.YELLOW + "🛠️  Troubleshooting Suggestions:" + Style.RESET_ALL)
            print(f"\n{Fore.LIGHTWHITE_EX}{trblshoting_suggs}{Style.RESET_ALL}")

            print(Fore.MAGENTA + "\n════════════════════════════════════" + Style.RESET_ALL)
            print(Fore.CYAN + "ℹ Press Ctrl+C to quit this live view.\n" + Style.RESET_ALL)

            time.sleep(10)

    except KeyboardInterrupt:
        print(Fore.RED + "\n\n↩ Exiting Live Internet Monitor.\n" + Style.RESET_ALL)

def compare_global():
    print(Fore.MAGENTA + "\n🌍 TB-NetMon: Compare to Global Average\n" \
                        "═════════════════════════════════════════════" + Style.RESET_ALL)

    try:
        running = [True]
        thread = threading.Thread(target=spinner, args=("Comparing Your Speed to Global Averages", running))
        thread.start()

        results = check_speed()
        time.sleep(2)  

        global_comparison = get_compareson()

        if "No Speed Test Data Was Given" in global_comparison:
            print(Fore.RED + "\n⚠️  Failed to retrieve your speed data." + Style.RESET_ALL)
            return
        elif "No Global Speed Data Was Given!" in global_comparison:
            print(Fore.RED + "\n⚠️  Failed to retrieve global average data." + Style.RESET_ALL)
            return
        else:
            down_compare, avg_down_sped, up_compare, avg_up_sped, ping_compare, avg_ping = global_comparison

    finally:
        running[0] = False
        thread.join()

        if "Error" in results:
            print(Fore.RED + "\n❌ Speed Test Failed!\n" + Style.RESET_ALL, results["Error"])
        else:
            print(Fore.CYAN + "\n\n📊 Results Summary\n" \
                  "────────────────────────────────────────────" + Style.RESET_ALL)

            print(f"📥 Your Download: {Fore.MAGENTA}{results['Download']} Mbps{Style.RESET_ALL}")
            print(f"🌍 Country Avg  : {Fore.YELLOW}{avg_down_sped} Mbps{Style.RESET_ALL}")
            print(f"📌 Comparison   : {Fore.LIGHTWHITE_EX}{down_compare}{Style.RESET_ALL}\n")

            print(f"📤 Your Upload  : {Fore.MAGENTA}{results['Upload']} Mbps{Style.RESET_ALL}")
            print(f"🌍 Country Avg  : {Fore.YELLOW}{avg_up_sped} Mbps{Style.RESET_ALL}")
            print(f"📌 Comparison   : {Fore.LIGHTWHITE_EX}{up_compare}{Style.RESET_ALL}\n")

            print(f"📶 Your Ping    : {Fore.MAGENTA}{results['Ping']} ms{Style.RESET_ALL}")
            print(f"🌍 Country Avg  : {Fore.YELLOW}{avg_ping} ms{Style.RESET_ALL}")
            print(f"📌 Comparison   : {Fore.LIGHTWHITE_EX}{ping_compare}{Style.RESET_ALL}\n")

            print(Fore.MAGENTA + "\n═════════════════════════════════════════════\n" + Style.RESET_ALL)

def signal_qulty():

    print(Fore.MAGENTA + "\n📡 TB-NetMon: Wi-Fi Signal Strength Detector\n" \
                            "═════════════════════════════════════════════" + Style.RESET_ALL)
    
    try:
        while True:
            check = check_Wifi_quality()  

            clear_terminal()  

            print(Fore.CYAN + "\n📶 Live Wi-Fi Signal Quality Monitor\n" \
                  "────────────────────────────────────────────" + Style.RESET_ALL)

            print(Fore.LIGHTWHITE_EX + check + Style.RESET_ALL)

            print(Fore.CYAN + "\n────────────────────────────────────────────\n" \
                  "ℹ Press Ctrl+C to stop monitoring." + Style.RESET_ALL)

            time.sleep(20)

    except KeyboardInterrupt:
        print(Fore.RED + "\n\n↩ Exited Wi-Fi Signal Quality Monitoring.\n" + Style.RESET_ALL)

def isp_info():
    print(Fore.MAGENTA + "\n🌍 TB-NetMon: ISP & Location Information\n" \
                        "════════════════════════════════════════════════" + Style.RESET_ALL)

    running = [True]
    thread = threading.Thread(target=spinner, args=("Fetching ISP & Location Data", running))

    try:
        thread.start()
        info = get_ISPndLoc_info()
        if "Error" in info:
            error = info["Error"]
            message = info["Message"]
            print(Fore.RED + f"\n❌ {message}\n {error}" + Style.RESET_ALL)


    finally:
        running[0] = False
        thread.join()
        
        # if there is an error, stop with return 
        if error:
            return

        print(Fore.CYAN + "\n\n📍 Your Current Network Location & ISP Info\n" \
                             "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)

        print(f"{Fore.YELLOW}🔸 Public IP Address:       {Style.RESET_ALL}{Fore.GREEN}{info['IP']}")
        print(f"{Fore.YELLOW}🏙️  City:                   {Style.RESET_ALL}{Fore.GREEN}{info['City']}")
        print(f"{Fore.YELLOW}🗺️  Region:                 {Style.RESET_ALL}{Fore.GREEN}{info['Region']}")
        print(f"{Fore.YELLOW}🌐 Country:                {Style.RESET_ALL}{Fore.GREEN}{info['Country_cli']}")
        print(f"{Fore.YELLOW}🏣 Postal Code:            {Style.RESET_ALL}{Fore.GREEN}{info['Postal']}")
        print(f"{Fore.YELLOW}🕓 Time Zone:              {Style.RESET_ALL}{Fore.GREEN}{info['TimeZone']}")
        print(f"{Fore.YELLOW}📡 ISP Provider:           {Style.RESET_ALL}{Fore.MAGENTA}{info['ISP']}")

        print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" + Style.RESET_ALL)

def url_info():
    print(Fore.CYAN + "\n🌐🔍 WEBSITE CHECKER TOOL\n" \
                "═════════════════════════════════════════════" + Style.RESET_ALL)

    while True:

        print(Fore.CYAN + "ℹ Enter a full URL like https://example.com\n" \
                        "🟦 Type 'q' and press Enter to quit.\n\n" + Style.RESET_ALL)
        
        url = input(Fore.YELLOW + "Enter the Website/URL >> " + Style.RESET_ALL).lower().strip()

        if url == "q":
            print(Fore.RED + "\n↩ Exiting Website Checker!\n" + Style.RESET_ALL)
            break
        
        else:
            try:            
                running = [True]
                thread = threading.Thread(target=spinner, args=("Checking URL Status", running)) 
                thread.start()

                data = check_website_stat(url) 
                err_messge = "❌ No Internet, Please Check Your Connection"


            except KeyboardInterrupt:
                print(Fore.RED + "\n↩ Exiting Website Checker!\n" + Style.RESET_ALL)
                break
            except Exception as er:
                print(Fore.RED + f"⚠️  An error occurred: {er}\n" + Style.RESET_ALL)
                continue       

            finally:
                running[0] = False       
                thread.join()

                if err_messge in data:
                    print(f"\n {err_messge}")
                    return

                print(Fore.CYAN + "\n\n🔎 Website Report\n" \
                    "──────────────────────────────────────────────\n" + Style.RESET_ALL)
                if data["domain_info"] is None: # Check if there was an error 
                        
                        print(f"{Fore.GREEN}📶 Status: {Style.RESET_ALL}\n{data['status']}")
                else:
                    # Status
                    print(f"{Fore.GREEN}📶 Status: {Style.RESET_ALL}\n{data['status']}")
                    print(f"{Fore.BLUE}⏱️  Response Time: {Style.RESET_ALL}{round(data['response_time'], 2)} seconds\n")

                    # Meta Info
                    print(f"{Fore.YELLOW}📄 Title: {Style.RESET_ALL}\n{data['meta_title']}\n")
                    print(f"{Fore.YELLOW}📝 Meta Description: {Style.RESET_ALL}\n{data['meta_description']}\n")
                    print(f"{Fore.YELLOW}🔷 Domain Info: {Style.RESET_ALL}\n")
                    print(f"{Fore.LIGHTWHITE_EX}{data['domain_info']}{Style.RESET_ALL}\n")

                    # SSL
                    print(f"{Fore.MAGENTA}🔐 SSL Status: {Style.RESET_ALL}{data['ssl_status']}")

                    # IP Info
                    print(f"{Fore.CYAN}🌐 Server IP: {Style.RESET_ALL}{data['server_ip']}")

                    # Ping Info
                    print(Fore.GREEN + "\n📡 Ping Results:" + Style.RESET_ALL)
                    for line in data["ping"]:
                        print(f"   {Fore.LIGHTWHITE_EX}{line}{Style.RESET_ALL}")
                        time.sleep(0.4)  # nice delay

                print(Fore.CYAN + "═════════════════════════════════════════════\n" + Style.RESET_ALL)

def show_table():
    print(Fore.MAGENTA + "\n📅 NetMon: View Past Speed Test Logs in Table\n" \
                "══════════════════════════════════════════════════════════════" + Style.RESET_ALL)

    range_type = filter_date()
    
    # Call backend table rendering function
    tst_hstry_table(range_type)

    print(Fore.CYAN + "\n💡 Additional Options:\n" \
            "  📥 Type 'export' or 'xprt' to export logs as a PDF report\n" \
            "  ❌ Type 'delet' or 'dlt' to delete stored history\n" + Style.RESET_ALL)

def show_graph():
    print(Fore.MAGENTA + "\n📈 TB-NetMon: View Past Speed Test Logs in Graph\n" \
                    "══════════════════════════════════════════════════════════════" + Style.RESET_ALL)

    range_type = filter_date()

    # Call backend graph rendering function
    tst_hstry_graph(range_type)

    print(Fore.CYAN + "\n💡 Additional Options:\n" \
            "  📥 Type 'export' or 'xprt' to export logs as a PDF report\n" \
            "  ❌ Type 'delet' or 'dlt' to delete stored history\n" + Style.RESET_ALL)

def export_logs():

    range_type = filter_date()
    filename = input(Fore.YELLOW + "⬜ Enter a Name for this PDF >> " + Style.RESET_ALL).strip()
    print("")
    result = export_tst_logs(range_type, filename + '.pdf')
    
    print(Fore.GREEN + result + Style.RESET_ALL)

def delet_data():
    print (Fore.YELLOW + "⚠ Warnig All Your Speed tests History Will Be Deleted❗" + Style.RESET_ALL)
    while True:
        ask = input(Fore.CYAN + "🔶 Do you Confirm Deleting❓ y = Yes / n = No ---> " + Style.RESET_ALL).lower().strip()
        if ask == "y" or ask == "yes":
            delet_rsults()
            print(Fore.MAGENTA + "\nHistory Data is Deleted❗\n" + Style.RESET_ALL)
            break
        elif ask == "n" or ask == "no":
            print(Fore.GREEN + "\nData is Alive✅\n" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\n❎ Invalid Command❕\n" + Style.RESET_ALL)    

if __name__ == "__main__":
    creat_table()
    run_cli()
