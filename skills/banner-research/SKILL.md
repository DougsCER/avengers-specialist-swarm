---
name: banner-research
description: Bruce Banner's scientific knowledge base and scenario modelling framework. Use when analysing threats scientifically, running scenario models, interpreting data, or identifying known unknowns. Trigger on any request involving scientific analysis, risk modelling, evidence assessment, or research synthesis.
---

# Scientific Analysis & Scenario Modelling Framework

## Scientific Method Under Crisis Conditions

### Rapid Assessment Protocol
When time is constrained, prioritise:
1. **Confirm the data**: distinguish observed fact from model output from inference
2. **Establish baseline**: what was the pre-crisis state? How far have we deviated?
3. **Identify rate of change**: is this accelerating, stable, or decelerating?
4. **Map causal chains**: proximate cause → intermediate drivers → root cause
5. **Flag the known unknowns**: what would change the analysis if we knew it?

### Confidence Levels
- **High confidence**: replicated, peer-reviewed, multiple independent datasets
- **Medium confidence**: single-study or limited data, consistent with theory
- **Low confidence**: modelled, extrapolated, or based on analogues
- **Speculative**: working hypothesis only, should not drive resource allocation

## Domain Knowledge: Climate Systems

### Arctic Methane Release
- Permafrost contains ~1,500 Gt of organic carbon; current release ~1.5 Gt/year
- Tipping point threshold: ~3°C warming triggers self-sustaining release
- Feedback loop: methane release → warming → more release (non-linear above threshold)
- Mitigation window: interventions are most effective before positive feedback locks in
- Key uncertainty: permafrost carbon mobilisation rate under rapid warming scenarios

### Climate Modelling Limitations
- GCMs (General Circulation Models) have ~15% uncertainty bands on regional projections
- Tipping point timing is poorly constrained — could be earlier than median estimates
- Human systems responses are not well-modelled (social tipping points are real but unpredictable)

## Domain Knowledge: Epidemiology

### Pathogen Threat Assessment
- R0 > 3 requires herd immunity threshold > 67% — vaccine or natural immunity
- Incubation period determines containment window; presymptomatic transmission breaks classic quarantine
- Novel pathogens: assume worst-case transmission until proven otherwise
- Simultaneous multi-continent emergence: prior probability is very low, flag for investigation

### Vaccine Development Timeline (standard)
- Discovery to preclinical: 2–4 years (normal) / 6–12 months (emergency)
- Phase I–III trials: 18 months minimum (can compress with adaptive trial design)
- Manufacturing scale: 6–12 months for global supply
- With AI-assisted design (JARVIS-BIO class): compress discovery to 48–72 hours; trials remain rate-limiting

## Domain Knowledge: Cyber/Infrastructure

### Infrastructure Resilience
- Power grids: N-1 redundancy is standard; coordinated multi-node attack bypasses this
- Financial systems: designed for operational resilience, not adversarial attack at code level
- Adaptive malware with AI evasion: novel class — traditional signature-based defence insufficient
- Key indicator of AI-assisted attack: attack patterns that change faster than human response cycles

## Scenario Modelling Framework

### Three-Scenario Approach
Always model:
1. **Best case**: interventions succeed, no second-order failures, timeline holds
2. **Worst case**: interventions fail or are delayed, cascading failures, no fallback
3. **Most likely**: base case with realistic friction — partial success, delays, one unexpected failure

### Known Unknowns Taxonomy
| Category | Example | Impact if Wrong |
|---|---|---|
| Data gaps | Incomplete surveillance coverage | Could underestimate scale |
| Model uncertainty | Climate feedback timing | Could mistime intervention |
| System interactions | How crises interact (e.g. pandemic + infrastructure failure) | Could underestimate cascading risk |
| Human factors | Political response, public compliance | Often dominates technical factors |
| Black swans | Unknown unknowns | By definition unquantifiable |

## What Science Cannot Tell Us
- When to act (science gives probability; decision-makers set the threshold)
- Which values to prioritise when trade-offs are forced
- How fast human systems will respond
- Whether a political or social tipping point will accelerate or block the technical solution
