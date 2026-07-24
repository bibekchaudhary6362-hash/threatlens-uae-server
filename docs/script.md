# Script: Live Critical CVE Feed

## What it does
This Python script pulls newly published CRITICAL severity vulnerabilities
(CVSS v3 score 9.0+) from the NVD (National Vulnerability Database) public
API, covering the last 7 days, and generates a live HTML briefing page
displayed on the ThreatLens UAE site. This directly supports the site's
purpose of giving UAE security teams up-to-date threat intelligence.

## How it works
1. Queries the NVD REST API (https://services.nvd.nist.gov/rest/json/cves/2.0)
   filtered by CRITICAL severity and a 7-day publish window
2. Parses each CVE result to extract the ID, publish date, CVSS score,
   and description
3. Renders the results into a styled HTML table matching the site theme
4. Writes the output to /var/www/html/threat-feed.html

## Automation
The script runs automatically every 6 hours via cron:
0 */6 * * * /usr/bin/python3 /home/azureuser/threatlens-uae-server/scripts/cve_feed.py

## Verifiable output
Live output: https://threatlensuae.xyz/threat-feed.html

## Reference
NVD API documentation: https://nvd.nist.gov/developers/vulnerabilities
