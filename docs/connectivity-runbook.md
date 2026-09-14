# Connectivity investigation runbook

Use only on systems and networks you administer. Commands below inspect state; they do not change network configuration. Their output may contain private addresses, names, and logs—sanitize it before sharing.

## 1. Establish scope

Record symptom, time, affected client/network, last known good state, and recent changes. Try a second authorized client. Distinguish name resolution failure, connection refusal, timeout, TLS failure, and application error.

## 2. Physical link and host addressing

```sh
ip -br link
ip -br addr
ip route
```

If link is down, inspect cable/transceiver, negotiated link, and switch port before modifying routes. Check DHCP/static-address consistency and the expected gateway. A link-up state alone does not prove correct VLAN membership.

## 3. Route and policy

```sh
ip route get 192.0.2.10
```

192.0.2.10 is a documentation address: replace it with an authorized destination. Confirm selected interface and route. Check switch tagging, gateway routing, and firewall counters/logs. A timeout can be a dropped packet, unavailable host, or return-path failure; it is not proof of a firewall fault. Do not disable the firewall as a first diagnostic step.

## 4. DNS and transport

```sh
getent ahosts example.com
curl --connect-timeout 3 --max-time 10 --head https://example.com/
```

Replace the example with the intended service. Compare resolution with known intended records; do not assume ping support. Separate TCP failure from TLS and HTTP status failures. A 405 response to HEAD can mean that the route requires GET, not that the host is down.

## 5. Host and application

```sh
ss -ltn
systemctl --failed --no-pager
systemctl status example.service --no-pager
journalctl -u example.service -n 50 --no-pager
```

`example.service` is a placeholder. For a user unit, add `--user` to systemctl/journalctl as appropriate. Check bind address, port, unit exit status, and logs. Compare a bounded local HTTP request with the same service through its intended network path.

## 6. Recovery and verification

Change only the failing layer after collecting evidence. Re-run the original client request and relevant negative/allowed tests. Record before/after observations, exact change, rollback, and remaining uncertainty. Do not label a successful restart as proof that the root cause is fixed.
