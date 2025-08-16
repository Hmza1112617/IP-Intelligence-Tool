
import sys
import socket
import ipaddress
import subprocess
import re
from datetime import datetime

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

console = Console()

def get_basic_info(ip_obj):
    return {"status": "success", "data": {
        "IP Address": str(ip_obj),
        "Version": f"IPv{ip_obj.version}",
        "Type": "Private" if ip_obj.is_private else "Public",
        "Is Loopback": ip_obj.is_loopback,
        "Is Global": ip_obj.is_global,
        "Reverse Pointer": ip_obj.reverse_pointer
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
        obj = IPWhois(ip_str)
        return {"status": "success", "data": obj.lookup_whois(get_referral=True)}
    except Exception as e:
        return {"status": "error", "data": str(e)}

def get_dns_data(ip_str):
    try:
        rev_name = reversename.from_address(ip_str)
        ptr = str(resolver.resolve(rev_name, "PTR")[0])
        return {"status": "success", "data": {"ptr": ptr}}
    except Exception:
        return {"status": "error", "data": {"ptr": "No PTR record found."}}

def generate_table(title, result):
    if result['status'] == 'error':
        return Panel(Text(str(result['data']), style="bold red"), title=f"[ 🚨 ] {title}", border_style="red")
    
    table = Table(box=None, show_header=False)
    table.add_column(style="bold magenta", width=25)
    table.add_column(style="white")
    
    data_content = result['data']
    if not data_content:
        return Panel(Text("No data returned from source.", style="yellow"), title=f"[ 🟡 ] {title}", border_style="yellow")

    if title != "WHOIS Records":
        for k, v in data_content.items():
            if isinstance(v, (dict, list)):
                continue
            table.add_row(str(k).replace('_', ' ').title(), str(v))
    else:
        table.add_row("ASN", f'{data_content.get('asn', 'N/A')} - {data_content.get('asn_description', 'N/A')}')
        table.add_row("ASN CIDR", data_content.get('asn_cidr', 'N/A'))
        for i, net in enumerate(data_content.get('nets', [])):
            table.add_row(f"Net #{i+1} Name", net.get('name'))
            table.add_row(f"Net #{i+1} Range", net.get('range'))
            table.add_row(f"Net #{i+1} Desc", net.get('description', 'N/A').replace('\n', ' '))

    return Panel(table, title=f"[ 🌐 ] {title}", border_style="blue")

def main():
    console.print(Panel("Ultimate IP Intelligence Tool - v3.3 (Final Keyless Edition)", style="bold magenta"))
    
    ip_to_check = ""
    if len(sys.argv) > 1:
        ip_to_check = sys.argv[1]
    else:
        ip_to_check = console.input(Text("\nEnter IP Address to analyze: ", style="bold yellow"))

    sanitized_ip = re.sub(r'[^0-9a-fA-F.:/]', '', ip_to_check).strip()
    if not sanitized_ip:
        console.print("[bold red]Invalid input after sanitization. Exiting.[/bold red]")
        return

    try:
        ip_obj = ipaddress.ip_address(sanitized_ip)
    except ValueError:
        console.print(f"[bold red]'{sanitized_ip}' is not a valid IP address.[/bold red]")
        return

    if ip_obj.is_private:
        console.print(generate_table("Basic Information", get_basic_info(ip_obj)))
        console.print("[yellow]Private IP addresses do not have public records.[/yellow]")
        return

    API_SOURCES = {
        "Geolocation (ip-api.com)": f"http://ip-api.com/json/{sanitized_ip}?fields=61439",
        "ASN/Company (ipinfo.io)": f"https://ipinfo.io/{sanitized_ip}/json",
        "Geolocation (freegeoip.app)": f"https://freegeoip.app/json/{sanitized_ip}",
        "Geolocation (ipapi.co)": f"https://ipapi.co/{sanitized_ip}/json/",
        "Connection Details (ipwho.is)": f"http://ipwho.is/{sanitized_ip}",
    }

    all_data = {}
    
    with Live(console=console, screen=False, auto_refresh=True, vertical_overflow="visible") as live:
        live.update(Text("Gathering initial data..."))
        all_data["Basic Information"] = get_basic_info(ip_obj)
        all_data["DNS Records"] = get_dns_data(sanitized_ip)

        for title, url in API_SOURCES.items():
            live.update(f"Querying [bold yellow]{title}[/bold yellow]...")
            all_data[title] = fetch_json_api(url)
        
        live.update(Text("Querying WHOIS databases (can be slow)..."))
        all_data["WHOIS Records"] = get_whois_data(sanitized_ip)
        live.update(Text("All data gathered. Rendering report..."))

    console.clear()
    console.print(Panel(f"Intelligence Report for [bold yellow]{sanitized_ip}[/bold yellow]", style="bold magenta"))
    for title, data in all_data.items():
        console.print(generate_table(title, data))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Process interrupted by user. Goodbye![/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected critical error occurred: {e}[/bold red]")
