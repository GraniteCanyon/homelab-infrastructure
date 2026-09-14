# INC-001 — Public service unavailable while recovery loops

**DisData · May 2026 · historical, sanitized case study**

Source: the expanded incident section and technical evidence notes on the [public portfolio](https://portfolio.disdata.info/#incident-dns), reviewed September 14, 2026. This was AI-assisted project maintenance, not a claim of unaided enterprise incident response. No raw host logs or deployment identifiers are published.

## Symptom

The public dashboard became unavailable and the host could not be reached over SSH. Availability logs showed repeated tunnel restarts during the outage.

## Scope

The investigation covered the local Python application, public HTTPS path, Cloudflare Tunnel, host networking, SSH, and the previous boot. Public failure and SSH unreachability suggested a wider scope than one application route.

## Evidence

The recorded investigation compared local and public health, reviewed tunnel and network logs, checked SSH, and examined prior-boot memory, disk, and shutdown evidence. Tunnel logs recorded DNS lookup failures; other network services reported unreachable routes. The journal ended abruptly before a new boot. The investigation found no evidence that an application crash or out-of-memory event caused this outage.

## Root cause — known and unresolved

DNS/network connectivity was unhealthy, and the watchdog's repeated tunnel restarts did not repair that dependency. The underlying network failure and unclean shutdown were **not conclusively traced to a single device or power event**. This case does not claim a proven cable, VLAN, gateway, or power-supply fault.

## Correction

Recovery was changed to distinguish local from public failures. Defaults require two failed local checks before application recovery, or three public failures before tunnel recovery. The tunnel has a 15-minute cooldown. Boot grace, route/DNS checks, and a lock prevent unnecessary or overlapping attempts. A separate boot-recovery script waits for network readiness before public-service recovery.

## Verification

The portfolio's recorded evidence review checked recovery scripts and enabled timers; local and public health endpoints returned HTTP 200 and recent watchdog logs recorded successful availability checks. These are historical validation observations from the cited review, not new measurements made for this file.

They demonstrate health at the time of review—not a controlled replay of the outage or a guarantee of recovery after power loss. The [current validation session](../validation-results.md) is separately dated and narrowly scoped.

## Lesson learned

A public endpoint is the end of a dependency chain. Check the failing layer before restarting components, bound recovery frequency, and retain uncertainty when evidence does not establish the initiating cause.
