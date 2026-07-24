# VPN Setup and Integration

## Overview
ThreatLens UAE runs a WireGuard VPN service alongside the main website,
providing a multi-purpose server with genuine integration between components:
the VPN is used to restrict access to the WordPress admin panel, so the
public-facing site remains open while the administrative backend is only
reachable by authenticated VPN clients.

## Installation
sudo apt install wireguard -y

## Server configuration
- Server private/public keypair generated with wg genkey / wg pubkey
- Interface address: 10.8.0.1/24
- Listening port: 51820 (UDP)
- IP forwarding enabled via /etc/sysctl.conf
- NAT/forwarding rules applied via PostUp/PostDown iptables commands

## Client configuration
A client keypair was generated and registered as a peer on the server,
with a corresponding client config (client1.conf) that can be imported
into the WireGuard app to connect.

## Firewall
Azure NSG rule added:
- Port: 51820
- Protocol: UDP
- Action: Allow

## Integration with WordPress
Apache is configured so that /wp-admin and wp-login.php are only accessible
from the VPN's internal subnet (10.8.0.0/24) or localhost. This was verified
by confirming that /wp-admin returns a 403 Forbidden error over the public
internet, and is only accessible once connected via WireGuard.

## Verification
- wg show confirms the server interface and registered peer
- Public access to /wp-admin correctly returns 403 Forbidden
- Site itself (Home, Briefings, Services, Contact) remains fully accessible

## Reference
WireGuard official quickstart: https://www.wireguard.com/quickstart/
