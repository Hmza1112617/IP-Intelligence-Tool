
# ======================================================================================
#  Advanced IP Intelligence Tool - v5.1 (Stable)
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
CURRENT_VERSION = "v5.1"
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
        match = re.search(r'CURRENT_VERSION\s*=\s*"(v[^"]+)"', remote_code)
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
    for title, result in all_data.items():
        if result['status'] == 'error':
            panel = Panel(Text(str(result['data']), style="bold red"), title=f"[ 🚨 ] {title}", border_style="red")
        else:
            table = Table(box=None, show_header=False)
            table.add_column(style="bold magenta", width=25)
            table.add_column(style="white")
            data_content = result['data']
            if not data_content: 
                panel = Panel(Text("No data returned.", style="yellow"), title=f"[ 🟡 ] {title}")
            elif title != "WHOIS Records":
                for k, v in data_content.items():
                    if not isinstance(v, (dict, list)): table.add_row(str(k).replace('_', ' ').title(), str(v))
                panel = Panel(table, title=f"[ 🌐 ] {title}", border_style="blue")
            else:
                table.add_row("ASN", f"{data_content.get('asn', 'N/A')} - {data_content.get('asn_description', 'N/A')}")
                for i, net in enumerate(data_content.get('nets', [])):
                    table.add_row(f"Net #{i+1} Name", net.get('name'))
                    table.add_row(f"Net #{i+1} Desc", net.get('description', 'N/A').replace('\n', ' '))
                panel = Panel(table, title=f"[ 🌐 ] {title}", border_style="blue")
        console.print(panel)

def send_telegram_report(ip_str, all_data):
    console.print("\nFormatting and sending report to Telegram...")
    message = f"*IP Intelligence Report for:* `{ip_str}`\n\n"
    for title, result in all_data.items():
        message += f"*-- {title} --*\n"
        if result['status'] == 'success' and result['data']:
            for k, v in result['data'].items():
                if not isinstance(v, (dict, list)) and v:
                    message += f"- *{str(k).replace('_', ' ').title()}:* `{str(v)}`\n"
        else:
            message += "- No data or an error occurred.\n"
        message += "\n"
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            console.print(f"[bold red]Failed to send Telegram message. Response: {response.text}[/bold red]")
        else:
            console.print("[green]✔️ Text report sent successfully.[/green]")
    except Exception as e:
        console.print(f"[bold red]Error sending Telegram message: {e}[/bold red]")
    geo_data = all_data.get("Geolocation (ip-api.com)", {}).get('data', {})
    if geo_data and geo_data.get('lat') and geo_data.get('lon'):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendLocation"
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'latitude': geo_data['lat'], 'longitude': geo_data['lon']}
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                console.print("[green]✔️ Location map sent successfully.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error sending location: {e}[/bold red]")

def main():
    check_for_updates()
    console.print(Panel(f"Ultimate IP Intelligence Tool - {CURRENT_VERSION}", style="bold magenta"))
    ip_to_check = sys.argv[1] if len(sys.argv) > 1 else console.input(Text("\nEnter IP Address to analyze: ", style="bold yellow"))
    sanitized_ip = re.sub(r'[^0-9a-fA-F.:/]', '', ip_to_check).strip()
    if not sanitized_ip: return console.print("[bold red]Invalid input. Exiting.[/bold red]")

    try:
        ip_obj = ipaddress.ip_address(sanitized_ip)
    except ValueError:
        return console.print(f"[bold red]'{sanitized_ip}' is not a valid IP address.[/bold red]")

    if ip_obj.is_private:
        display_console_report(sanitized_ip, {"Basic Information": get_basic_info(ip_obj)})
        return

    output_mode = 'console'
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        if len(sys.argv) < 2:
            choice = console.input("\n[bold yellow]How to deliver the report?\n[1] Display on screen\n[2] Send to Telegram\nEnter choice (1 or 2): [/bold yellow]").strip()
            if choice == '2':
                output_mode = 'telegram'

    API_SOURCES = {
        "Geolocation (ip-api.com)": f"http://ip-api.com/json/{sanitized_ip}?fields=61439",
        "ASN/Company (ipinfo.io)": f"https://ipinfo.io/{sanitized_ip}/json",
        "Connection Details (ipwho.is)": f"http://ipwho.is/{sanitized_ip}",
    }
    all_data = {}
    with Live(console=console, screen=False, auto_refresh=True) as live:
        live.update("Gathering initial data...")
        all_data["Basic Information"] = get_basic_info(ip_obj)
        all_data["DNS Records"] = get_dns_data(sanitized_ip)
        for title, url in API_SOURCES.items():
            live.update(f"Querying [bold yellow]{title}[/bold yellow]...")
            all_data[title] = fetch_json_api(url)
        live.update("Querying WHOIS databases...")
        all_data["WHOIS Records"] = get_whois_data(sanitized_ip)
        live.update("All data gathered.")

    if output_mode == 'console':
        display_console_report(sanitized_ip, all_data)
    elif output_mode == 'telegram':
        send_telegram_report(sanitized_ip, all_data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Process interrupted by user.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected critical error occurred: {e}[/bold red]")
