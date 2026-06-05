---
name: widow-intel
description: Black Widow's intelligence tradecraft and source library. Use when assessing threat actors, mapping capabilities and intentions, identifying vulnerabilities, or filling intelligence gaps. Trigger on any request involving intelligence analysis, threat attribution, actor profiling, recon, or counterintelligence.
---

# Intelligence Tradecraft & Source Library

## Threat Actor Assessment Framework

### Actor Profiling
For any threat actor, assess across five dimensions:
1. **Capability**: what can they actually do vs. what they claim?
2. **Intent**: what do they want, and how committed are they?
3. **Resources**: funding, personnel, logistics, technical infrastructure
4. **Vulnerabilities**: what do they need that they don't have? What do they fear?
5. **Timeline**: when does their window open and close?

### Attribution Standards
- **Confirmed**: multiple independent sources, physical evidence, technical signature match
- **High confidence**: 2+ technical indicators + behavioural pattern match
- **Assessed**: single-source with strong corroboration
- **Suspected**: working hypothesis only — do not act on suspected attribution alone

## Known Threat Actor Profiles

### Stateless Advanced Persistent Threat (APT) Groups
- Operate without national accountability, making deterrence difficult
- Typically funded by criminal proceeds, ransomware, or dark-market services
- Signature: adaptive tooling, living-off-the-land techniques, patience
- Vulnerability: they need infrastructure (C2 servers, financial flows) — follow the money

### State-Sponsored Actors
- Operate with deniability as primary constraint — they don't want attribution
- Target critical infrastructure during crisis to create leverage, not destruction
- Vulnerability: political cost of exposure; they will stand down if attribution is credible and public

### Non-State Crisis Exploiters
- Actors who use existing crises (pandemic, climate disaster) as cover for secondary objectives
- Often opportunistic rather than planned — faster decision cycles, less operational security
- Vulnerability: speed means mistakes; look for the errors in their execution

## Intelligence Collection Priorities

### For Cyber Threats
- Command-and-control infrastructure mapping
- Financial flows (cryptocurrency tracing, dark market activity)
- Technical signature comparison against known toolkits
- Insider threat indicators in targeted organisations

### For Biological Threats
- Origin mapping: where did the pathogen first appear and who had access?
- Supply chain of precursor materials
- Communications intercepts around timing of emergence
- Parallel emergence across continents is a red flag for deliberate release

### For Environmental/Climate Threats
- Natural vs. accelerated: what's the natural rate vs. current rate?
- Industrial actors who benefit from delayed response
- Political actors suppressing or distorting scientific data

## Source Reliability Matrix
| Source Type | Reliability | Caveats |
|---|---|---|
| SIGINT (signals intelligence) | High | Can be spoofed; always corroborate |
| HUMINT (human intelligence) | Variable | Motivation of source matters more than content |
| OSINT (open source) | Medium | Widely available = may be planted |
| Technical forensics | High | Slow; requires access to evidence |
| Allied liaison | Medium-High | Shared interest ≠ shared information |

## What We're Almost Always Missing
- Intent (we can see capability; intent requires access to decision-makers)
- The full network (we see nodes, rarely the full graph)
- Timeline (actors rarely telegraph when they'll act)
- The thing we don't know we don't know — always leave a column for unknown unknowns
