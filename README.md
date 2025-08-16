# Mega IP Intelligence Tool (v7.0)

An extremely fast, concurrent IP analysis tool that aggregates data from over 50 keyless and API-key based public sources into logical categories.

![Tool Preview](./Screenshot_20250816-205928_Termux.png)

## 🔥 Key Features | المميزات الأساسية

-   **Massive Data Aggregation:** Gathers data from over 50+ keyless and API-key based APIs and aggregates it intelligently, avoiding repetitive reports.
-   **High-Speed & Concurrent:** Uses multi-threading to query all sources simultaneously, delivering results in seconds, not minutes.
-   **Intelligent Reporting:** Instead of one panel per API, data is grouped into logical categories:
    -   **Geolocation Comparison:** Compares location data from multiple sources.
    -   **ISP & ASN Information:** Summarizes provider and network data.
    -   **Network & Routing (BGP/RDAP):** Provides advanced data about BGP prefixes and modern RDAP registration details.
    -   **Security & Threat Intel:** Integrates open-source threat intelligence feeds.
-   **Rich & Clean Output:** Uses the `rich` library for beautiful, readable tables and panels.
-   **Automatic Dependency Check:** Installs required libraries on first run.

## 🚀 Getting Started | البدء السريع

**1. Clone the Repository | ١. نسخ المستودع**

```bash
git clone https://github.com/Hmza1112617/IP-Intelligence-Tool.git
```

**2. Navigate to the Directory | ٢. الدخول إلى المجلد**

```bash
cd IP-Intelligence-Tool
```

**3. Run the Tool | ٣. تشغيل الأداة**

```bash
# For interactive mode
python ip_info.py

# To analyze an IP directly
python ip_info.py 8.8.8.8
```

---
## Credits

Telegram: @DRR_R2 - @phpandpy
