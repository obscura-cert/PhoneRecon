import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from phonenumbers.phonenumberutil import number_type, NumberParseException
import requests
import sys

def country_flag(iso):
    return ''.join(chr(127397 + ord(c)) for c in iso.upper()) if iso else "🏳️"

def analyze_number(raw_number):
    print("\n📞 Analyzing Phone Number:", raw_number)
    try:
        number = phonenumbers.parse(raw_number)
    except NumberParseException:
        print("❌ Invalid phone number format.")
        sys.exit(1)

    # BASIC INFO
    is_valid = phonenumbers.is_valid_number(number)
    is_possible = phonenumbers.is_possible_number(number)
    iso = phonenumbers.region_code_for_number(number)
    print("\n📌 BASIC DETAILS")
    print("✔️ Valid Number:", is_valid)
    print("📏 Possible Number:", is_possible)
    print("🔢 Number Length:", len(str(number.national_number)))
    print("🔤 Country Code:", number.country_code)

    # REGION / OPERATOR
    print("\n🌍 REGION & CARRIER INFO")
    print("🌎 ISO Region:", iso)
    print("🚩 Country Flag:", country_flag(iso))
    print("📍 Region (Geo):", geocoder.description_for_number(number, "en"))
    print("📡 Carrier:", carrier.name_for_number(number, "en"))

    # LINE TYPE
    type_map = {
        0: "Fixed Line", 1: "Mobile", 2: "Fixed or Mobile", 3: "Toll Free",
        4: "Premium Rate", 5: "Shared Cost", 6: "VoIP", 7: "Personal",
        8: "Pager", 9: "UAN", 10: "Voicemail"
    }
    print("🕹️ Number Type:", type_map.get(number_type(number), "Unknown"))

    # TIMEZONES
    print("\n⏱️ TIMEZONE INFORMATION")
    for tz in timezone.time_zones_for_number(number):
        print("🕰️ Timezone:", tz)

    # FORMATS
    print("\n🧮 NUMBER FORMATS")
    print("🔢 E.164 Format:", phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164))
    print("🌐 International Format:", phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
    print("🏠 National Format:", phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL))
    print("🧷 RFC3966 Format:", phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.RFC3966))
    print("🔢 Raw National Number:", number.national_number)

    # ADVANCED CHECKS
    print("\n🔍 ADVANCED VALIDITY CHECKS")
    print("📦 Is Possible Short Number:", phonenumbers.is_possible_short_number(number))
    print("📦 Is Valid For Region:", phonenumbers.is_valid_number_for_region(number, iso))
    print("📦 Is Possible For Region & Type:", phonenumbers.is_possible_number_for_type(number, number_type(number)))

    # GOOGLE DORKS
    print("\n🔗 GOOGLE DORKS FOR INVESTIGATION")
    forks = [
        "facebook.com", "instagram.com", "linkedin.com", "pastebin.com", "telegram.me OR t.me",
        "twitter.com", "github.com", "reddit.com", "tiktok.com", "truecaller.com",
        "youtube.com", "amazon.in", "medium.com", "quora.com", "flipkart.com",
        "snapchat.com", "cash.app", "docdroid.net", "archive.org", "scamadviser.com"
    ]
    for site in forks:
        dork = f'"{raw_number}" site:{site}'
        print("🔎", "https://www.google.com/search?q=" + requests.utils.quote(dork))

if __name__ == "__main__":
    raw_input = input("📱 Enter phone number (with +country code): ")
    analyze_number(raw_input.strip())
