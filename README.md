# ThreatLens UAE — Cyber Threat Intelligence Platform

**Live Server:** https://threatlensuae.xyz
**IP Address:** 135.235.217.244
**Student:** Bibek Chaudhary Tharu
**Student ID:** 35581249
**Unit:** ICT171 — Introduction to Server Environments and Architectures

---

## Overview

ThreatLens UAE is a cyber threat intelligence briefing platform for organisations
and security professionals across the UAE and Gulf region. It runs as a
multi-purpose Infrastructure-as-a-Service deployment on Microsoft Azure,
combining a manually installed WordPress site, a live automated vulnerability
feed, and a VPN-restricted administrative backend.

## Architecture

| Component | Technology | Purpose |
|---|---|---|
| Web Server | Apache2 + PHP + MySQL | Hosts the WordPress site |
| CMS | WordPress (manual install) | Site content and structure |
| Data Feed | Python 3 + NVD API | Live critical CVE briefings |
| Automation | cron | Refreshes the feed every 6 hours |
| Security | Let's Encrypt (Certbot) | HTTPS/TLS |
| Access Control | WireGuard VPN | Restricts /wp-admin to VPN clients only |
| Version Control | Git / GitHub | Documentation and change history |

## Documentation

- [DNS Setup](docs/dns-setup.md)
- [SSL/TLS Setup](docs/ssl-setup.md)
- [Website Setup (WordPress)](docs/website-setup.md)
- [VPN Setup and Integration](docs/vpn-setup.md)
- [Script Documentation](docs/script.md)

## Live Verification

- Site: https://threatlensuae.xyz
- Live CVE Feed: https://threatlensuae.xyz/threat-feed.html
- Admin panel (VPN-restricted, returns 403 without VPN): https://threatlensuae.xyz/wp-admin

## Video Explainer

[Video link here]

## References

Each documentation file in `/docs` lists the specific external references used
(Azure documentation, Certbot, WireGuard, NVD API) for that component.
