# IP Intelligence Tool

A powerful, console-based IP intelligence tool written in Python. This script gathers extensive information about any given IP address from multiple public, keyless sources and presents it in a clean, human-readable format using the `rich` library.

## Features

-   **Comprehensive Data:** Gathers information from 6 different keyless sources:
    -   `ip-api.com` (Geolocation)
    -   `ipinfo.io` (ASN/Company Details)
    -   `freegeoip.app` (Alternative Geolocation)
    -   `ipapi.co` (Alternative Geolocation)
    -   `ipwho.is` (Connection Details)
    -   Public WHOIS servers (Registration Data)
-   **Rich & Clean Output:** Uses the `rich` library to display data in beautifully formatted panels and tables.
-   **No API Keys Required:** Works entirely on public, keyless APIs.
-   **Automatic Dependency Check:** Automatically detects and installs missing Python libraries (`requests`, `rich`, `ipwhois`, `dnspython`) on first run.
-   **Robust Input Handling:** Sanitizes input to prevent errors from hidden or invalid characters.
-   **Flexible Usage:** Can be run interactively or by passing an IP address as a command-line argument.

## Usage

1.  Clone the repository.
2.  Run the script from your terminal:

    ```bash
    # For interactive mode
    python ip_info.py

    # To analyze an IP directly
    python ip_info.py 8.8.8.8
    ```

---
## Credits

Telegram: @DRR_R2 - @phpandpy
