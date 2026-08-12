# Port-Scanner (synx)

A TCP port scanner built from the ground up in Python — raw sockets, manually packed IP/TCP headers, and asyncio for concurrency. No Scapy, no third-party packet libraries. Includes `synx`, a custom interactive shell for running scans.

## Features

- **Raw packet construction** — IP and TCP headers are built by hand with `struct.pack`, including proper checksum calculation (IP header checksum + TCP checksum via pseudo-header)
- **Four scan types**:
  - `synscan` — standard SYN scan (half-open scan, checks for SYN-ACK)
  - `finscan` — FIN scan (stealth scan, relies on RST from closed ports)
  - `nullscan` — NULL scan (no flags set)
  - `xmascan` — XMAS scan (URG + PSH + FIN set)
- **Async scanning** — ports are probed concurrently via `asyncio`, each on its own raw socket, with a per-port timeout
- **`synx` shell** — a custom `cmd.Cmd`-based interactive shell for running scans without re-invoking Python each time

## Project structure

```
.
├── tcp_scan.py      # Packet class — header construction, checksums, packet generation
├── port_scanner.py  # ScanPort class — scan orchestration, async dispatch, result files
└── synx.py          # Interactive shell (synx) — CLI front-end for port_scanner
```

## Requirements

- Python 3
- Linux (raw sockets with `IP_HDRINCL` are used, which is a POSIX/Linux-style raw socket API)
- Root/administrator privileges (raw sockets require elevated permissions)

## Usage

Launch the shell with elevated privileges:

```bash
sudo python3 synx.py
```

From the `synx >` prompt, run a scan with the `-p` flag to specify a port range:

```
synx > synscan -p 1000 9000
synx > finscan -p 1 1024
synx > nullscan -p 8000 8100
synx > xmascan -p 20 100
```

Other shell commands:

```
synx > clear     # clear the terminal
synx > quit      # exit the shell (alias: exit)
```

Each scan writes its results to disk in the working directory:

- `Every_Port_Status.txt` — full open/closed breakdown (SYN scans only)
- `open_port.txt` — ports reported as open (or filtered, where applicable) for the scan just run

The shell automatically prints `open_port.txt` back to the terminal after each scan completes.

## How the scans differ

| Scan | Flags sent | Signal for "closed" | Signal for "open" |
|---|---|---|---|
| SYN | SYN | RST or no SYN-ACK | SYN-ACK |
| FIN | FIN | RST | No response |
| NULL | (none) | RST | No response |
| XMAS | URG, PSH, FIN | RST | No response |

FIN, NULL, and XMAS scans can't distinguish an open port from one silently dropped by a firewall — both look like "no response." They exist as variants of each other mainly for firewall/IDS evasion, since some filtering rules are written around specific flag patterns rather than full connection-state tracking. They're also unreliable against non-RFC-793-compliant stacks (e.g. Windows, which sends RST regardless of port state).

## Disclaimer

This tool sends raw, hand-crafted packets and is intended for educational use and scanning systems you own or have explicit authorization to test. Port scanning systems you don't have permission to test may violate laws or terms of service depending on your jurisdiction and the target's policies.
