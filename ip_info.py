
# ======================================================================================
#  Advanced IP Intelligence Tool - v5.0 (Auto-Update Edition)
#  Author: Python & Networking Expert
#  Description: A comprehensive tool to gather and report IP data, with self-updating.
# ======================================================================================

import sys
import socket
import ipaddress
import subprocess
import re
from datetime import datetime

# --- Version & Update Configuration ---
CURRENT_VERSION = "v5.0"
REPO_URL = "https://raw.githubusercontent.com/Hmza1112617/IP-Intelligence-Tool/main/ip_info.py"

# --- Dependency Check & Auto-Installation ---
try:
    import requests
    from ipwhois import IPWhois
    from dns import reversename, resolver
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.live import Live
except ImportError:
    print("\n[!] Some required libraries are missing. Attempting to install them now...")
    required_packages = ['requests', 'ipwhois', 'dnspython', 'rich']
    try:
        for package in required_packages:
            print(f"--- Installing {package} ---")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("\n[+] Libraries installed successfully! Please restart the script.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\n[x] Failed to install libraries. Error: {e}")
        print("Please try installing them manually: pip install requests ipwhois dnspython rich")
    sys.exit()

# --- TELEGRAM BOT CONFIGURATION ---
TELEGRAM_BOT_TOKEN = ""  # Paste your bot token here
TELEGRAM_CHAT_ID = ""    # Paste your chat ID here

console = Console()

def check_for_updates():
    console.print(f"[cyan]Current version: {CURRENT_VERSION}. Checking for updates...[/cyan]")
    try:
        response = requests.get(REPO_URL, timeout=5)
        response.raise_for_status()
        remote_code = response.text
        match = re.search(r'CURRENT_VERSION\s*=\s*"(v[^"]+)'', remote_code)
        if not match:
            return

        remote_version = match.group(1)
        if remote_version != CURRENT_VERSION:
            console.print(f"\n[bold yellow]A new version ({remote_version}) is available![/bold yellow]")
            if console.input("Do you want to update now? (y/n): ").lower() in ['y', 'yes']:
                console.print("Updating...", style="green")
                try:
                    with open(sys.argv[0], 'w', encoding='utf-8') as f:
                        f.write(remote_code)
                    console.print("Update successful! Please restart the script.", style="bold green")
                    sys.exit()
                except Exception as e:
                    console.print(f"[bold red]Update failed: {e}[/bold red]")
                    sys.exit()
            else:
                console.print("Update skipped.", style="yellow")
        else:
            console.print("[green]You are on the latest version.[/green]")
    except Exception:
        console.print("[yellow]Could not check for updates.[/yellow]", highlight=False)

def get_basic_info(ip_obj):
    return {"status": "success", "data": {
        "IP Address": str(ip_obj), "Version": f"IPv{ip_obj.version}",
        "Type": "Private" if ip_obj.is_private else "Public",
        "Is Global": ip_obj.is_global, "Reverse Pointer": ip_obj.reverse_pointer
    }}

def fetch_json_api(url):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return {"status": "success", "data": r.json()}
    except Exception as e:
        return {"status": "error", "data": str(e)}

def get_whois_data(ip_str):
    try:
        return {"status": "success", "data": IPWhois(ip_str).lookup_whois(get_referral=True)}
    except Exception as e:
        return {"status": "error", "data": str(e)}

def get_dns_data(ip_str):
    try:
        rev_name = reversename.from_address(ip_str)
        ptr = str(resolver.resolve(rev_name, "PTR")[0])
        return {"status": "success", "data": {"ptr": ptr}}
    except Exception:
        return {"status": "error", "data": {"ptr": "No PTR record found."}}

def display_console_report(ip_str, all_data):
    console.clear()
    console.print(Panel(f"Intelligence Report for [bold yellow]{ip_str}[/bold yellow]", style="bold magenta"))
    # ... (display logic is complex, assuming it's correct)

def send_telegram_report(ip_str, all_data):
    # ... (telegram logic is complex, assuming it's correct)
    pass

def main():
    check_for_updates()
    console.print(Panel(f"Ultimate IP Intelligence Tool - {CURRENT_VERSION}", style="bold magenta"))
    # ... (rest of main logic)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Process interrupted by user.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected critical error occurred: {e}[/bold red]")
