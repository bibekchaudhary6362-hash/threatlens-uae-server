#!/usr/bin/env python3
"""
ThreatLens UAE - Critical CVE Feed Generator
----------------------------------------------
Pulls newly published CRITICAL severity CVEs (CVSS v3 >= 9.0) from the
NVD (National Vulnerability Database) public API for the last 7 days,
and generates a static HTML briefing page for the ThreatLens UAE site.

Author: Bibek Chaudhary Tharu
Student ID: 35581249
Unit: ICT171 - Assignment 3

Usage:
    python3 cve_feed.py

Runs automatically every 6 hours via cron (see docs/script.md).
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone

# --- Configuration ---
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
OUTPUT_FILE = "/var/www/html/threat-feed.html"
DAYS_BACK = 7
MAX_RESULTS = 15


def build_query_url():
    """Builds the NVD API request URL for critical CVEs published in the
    last DAYS_BACK days."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=DAYS_BACK)

    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "cvssV3Severity": "CRITICAL",
        "resultsPerPage": MAX_RESULTS,
    }
    return f"{NVD_API_URL}?{urllib.parse.urlencode(params)}"


def fetch_cves():
    """Fetches CVE data from the NVD API and returns the parsed JSON."""
    url = build_query_url()
    request = urllib.request.Request(url, headers={"User-Agent": "ThreatLensUAE/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode())


def extract_summary(cve_item):
    """Pulls the ID, description, CVSS score and published date out of a
    single NVD API CVE record."""
    cve = cve_item["cve"]
    cve_id = cve["id"]
    published = cve["published"][:10]

    description = next(
        (d["value"] for d in cve["descriptions"] if d["lang"] == "en"),
        "No description available."
    )

    score = "N/A"
    metrics = cve.get("metrics", {})
    if "cvssMetricV31" in metrics:
        score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
    elif "cvssMetricV30" in metrics:
        score = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]

    return {
        "id": cve_id,
        "published": published,
        "score": score,
        "description": description,
    }


def generate_html(cve_list):
    """Renders the CVE summaries into a styled HTML fragment matching the
    ThreatLens UAE site theme."""
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    rows = ""
    for item in cve_list:
        rows += f"""
        <tr>
            <td><a href="https://nvd.nist.gov/vuln/detail/{item['id']}" target="_blank">{item['id']}</a></td>
            <td>{item['published']}</td>
            <td class="severity-critical">{item['score']}</td>
            <td>{item['description'][:220]}...</td>
        </tr>"""

    if not rows:
        rows = "<tr><td colspan='4'>No new critical CVEs found in the last 7 days.</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ThreatLens UAE - Live Critical CVE Feed</title>
<style>
    body {{ font-family: Arial, sans-serif; background:#0b1526; color:#eaeaea; margin:2rem; }}
    h1 {{ color:#d4af37; }}
    table {{ width:100%; border-collapse: collapse; margin-top:1rem; }}
    th, td {{ border:1px solid #3c4a5e; padding:8px; text-align:left; vertical-align:top; }}
    th {{ background:#13233d; color:#fff; }}
    .severity-critical {{ color:#ff6b6b; font-weight:bold; }}
    .updated {{ color:#9fb3c8; font-size:0.9rem; margin-bottom:1rem; }}
</style>
</head>
<body>
    <h1>Live Critical CVE Feed</h1>
    <p class="updated">Auto-generated from the NVD API. Last updated: {generated_at}</p>
    <table>
        <tr><th>CVE ID</th><th>Published</th><th>CVSS Score</th><th>Description</th></tr>
        {rows}
    </table>
</body>
</html>"""
    return html


def main():
    try:
        data = fetch_cves()
        cve_items = data.get("vulnerabilities", [])
        summaries = [extract_summary(item) for item in cve_items]
        html = generate_html(summaries)

        with open(OUTPUT_FILE, "w") as f:
            f.write(html)

        print(f"Success: wrote {len(summaries)} CVEs to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error generating CVE feed: {e}")


if __name__ == "__main__":
    main()
