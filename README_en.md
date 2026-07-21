# Lab Dashboard — School Computer Lab Monitoring System

> Real-time dashboard for monitoring the status of a school computer lab's machines, built with Firebase/Firestore and Python.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Firebase](https://img.shields.io/badge/firebase-firestore-orange)

---

## About the project

This project came from a real need at my workplace: I manage a computer lab with 13 machines, and I needed a fast, visual way to know which ones were online, offline, or having issues — without manually checking each one.

The system consists of:
- A **web dashboard** (`index.html`) that displays real-time status for each PC, powered by Firebase/Firestore
- A **Python script** (`ping_agent.py`) that runs periodically, checks connectivity for each machine, and updates its status in the database

## Screenshots

### Dashboard overview

<img width="1361" height="766" alt="dashboard" src="https://github.com/user-attachments/assets/d925482f-0510-43cc-8820-b5e627e8ab7e" />

The main panel shows the total number of machines, how many are working, under maintenance, or unavailable, plus search filters and export options (Excel/PDF).

### Card detail (online vs offline)

<img width="661" height="182" alt="cards" src="https://github.com/user-attachments/assets/0bf3c17a-7919-466e-9bc0-98d0e8f94930" />

Each card shows technical details of the machine (CPU, RAM, storage), current IP, status, and the last update timestamp.

## My role in this project (transparency)

I want to be transparent about how this project was built, because I think that's more valuable than appearing to be something it's not:

- **I identified the problem** and defined the requirements: monitor 13 machines, real-time status, solve it through a web interface
- **I made the technical architecture decisions**: choosing Firebase/Firestore, deciding to migrate from static IP to hostname-based pinging (after diagnosing that DHCP-assigned IPs were breaking the ping system)
- **I tested and validated everything in the real environment** of the lab, including network troubleshooting (ICMPv4 firewall rules, hostname resolution)
- **I made the design decisions** (cyber teal/navy palette, typography, visual behavior)
- Since my programming skill level is still basic, **I used AI assistance (Claude/Anthropic) to implement the code**, reviewing, testing, and adjusting every part in my own environment

I'm actively studying programming, Python, SQL, and cybersecurity to keep growing my ability to build this kind of solution more independently over time.

## Technical problem solved

One of the most interesting challenges in this project: the lab PCs received dynamic IPs via DHCP, which constantly broke the ping system (the IP saved in the database would go stale).

**Solution:** I migrated the ping logic to use **hostname-based pinging** (`ping -4 LABXX`) instead of static IPs. The agent tries the hostname first; if it doesn't respond, it falls back to the last known IP, and automatically updates Firestore whenever it detects a new IP — without overwriting the other fields in the record.

### The agent in action

<img width="738" height="496" alt="ping_agent" src="https://github.com/user-attachments/assets/b3edf592-f28a-4a89-9e40-25f660656b9f" />

Notice PC-07: the agent detected that the IP had changed (`10.0.10.231 → 10.0.4.159`) and automatically updated it in the database. PCs 03, 04, 11, and 12 didn't respond via hostname, so the agent tried the old saved IP as a fallback before marking them offline.

## Tech stack

- **Frontend:** HTML, CSS (custom variables), JavaScript
- **Backend/Data:** Firebase / Firestore
- **Automation:** Python (`ping_agent.py`)
- **Infrastructure:** Hostname resolution, Windows firewall rules (ICMPv4)

## How it works

1. `ping_agent.py` runs periodically and checks connectivity for each PC (PC-01 to PC-13) via hostname
2. If the hostname doesn't respond, it falls back to the last known IP
3. The result (online/offline + current IP) is saved to Firestore, without overwriting other fields
4. `index.html` consumes this data in real time and displays status, with animations and visual badges
5. An optional field allows manually overriding the hostname for non-standard machines

## Contact

Feel free to reach out if you have questions about this project or want to discuss IT/cybersecurity topics.
