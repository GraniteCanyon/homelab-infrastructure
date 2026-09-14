# Logical topology and trust boundaries

The portfolio describes a UDM-SE feeding a core switch with VLAN 10 (management), 20 (servers), 30 (clients), and 40 (IoT). Proxmox, NAS storage, Linux hosts, and DGX Spark are part of the infrastructure; their exact placement is not published.

## Intent versus evidence

Segmentation provides separate broadcast domains. Inter-VLAN isolation still depends on configured routing and firewall policy. This repository does not contain a verified ACL export. The policy worksheet is a proposed review baseline, not a representation of every live rule.

Management should be a deliberately constrained administrative path. Client-to-service access should be limited to the required ports. IoT-to-management access is a useful negative test. Record the source network, destination role, protocol, expected decision, actual decision, and evidence for every validation.

## Service paths

Public DisData requests pass through Cloudflare Tunnel to a Linux-hosted Python application with SQLite storage. Collection and serving are separate operational concerns. A private AI service has another path: LAN client → Docker-exposed service → inference runtime on DGX Spark. Successful localhost access is not proof of either end-to-end path.

## Deliberate omissions

No addressing plan, device serial numbers, switch ports, administrative URLs, tunnel identifiers, or backup locations are published. Use a private inventory for those details. The diagram is downloadable as source in the repository README; it is not a physical wiring diagram.
