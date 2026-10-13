#!/usr/bin/env python3
"""Guess the user's curriculum region from this computer's time zone and language settings.

Only reads settings; sends nothing anywhere. Prints JSON: the time zone, the locale, and a short list of
likely regions to OFFER the user. It is a guess, never an answer: one time zone covers several provinces
or states, so the skill always asks the user to confirm.

In the Claude app the skill runs in a cloud sandbox, so this script sees the sandbox, not the user's
computer. It reports that ("sandbox": true) and the skill just asks.

    python3 scripts/detect_region.py
"""
import json
import locale
import os
import platform
import subprocess

# IANA time zone -> regions to offer, most likely first. Canada by province (its curricula are provincial).
ZONES = {
    "America/Toronto": ["Ontario", "Quebec"],
    "America/Montreal": ["Quebec", "Ontario"],
    "America/Nipigon": ["Ontario"], "America/Thunder_Bay": ["Ontario"], "America/Iqaluit": ["Nunavut"],
    "America/Vancouver": ["British Columbia"], "America/Whitehorse": ["Yukon"],
    "America/Edmonton": ["Alberta", "Northwest Territories"], "America/Yellowknife": ["Northwest Territories"],
    "America/Regina": ["Saskatchewan"], "America/Swift_Current": ["Saskatchewan"],
    "America/Winnipeg": ["Manitoba"],
    "America/Halifax": ["Nova Scotia", "Prince Edward Island"], "America/Glace_Bay": ["Nova Scotia"],
    "America/Moncton": ["New Brunswick"], "America/St_Johns": ["Newfoundland and Labrador"],
    "America/Goose_Bay": ["Newfoundland and Labrador"],
    # United States: one zone spans many states, so offer the zone and ask for the state.
    "America/New_York": ["a US state on Eastern time (New York, Florida, Georgia, Ohio, ...)"],
    "America/Detroit": ["Michigan"], "America/Indiana/Indianapolis": ["Indiana"],
    "America/Chicago": ["a US state on Central time (Texas, Illinois, Minnesota, ...)"],
    "America/Denver": ["a US state on Mountain time (Colorado, Utah, New Mexico, ...)"],
    "America/Phoenix": ["Arizona"], "America/Boise": ["Idaho"],
    "America/Los_Angeles": ["a US state on Pacific time (California, Washington, Oregon, Nevada)"],
    "America/Anchorage": ["Alaska"], "Pacific/Honolulu": ["Hawaii"],
    # Elsewhere: national curricula, or the parts that differ.
    "Europe/London": ["England", "Scotland", "Wales", "Northern Ireland"],
    "Europe/Dublin": ["Ireland"],
    "Africa/Lagos": ["Nigeria"], "Africa/Accra": ["Ghana"], "Africa/Nairobi": ["Kenya"],
    "Africa/Johannesburg": ["South Africa"],
    "Asia/Kolkata": ["India"], "Asia/Calcutta": ["India"], "Asia/Karachi": ["Pakistan"],
    "Asia/Manila": ["Philippines"], "Asia/Singapore": ["Singapore"], "Asia/Dubai": ["United Arab Emirates"],
    "Australia/Sydney": ["New South Wales", "Australian Capital Territory"], "Australia/Melbourne": ["Victoria"],
    "Australia/Brisbane": ["Queensland"], "Australia/Perth": ["Western Australia"],
    "Australia/Adelaide": ["South Australia"], "Australia/Hobart": ["Tasmania"], "Australia/Darwin": ["Northern Territory"],
    "Pacific/Auckland": ["New Zealand"],
}
COUNTRY = {"CA": "Canada", "US": "United States", "GB": "United Kingdom", "IE": "Ireland", "AU": "Australia",
           "NZ": "New Zealand", "NG": "Nigeria", "GH": "Ghana", "KE": "Kenya", "ZA": "South Africa", "IN": "India",
           "PK": "Pakistan", "PH": "Philippines", "SG": "Singapore", "AE": "United Arab Emirates"}


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return ""


def time_zone():
    if os.environ.get("TZ") and "/" in os.environ["TZ"]:
        return os.environ["TZ"].lstrip(":")
    if platform.system() == "Windows":   # Windows names ("Eastern Standard Time") are coarse; offer, then ask
        return run(["powershell", "-NoProfile", "-Command", "(Get-TimeZone).Id"]) or run(["tzutil", "/g"])
    try:
        link = os.path.realpath("/etc/localtime")
        if "zoneinfo/" in link:
            return link.split("zoneinfo/", 1)[1]
    except OSError:
        pass
    try:
        return open("/etc/timezone").read().strip()
    except OSError:
        return run(["timedatectl", "show", "-p", "Timezone", "--value"])


def user_locale():
    if platform.system() == "Darwin":
        loc = run(["defaults", "read", "-g", "AppleLocale"])
        if loc:
            return loc
    if platform.system() == "Windows":
        loc = run(["powershell", "-NoProfile", "-Command", "(Get-Culture).Name"])
        if loc:
            return loc
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        if os.environ.get(var):
            return os.environ[var].split(".")[0]
    return (locale.getlocale()[0] or "")


def looks_like_sandbox(tz, loc):
    # Cloud sandboxes usually run on UTC with no desktop locale.
    return platform.system() == "Linux" and tz in ("", "UTC", "Etc/UTC") and loc in ("", "C", "C.UTF-8", "POSIX", "en_US")


def main():
    tz, loc = time_zone(), user_locale()
    country_code = loc.replace("-", "_").split("_")[1][:2].upper() if "_" in loc.replace("-", "_") else ""
    offer = list(ZONES.get(tz, []))
    if country_code == "CA" and loc.lower().startswith("fr") and "Quebec" in offer:   # French-Canadian settings
        offer.remove("Quebec")
        offer.insert(0, "Quebec")
    print(json.dumps({
        "time_zone": tz or None,
        "locale": loc or None,
        "country_from_locale": COUNTRY.get(country_code, country_code or None),
        "offer": offer,
        "sandbox": looks_like_sandbox(tz, loc),
        "note": "A guess from settings, not a location. Always ask the user to confirm or type their region.",
    }, indent=2))


if __name__ == "__main__":
    main()
