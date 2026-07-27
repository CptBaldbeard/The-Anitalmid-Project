---
title: "Security Analyst (SOC)"
created: 2026-07-26
source: "Camufox Web Search + Industry Research"
related_roles:
  - "[[SOC Analyst]]"
  - "[[Incident Responder]]"
  - "[[Threat Hunter]]"
  - "[[Security Engineer]]"
  - "[[GRC Analyst]]"
birkman_area: "[[Computer & Mathematical Science]]"
birkman_colors:
  - "[[analyzer - yellow]]"
  - "[[thinker - blue]]"
tags:
  - role-profile
  - cybersecurity
  - soc
  - incident-response
skills:
  core:
    - "SIEM monitoring and alert triage (Splunk, Microsoft Sentinel, Chronicle, Elastic)"
    - "Log analysis across endpoints, network, cloud, and identity sources"
    - "Security incident classification, investigation, and escalation (triage process)"
    - "Understanding of the cyber kill chain, MITRE ATT&CK framework, and common TTPs"
    - "Endpoint Detection and Response (EDR) — CrowdStrike, Microsoft Defender for Endpoint, SentinelOne"
    - "Network traffic analysis and packet inspection (Wireshark, Zeek, Suricata)"
    - "Email security — phishing analysis, SPF/DKIM/DMARC, email gateway investigation"
  specialized:
    - "Threat intelligence consumption and IOC enrichment (VirusTotal, AlienVault OTX, MISP)"
    - "Digital forensics and evidence collection (chain of custody, disk imaging, memory analysis)"
    - "Malware analysis (static and dynamic, sandboxing)"
    - "Kusto Query Language (KQL) — essential for Microsoft Sentinel environments"
    - "Cloud security monitoring (AWS GuardDuty, Azure Defender for Cloud, GCP Security Command Center)"
    - "Incident response playbook development and tabletop exercise facilitation"
  soft:
    - "Pattern recognition and anomaly detection mindset"
    - "Calm under pressure during active incidents"
    - "Clear written and verbal communication — incident reports, executive summaries, postmortems"
    - "Detail-oriented investigation without tunnel vision"
    - "Cross-team collaboration (IT, legal, HR, PR during major incidents)"
certifications:
  entry_level:
    - "CompTIA Security+"
    - "CompTIA CySA+ (Cybersecurity Analyst)"
    - "Microsoft Certified: Security, Compliance, and Identity Fundamentals (SC-900)"
  professional:
    - "GIAC Certified Incident Handler (GCIH)"
    - "GIAC Certified Forensic Analyst (GCFA)"
    - "Certified SOC Analyst (CSA) — EC-Council"
    - "Microsoft Certified: Security Operations Analyst Associate (SC-200)"
    - "Certified Ethical Hacker (CEH)"
  advanced:
    - "CISSP (Certified Information Systems Security Professional)"
    - "GIAC Certified Detection Analyst (GCDA)"
    - "GIAC Reverse Engineering Malware (GREM)"
    - "OSCP (Offensive Security Certified Professional)"
tools:
  primary:
    - "SIEM (Splunk / Microsoft Sentinel / Chronicle)"
    - "EDR (CrowdStrike Falcon / Microsoft Defender for Endpoint)"
    - "SOAR (Splunk Phantom / Microsoft Sentinel automation)"
    - "Ticketing (Jira Service Management / ServiceNow)"
    - "Threat Intel Platforms (VirusTotal, MISP, AlienVault OTX)"
  secondary:
    - "Wireshark / tcpdump / Network Watcher"
    - "PowerShell / Python for automation"
    - "Volatility (memory forensics)"
    - "Autopsy / FTK Imager (disk forensics)"
    - "Any.Run / Joe Sandbox (malware analysis)"
    - "Azure Sentinel / Defender for Cloud"
salary_data:
  entry_level:
    range: "$55,000 - $75,000"
    title: "SOC Analyst Tier 1 / Junior Security Analyst"
    experience: "0-2 years"
  mid_level:
    range: "$80,000 - $110,000"
    title: "SOC Analyst Tier 2 / Security Analyst"
    experience: "3-5 years"
  senior:
    range: "$110,000 - $150,000"
    title: "Senior SOC Analyst / Incident Response Lead / Tier 3"
    experience: "6-10 years"
  source: "Glassdoor, Payscale, CyberSeek, BLS (2025)"
  region: "United States"
career_progression:
  - level: "Tier 1 — SOC Analyst (0-2 yrs)"
    role: "IT Support / Help Desk → Tier 1 SOC Analyst"
    growth_signals: "Security+ certification, SIEM alert triage, ability to follow runbooks, basic log analysis"
  - level: "Tier 2 — Security Analyst (2-5 yrs)"
    role: "Tier 1 → Tier 2 Security Analyst"
    growth_signals: "CySA+ or GCIH, independent incident investigation, EDR deep-dive, phishing campaign analysis, basic threat hunting"
  - level: "Tier 3 — Senior SOC Analyst (5-8 yrs)"
    role: "Tier 2 → Tier 3 / Incident Response Lead"
    growth_signals: "CISSP or GCFA, leading major incidents, developing detection rules, mentoring Tier 1/2, forensic investigation"
  - level: "Lead / Manager (8-12 yrs)"
    role: "Tier 3 → SOC Manager / Security Operations Lead"
    growth_signals: "Team leadership, SOC tooling strategy, metrics and KPIs, budget ownership, CISO reporting"
  - level: "Director / CISO Track (12+ yrs)"
    role: "SOC Manager → Director of Security Operations / CISO"
    growth_signals: "Enterprise security strategy, board-level communication, compliance integration"
responsibilities:
  - "Monitor SIEM dashboards and alerts for indicators of compromise and policy violations"
  - "Triage security alerts from EDR, firewall, IDS/IPS, email gateway, and cloud security tools"
  - "Investigate phishing reports — analyze email headers, attachments, and URLs; remediate malicious campaigns"
  - "Perform initial incident scoping: determine affected systems, data exposure, and attacker TTPs"
  - "Escalate confirmed incidents to Tier 2/3 analysts and incident response teams with detailed handoff notes"
  - "Execute incident response playbooks for common scenarios (ransomware, BEC, credential compromise)"
  - "Collect and preserve forensic evidence — logs, memory dumps, disk images — maintaining chain of custody"
  - "Analyze malware samples through sandboxing and static analysis; extract IOCs for blocking"
  - "Tune SIEM detection rules to reduce false positives and improve alert fidelity"
  - "Conduct proactive threat hunting — query SIEM for adversary behaviors not caught by existing alerts"
  - "Document all investigation steps, findings, and remediation actions in ticketing system"
  - "Write post-incident reports and executive summaries for leadership consumption"
  - "Stay current with emerging threats — follow threat intel feeds, security blogs, and CVE announcements"
  - "Participate in 24x7 on-call rotation for security incident response"
  - "Support compliance audits by producing evidence of security monitoring and incident response processes"
aptitude_signals:
  strong_match:
    - "Yellow Analyzer dominance — SOC work is systematic, process-driven, and rule-based; triaging alerts follows defined playbooks and requires methodical attention to detail"
    - "Investigating strength — Birkman explicitly identifies 'research or trouble-shooting capacity' as Dan's top strength; security investigation is the purest expression of this"
    - "Scientific interest (92%) — hypothesis-driven investigation: 'What caused this alert? Is this a true positive? What attacker technique is being used?'"
    - "Ambiguity handling strength — alerts are often incomplete or noisy; distinguishing signal from noise without full context is core SOC work"
    - "Structured thinking strength — consistent alert triage, evidence collection, and investigation methodology require rigorous structure"
    - "[[Career History/Information_Systems_Specialist]] — directly adjacent: monitors and responds to security alerts, investigates suspicious activity as first-level responder, CJIS compliance, endpoint protection across 200+ devices"
    - "Written word strength — incident reports, investigation summaries, and postmortems demand clear, precise technical writing"
    - "Reflective efficiency — Dan's pattern of making efficient use of energy maps to tuning alerts and automating repetitive triage tasks (SOAR)"
  development_areas:
    - "Yellow stress rigidity — active incidents are the definition of high-stress, rapid-change environments; Dan's tendency to become rule-bound and resist change under stress could impair creative incident response when playbooks don't cover the scenario"
    - "Low Persuasive interest (32%) — Tier 3 and Lead roles increasingly involve stakeholder communication, briefing executives during incidents, and advocating for security investment; pure analyst roles avoid this, but career growth requires communication upward"
    - "On-call and 24x7 operations — SOC roles typically involve shift work or on-call rotation with night/weekend coverage; Dan's need for uninterrupted concentration and structured schedules may cause friction"
    - "Low Social Service interest (21%) — while SOC is technical, Tier 1 roles involve significant interaction with end users reporting phishing or odd behavior; this diminishes at Tier 2+"
    - "Alert fatigue risk — repetitive false-positive triage is administrative in nature and could drain Dan if not balanced with deeper investigation work"
adjacent_roles:
  - "[[GRC Analyst]] — moves from reactive security to proactive governance and compliance"
  - "[[Security Engineer]] — builds and tunes detection infrastructure rather than operating it"
  - "[[Incident Responder]] — specialized role focused exclusively on major incidents, forensics, and remediation"
  - "[[Threat Hunter]] — proactive hypothesis-driven hunting without the alert triage queue"
  - "[[Information Systems Specialist]] — Dan's current role; broader IT with security as a component"
---
# Security Analyst (SOC) — Role Profile

## Overview

The Security Operations Center (SOC) Analyst is the front line of cyber defense — monitoring, triaging, investigating, and responding to security alerts across an organization's digital environment. Working within a SIEM and EDR toolset, the SOC Analyst identifies malicious activity, scopes incidents, and initiates response. This role is a **strong alternative path** for Dan: it directly extends his security monitoring and alert response work as an [[Career History/Information_Systems_Specialist|Information Systems Specialist]] into a dedicated cybersecurity career.

## Why This Role Matters

Cyberattacks are escalating in frequency and sophistication — the 2024 IBM Cost of a Data Breach report pegged the average breach cost at $4.88 million. Every organization handling sensitive data (government, healthcare, finance, education) needs SOC analysts. The cybersecurity workforce gap exceeds 3.5 million unfilled positions globally (ISC², 2025). SOC Analyst is the most common entry point into cybersecurity, with the highest volume of open positions and the clearest tiered progression path in the field.

## Day in the Life

| Time | Activity |
|------|----------|
| 07:00 | Shift handoff from overnight analyst — review open investigations, critical alerts, and ongoing incidents |
| 07:30 | Triage new SIEM alerts from overnight: sort false positives, queue true positives for investigation |
| 09:00 | Deep-dive investigation of suspicious PowerShell execution alert — correlate with EDR telemetry and network logs |
| 10:30 | Phishing campaign detected: analyze sample emails, extract IOCs, block sender domains, initiate user notifications |
| 12:00 | Write investigation report for confirmed malware incident; document IOCs and remediation steps |
| 13:00 | Threat hunting block: query SIEM for C2 beaconing patterns using known threat intel indicators |
| 14:00 | Tune detection rule that generated too many false positives — adjust threshold and add exclusion filters |
| 15:00 | Attend red team/blue team debrief — share detection gaps found during latest exercise |
| 16:00 | Review and update incident response playbook based on lessons learned from recent incident |
| 16:45 | Prepare shift handoff summary for oncoming analyst |

## Search Sources

- Camufox Web Search: "SOC analyst security analyst core skills responsibilities" (2026-07-26)
- Camufox Web Search: "CompTIA Security+ CySA+ CISSP security analyst certification path" (2026-07-26)
- Camufox Web Search: "SOC analyst security analyst salary United States 2025" (2026-07-26)
- Camufox Web Search: "SOC analyst tools technologies SIEM Splunk Sentinel CrowdStrike EDR" (2026-07-26)
- Camufox Web Search: "security analyst SOC career progression path tier 1 tier 2 tier 3" (2026-07-26)
- Camufox Web Search: "day in the life SOC analyst security operations center" (2026-07-26)

## Related Vault Content

- [[Dan Bechtel Birkman Profile]]
- [[Top_Career_Areas_to_Explore]]
- [[Career History/Information_Systems_Specialist]] — active security monitoring, CJIS compliance, endpoint protection
- [[Career History/Technical_Writer]] — GRC and compliance documentation (ISO 27001, SOC2, data privacy)
- [[Career History/Vandal_Card_Specialist_and_IT_Help_Desk_Technician]] — security access management, identity lifecycle
- [[Role Profiles/Systems Administrator]] — adjacent: security administration as component of sysadmin work
- [[Role Profiles/Cloud Administrator (Azure)]] — cloud security monitoring cross-over
- [[Role Profiles/GRC Analyst]] — compliance side of the security spectrum
- [[Birkman Method Overview]]
