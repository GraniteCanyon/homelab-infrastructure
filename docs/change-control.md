# Change and recovery checklist

This is an operating template, not a completed production change record.

## Before

- State the symptom or intended improvement and the affected dependencies.
- Save the current configuration privately and confirm administrative recovery access.
- Record a baseline from the actual client network, not only localhost.
- Define a bounded maintenance window, success test, and rollback trigger.
- Change one layer at a time; do not combine addressing, firewall, and application changes.

## During

- Keep a timestamped private record of commands and observations.
- Protect the management path before applying network policy changes.
- Stop if the evidence contradicts the diagnosis.

## After

- Test expected allowed paths and expected denied paths from appropriate clients.
- Check logs and dependency health; verify that restart loops did not appear.
- Verify persistence separately when reboot survival is part of the change.
- Record unresolved findings. A backup is not verified until a restore has been exercised.
- Publish only a sanitized summary, not raw logs or secrets.

## Evidence record

| Field | Fill during a real change |
| --- | --- |
| Symptom / expected behavior | |
| Scope and dependencies | |
| Before evidence | |
| Change | |
| After evidence | |
| Rollback condition and result | |
| Remaining uncertainty | |
