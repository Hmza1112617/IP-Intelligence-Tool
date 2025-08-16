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

# أداة استخبارات IP

أداة قوية لاستخبارات عناوين IP تعمل من سطر الأوامر، مكتوبة بلغة بايثون. تقوم هذه الأداة بجمع معلومات شاملة عن أي عنوان IP من عدة مصادر عامة لا تتطلب مفتاح API، وتقدمها في شكل منظم وواضح باستخدام مكتبة `rich`.

## المميزات

-   **بيانات شاملة:** تجمع المعلومات من 6 مصادر مختلفة لا تتطلب مفتاح API.
-   **عرض جذاب وواضح:** تستخدم مكتبة `rich` لعرض البيانات في جداول ومنسقة.
-   **لا تتطلب مفاتيح API:** تعمل بشكل كامل على مصادر البيانات العامة.
-   **فحص تلقائي للمكتبات:** تقوم بتثبيت المكتبات الناقصة تلقائياً عند أول تشغيل.
-   **معالجة قوية للمدخلات:** تقوم بتنظيف المدخلات لمنع الأخطاء الناتجة عن المحارف الخفية.
-   **استخدام مرن:** يمكن تشغيلها بشكل تفاعلي أو عبر تمرير الـ IP كمدخل لسطر الأوامر.

## طريقة الاستخدام

1.  قم بنسخ المستودع.
2.  شغل السكريبت من خلال الـ terminal:

    ```bash
    # للوضع التفاعلي
    python ip_info.py

    # لتحليل IP مباشرة
    python ip_info.py 8.8.8.8
    ```

---
## Credits

Telegram: @DRR_R2 - @phpandpy
