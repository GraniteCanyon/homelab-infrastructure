# Adding a TP-Link SG2428LP to my UniFi homelab

I added a TP-Link SG2428LP to my UniFi setup so I could expand the number of ports in the lab without changing the rest of the network.

My setup still uses UniFi for routing, DHCP, firewall rules, and VLAN gateways. The TP-Link is managed through Omada and is basically being used as a Layer-2 switch.

The VLAN layout is:

- VLAN 10 — Management
- VLAN 20 — Servers
- VLAN 30 — Clients
- VLAN 40 — IoT

I’m leaving out live IP addresses, exact switch ports, credentials, and management URLs.

## What went wrong

At first, the switch was connected over SFP.

Pretty quickly, devices behind the TP-Link started dropping in and out. UniFi was showing a few different warnings:

- `STP State Flapping`
- `Port Link Flapping`
- `Receive SFP Signal Loss`

The devices connected to the TP-Link would show up for a few seconds, disappear, and then come back again.

I also had a Raspberry Pi show up in Omada on the wrong network with the wrong IP address.

At first this looked like a VLAN or STP problem, but the SFP warning ended up being the biggest clue.

## Troubleshooting

I started by simplifying everything as much as possible.

Instead of changing VLANs, STP settings, and port profiles all at once, I disconnected the extra devices and focused on the uplink between UniFi and the TP-Link.

The SFP connection kept throwing signal-loss and link-flapping alerts.

I moved the TP-Link over to a regular copper Ethernet uplink instead.

That immediately made the network much more stable and the STP flapping stopped.

At that point I factory-reset the SG2428LP and adopted it into Omada again from scratch.

## Rebuilding the switch

After the reset, I kept the setup simple.

UniFi stayed responsible for:

- Routing
- DHCP
- Firewall rules
- VLAN gateways

Omada and the TP-Link only handled:

- VLAN membership
- Tagged/untagged traffic
- Access-port assignments

The working layout looks like this:

```text
Internet
   |
UniFi gateway
   |
UniFi switching
   |
   | single copper trunk
   |
TP-Link SG2428LP
   |-- VLAN 20 server ports
   |-- VLAN 30 client ports
   `-- VLAN 40 IoT ports
```

The uplink carries the default network untagged and the other VLANs tagged:

```text
Default     native / untagged
VLAN 10     tagged
VLAN 20     tagged
VLAN 30     tagged
VLAN 40     tagged
```

On the UniFi side, the port allows the tagged VLANs.

On the Omada side, the uplink uses the equivalent of the `All` profile.

Normal device ports are set as access ports for whatever VLAN that device belongs to.

For example, a server port uses VLAN 20 as its native network and does not pass the other VLANs to the device.

## Raspberry Pi issue

After the reset, the Raspberry Pi was visible in Omada, but it was on the default network instead of the Servers VLAN.

Because of that, it got an IP address from the wrong DHCP scope.

The fix was just to assign that TP-Link port to VLAN 20 and let the Pi renew its address.

After that, it showed up on the correct network and was reachable again.

## What actually fixed it

The main fixes were:

- Stop using the unstable SFP uplink
- Move the switch to a regular copper Ethernet uplink
- Factory-reset the TP-Link and adopt it again in Omada
- Leave routing and DHCP on UniFi
- Recreate the VLANs in Omada as Layer-2 VLANs
- Leave the uplink as a trunk
- Assign normal device ports to the correct VLAN one at a time

Once that was done, the switch stayed online and the devices behind it stopped dropping in and out.

## What I learned

The biggest lesson was to check the physical link before assuming the problem is VLANs or STP.

The unstable SFP connection was causing secondary symptoms that looked like a switching or loop problem.

I also learned that after a switch reset, connected devices can still be online but end up on the wrong VLAN because all of the port assignments are back at their defaults.

For a mixed UniFi/Omada setup, keeping the responsibilities separate made the configuration much easier:

- UniFi handles Layer 3
- TP-Link handles Layer 2

I also found that it was much easier to fix the problem by rebuilding one piece at a time instead of changing several settings at once.

This follows the same basic approach in the [connectivity runbook](../connectivity-runbook.md): physical link first, then addressing, VLANs/routing, firewall policy, and finally the service itself.
