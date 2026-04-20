# Mirth AI Triage Copilot

AI-powered HL7 and Mirth Connect incident triage tool. Cuts interface troubleshooting time from hours to minutes.

Built by Joseph Quinn — Healthcare SaaS Integration Engineer with 2+ years production Mirth Connect 3.10+ and HL7 2.x experience.

\---

## What it does

**Tab 1 — HL7 Triage**
Paste any raw HL7 2.x message. Returns field-level breakdown, exact errors, downstream impact, and specific fix in under 60 seconds.

**Tab 2 — Mirth Analyzer**
Paste a Mirth Connect error log or channel export. Returns root cause, exact transformer/line, copy-paste JavaScript fix, and severity score.

**Tab 3 — Batch Clustering**
Upload up to 50 failed messages. Clusters failures by root cause pattern, shows top issues, and estimates total fix effort.

\---

## Setup

### Requirements

* Python 3.11+
* Anthropic API key

### Install

```powershell
cd D:\\Projects\\mirth-ai-triage
pip install fastapi uvicorn anthropic python-multipart
```

### Set API key

```powershell
$env:ANTHROPIC\_API\_KEY = "sk-ant-YOUR-KEY-HERE"
```

### Run

**Terminal 1 — Backend:**

```powershell
cd D:\\Projects\\mirth-ai-triage\\mvp\_demo
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Then open browser to:**

```
http://localhost:8001
```

\---

## Demo Script (3 minutes for Loom)

### 0:00–0:15 — Setup

* Open http://localhost:8001
* "This is Mirth AI Triage Copilot. It cuts HL7 interface troubleshooting from hours to minutes."

### 0:15–1:00 — HL7 Triage

* Click "Load broken ORU sample"
* Click "Analyze Message"
* Point out: severity score, missing OBX segment detected, exact fix shown
* "This would normally take an integration engineer 30-90 minutes to diagnose manually."

### 1:00–2:00 — Mirth Analyzer

* Switch to Mirth Analyzer tab
* Click "Load sample error log"
* Click "Analyze Error"
* Point out: channel name identified, line 47 pinpointed, JavaScript fix shown copy-paste ready
* "847 messages in the error queue. This tells you exactly what broke and exactly how to fix it."

### 2:00–2:45 — Batch Clustering

* Switch to Batch Clustering tab
* Click "Load sample batch"
* Click "Cluster \& Analyze"
* Point out: failure patterns grouped, most common root cause surfaced
* "Instead of reviewing 500 individual errors, you see the top 3 root causes in one view."

### 2:45–3:00 — Close

* "I can run a free triage on one real broken feed. Send me a log. This just saved your team 40 hours."

\---

## Outreach Message

> "I built a tool that turns broken HL7 messages and Mirth Connect errors into root-cause triage in under 2 minutes. Looking for one healthcare integration team willing to test it on a redacted sample HL7 message or error log. Send one redacted sample and I'll return a clean triage summary at no charge."

\---

## Target Titles on LinkedIn

* Director of Interoperability
* Integration Engineering Manager
* VP of Implementations
* Head of Professional Services
* Principal Integration Architect

## Target Companies

* Healthcare SaaS vendors 50-500 employees
* Digital health startups Series A/B with hospital integrations
* Lab vendors, radiology vendors, RCM companies
* Any company still on Mirth 3.x evaluating the 4.6 licensing change

\---

## Safety Notes

* Never auto-apply suggested fixes. Always require human review and sign-off.
* Redact all PHI from demo screenshots and Loom recordings.
* This tool is for research and triage assistance only, not production automation.

