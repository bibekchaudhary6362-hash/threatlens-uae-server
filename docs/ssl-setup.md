
## Troubleshooting: HTTPS not accessible after certificate issued
After Certbot issued the certificate, https://threatlensuae.xyz initially timed out.
Cause: Azure's Network Security Group (NSG) had inbound rules for HTTP (80) and
SSH (22) but not HTTPS (443), so all HTTPS traffic was blocked by the default
DenyAllInBound rule.

Fix: Added an inbound NSG rule to allow port 443.
- Destination port ranges: 443
- Protocol: TCP
- Action: Allow
- Priority: 310
- Name: HTTPS

After adding this rule, https://threatlensuae.xyz loaded correctly.
