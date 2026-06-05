"""
Run the Avengers swarm against Operation: New Dawn.

Streams the multi-agent session, captures per-hero outputs, then
renders outputs/index.html — an interactive comic-panel presentation.

Usage:
    python run_mission.py
"""

import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
for _var in ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "AZURE_OPENAI_ENDPOINT"):
    os.environ.pop(_var, None)

# ── Hero display config ─────────────────────────────────────────────────────

HERO_META = {
    "Iron Man (Tony Stark)": {
        "emoji": "🔴",
        "color": "#c0392b",
        "glow": "#e74c3c",
        "role": "Engineering & Technology",
        "bg": "#1a0a0a",
        "label": "STARK",
    },
    "Captain America (Steve Rogers)": {
        "emoji": "🔵",
        "color": "#2980b9",
        "glow": "#3498db",
        "role": "Strategy & Ethics",
        "bg": "#0a0d1a",
        "label": "CAP",
    },
    "Black Widow (Natasha Romanoff)": {
        "emoji": "⚫",
        "color": "#7f8c8d",
        "glow": "#95a5a6",
        "role": "Intelligence & Recon",
        "bg": "#0a0a0a",
        "label": "WIDOW",
    },
    "Bruce Banner / Hulk": {
        "emoji": "🟢",
        "color": "#27ae60",
        "glow": "#2ecc71",
        "role": "Science & Research",
        "bg": "#0a1a0a",
        "label": "BANNER",
    },
    "Nick Fury": {
        "emoji": "🟡",
        "color": "#f39c12",
        "glow": "#f1c40f",
        "role": "Director, S.H.I.E.L.D.",
        "bg": "#1a1500",
        "label": "FURY",
    },
}

FALLBACK_META = {
    "emoji": "⚡",
    "color": "#9b59b6",
    "glow": "#8e44ad",
    "role": "Avenger",
    "bg": "#0d0d1a",
    "label": "HERO",
}


# ── Session ──────────────────────────────────────────────────────────────────

def run_mission() -> dict:
    """Run the swarm session and return captured data."""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")

    coordinator_id_path = Path(".coordinator_id")
    environment_id_path = Path(".environment_id")

    if not coordinator_id_path.exists():
        raise SystemExit("Run create_coordinator.py first.")
    if not environment_id_path.exists():
        raise SystemExit("Run setup_environment.py first.")

    coordinator_id = coordinator_id_path.read_text().strip()
    environment_id = environment_id_path.read_text().strip()

    mission_brief_path = Path("synthetic-data/mission-brief.md")
    if not mission_brief_path.exists():
        raise SystemExit("Mission brief not found at synthetic-data/mission-brief.md")
    mission_brief = mission_brief_path.read_text()

    client = Anthropic(
        api_key=api_key,
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    print("━" * 60)
    print("  AVENGERS ASSEMBLE — OPERATION: NEW DAWN")
    print("  Coordinator:", coordinator_id)
    print("  Environment:", environment_id)
    print("━" * 60)

    session = client.beta.sessions.create(
        agent=coordinator_id,
        environment_id=environment_id,
        title="Operation: New Dawn",
    )
    print(f"\nSession: {session.id}")
    print("\nStreaming events...\n")

    # Capture state
    hero_outputs: dict[str, str] = {}          # agent_name → accumulated text
    thread_order: list[str] = []               # order heroes were spawned
    fury_synthesis: str = ""
    all_events: list[dict] = []

    with client.beta.sessions.events.stream(session.id) as stream:
        # Stream-first pattern: open stream before sending the user message
        client.beta.sessions.events.send(
            session.id,
            events=[{
                "type": "user.message",
                "content": [{"type": "text", "text": mission_brief}],
            }],
        )

        for event in stream:
            etype = event.type
            all_events.append({"type": etype})

            if etype == "session.thread_created":
                agent_name = getattr(event, "agent_name", "Unknown")
                thread_id = getattr(event, "session_thread_id", "?")
                meta = HERO_META.get(agent_name, FALLBACK_META)
                print(f"  {meta['emoji']}  Thread opened: {agent_name} [{thread_id[:12]}…]")
                if agent_name not in thread_order and agent_name != "Nick Fury":
                    thread_order.append(agent_name)

            elif etype == "agent.thread_message_received":
                from_name = getattr(event, "from_agent_name", None) or "Unknown"
                content_blocks = getattr(event, "content", []) or []
                text_parts = []
                for block in content_blocks:
                    if hasattr(block, "type") and block.type == "text":
                        text_parts.append(block.text)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                text = "\n\n".join(text_parts).strip()
                if text:
                    meta = HERO_META.get(from_name, FALLBACK_META)
                    print(f"\n  {meta['emoji']}  {from_name} reported in:")
                    preview = textwrap.shorten(text, width=120, placeholder="…")
                    print(f"     {preview}\n")
                    if from_name not in hero_outputs:
                        hero_outputs[from_name] = text
                    else:
                        hero_outputs[from_name] += "\n\n" + text

            elif etype == "agent.message":
                # Nick Fury's outbound messages / final synthesis
                content_blocks = getattr(event, "content", []) or []
                text_parts = []
                for block in content_blocks:
                    if hasattr(block, "type") and block.type == "text":
                        text_parts.append(block.text)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                text = "\n\n".join(text_parts).strip()
                if text:
                    print(f"  🟡  Nick Fury: {textwrap.shorten(text, width=100, placeholder='…')}")
                    # The final, longest message from Fury is the synthesis
                    if len(text) > len(fury_synthesis):
                        fury_synthesis = text

            elif etype == "agent.thread_message_sent":
                to_name = getattr(event, "to_agent_name", None)
                if to_name:
                    print(f"     → Dispatch to {to_name}")

            elif etype == "session.status_idle":
                stop_reason = getattr(event, "stop_reason", None)
                if stop_reason:
                    reason_type = getattr(stop_reason, "type", None) or (
                        stop_reason.get("type") if isinstance(stop_reason, dict) else None
                    )
                    if reason_type != "requires_action":
                        print("\n  ✓  Session idle — mission complete.")
                        break
                else:
                    print("\n  ✓  Session idle — mission complete.")
                    break

            elif etype == "session.status_terminated":
                print("\n  ✓  Session terminated.")
                break

    # If Fury didn't produce a standalone synthesis but wrote reports,
    # extract the longest block from hero_outputs keyed "Nick Fury"
    if not fury_synthesis and "Nick Fury" in hero_outputs:
        fury_synthesis = hero_outputs.pop("Nick Fury")

    # Fill in any heroes that were mentioned but didn't reply
    for name in thread_order:
        if name not in hero_outputs:
            hero_outputs[name] = "Awaiting report…"

    print(f"\n  Heroes reported: {list(hero_outputs.keys())}")
    print(f"  Fury synthesis: {len(fury_synthesis)} chars")

    return {
        "hero_outputs": hero_outputs,
        "thread_order": thread_order,
        "fury_synthesis": fury_synthesis,
        "session_id": session.id,
    }


# ── HTML renderer ────────────────────────────────────────────────────────────

def nl2p(text: str) -> str:
    """Convert newline-separated paragraphs to <p> tags."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paras)


def render_html(data: dict) -> str:
    hero_outputs: dict[str, str] = data["hero_outputs"]
    thread_order: list[str] = data["thread_order"]
    fury_synthesis: str = data["fury_synthesis"]
    session_id: str = data["session_id"]
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Order hero cards: thread_order first, then any stragglers
    ordered_heroes = thread_order + [
        h for h in hero_outputs if h not in thread_order and h != "Nick Fury"
    ]

    def hero_card(name: str, idx: int) -> str:
        meta = HERO_META.get(name, FALLBACK_META)
        report_html = nl2p(hero_outputs.get(name, "No report received."))
        delay_ms = idx * 400  # stagger the reveal animation
        return f"""
        <div class="hero-card" id="card-{idx}"
             style="--hero-color:{meta['color']};--hero-glow:{meta['glow']};--hero-bg:{meta['bg']};animation-delay:{delay_ms}ms">
          <div class="hero-header">
            <span class="hero-label">{meta['label']}</span>
            <span class="hero-role">{meta['role']}</span>
          </div>
          <div class="hero-name">{name}</div>
          <div class="hero-report">{report_html}</div>
        </div>"""

    hero_cards_html = "\n".join(hero_card(name, i) for i, name in enumerate(ordered_heroes))

    fury_html = nl2p(fury_synthesis) if fury_synthesis else "<p>Mission brief pending synthesis…</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Avengers Assemble — Operation: New Dawn</title>
<style>
  /* ── Reset & base ─────────────────────────────────────── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    background: #080808;
    color: #e0e0e0;
    font-family: 'Courier New', Courier, monospace;
    min-height: 100vh;
  }}

  /* ── Top bar ──────────────────────────────────────────── */
  .top-bar {{
    background: #0a0a0a;
    border-bottom: 2px solid #f1c40f;
    padding: 0.75rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
  }}
  .top-bar .title {{ color: #f1c40f; font-size: 0.85rem; letter-spacing: 0.15em; font-weight: bold; }}
  .top-bar .meta {{ color: #666; font-size: 0.7rem; }}
  .classified {{
    background: #c0392b;
    color: #fff;
    padding: 0.2rem 0.6rem;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    font-weight: bold;
    border-radius: 2px;
  }}

  /* ── Masthead ─────────────────────────────────────────── */
  .masthead {{
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
    overflow: hidden;
  }}
  .masthead::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, #1a1200 0%, #080808 70%);
    z-index: 0;
  }}
  .masthead > * {{ position: relative; z-index: 1; }}
  .masthead h1 {{
    font-size: clamp(2rem, 6vw, 4.5rem);
    color: #f1c40f;
    letter-spacing: 0.08em;
    text-shadow: 0 0 40px #f1c40f88;
    line-height: 1.1;
  }}
  .masthead .op-name {{
    font-size: clamp(0.8rem, 2vw, 1.1rem);
    color: #aaa;
    letter-spacing: 0.3em;
    margin-top: 0.5rem;
  }}
  .masthead .omega-badge {{
    display: inline-block;
    margin-top: 1rem;
    background: #c0392b;
    color: #fff;
    padding: 0.3rem 1.2rem;
    letter-spacing: 0.25em;
    font-size: 0.75rem;
    font-weight: bold;
    border-radius: 2px;
    box-shadow: 0 0 20px #c0392b88;
  }}

  /* ── Section labels ───────────────────────────────────── */
  .section-label {{
    text-align: center;
    padding: 2rem 1rem 1rem;
    color: #f1c40f;
    font-size: 0.75rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
  }}

  /* ── Hero grid ────────────────────────────────────────── */
  .hero-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2px;
    padding: 0 2px 2px;
    max-width: 1600px;
    margin: 0 auto;
  }}

  /* ── Hero card ────────────────────────────────────────── */
  .hero-card {{
    background: var(--hero-bg, #0a0a0a);
    border: 1px solid var(--hero-color, #444);
    padding: 1.5rem;
    opacity: 0;
    transform: translateY(20px);
    animation: card-appear 0.6s ease forwards;
    position: relative;
    overflow: hidden;
  }}
  .hero-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--hero-color, #444);
    box-shadow: 0 0 12px var(--hero-glow, #444);
  }}
  @keyframes card-appear {{
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  .hero-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.4rem;
  }}
  .hero-label {{
    color: var(--hero-color, #aaa);
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    font-weight: bold;
  }}
  .hero-role {{
    color: #666;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
  }}
  .hero-name {{
    font-size: 1.05rem;
    color: #fff;
    font-weight: bold;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--hero-color, #333);
    text-shadow: 0 0 8px var(--hero-glow, transparent);
  }}
  .hero-report {{
    font-size: 0.82rem;
    line-height: 1.65;
    color: #ccc;
  }}
  .hero-report p {{ margin-bottom: 0.75rem; }}
  .hero-report p:last-child {{ margin-bottom: 0; }}

  /* ── Fury synthesis ───────────────────────────────────── */
  .fury-section {{
    max-width: 960px;
    margin: 0 auto;
    padding: 2rem;
  }}
  .fury-panel {{
    background: #1a1500;
    border: 2px solid #f1c40f;
    padding: 2rem 2.5rem;
    position: relative;
    box-shadow: 0 0 40px #f1c40f22;
  }}
  .fury-panel::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: #f1c40f;
    box-shadow: 0 0 20px #f1c40f;
  }}
  .fury-byline {{
    color: #f1c40f;
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #f1c40f44;
    display: flex;
    justify-content: space-between;
  }}
  .fury-synthesis {{
    font-size: 0.88rem;
    line-height: 1.75;
    color: #ddd;
  }}
  .fury-synthesis p {{ margin-bottom: 1rem; }}
  .fury-synthesis p:last-child {{ margin-bottom: 0; }}

  /* ── Footer ───────────────────────────────────────────── */
  .footer {{
    text-align: center;
    padding: 2rem;
    color: #444;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    border-top: 1px solid #1a1a1a;
    margin-top: 3rem;
  }}

  /* ── Scan lines overlay ───────────────────────────────── */
  body::after {{
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.03) 2px,
      rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
  }}
</style>
</head>
<body>

<!-- Top bar -->
<div class="top-bar">
  <span class="title">S.H.I.E.L.D. COMMAND</span>
  <span class="classified">CLASSIFIED</span>
  <span class="meta">{ts} · SESSION {session_id[:16]}…</span>
</div>

<!-- Masthead -->
<div class="masthead">
  <h1>AVENGERS ASSEMBLE</h1>
  <div class="op-name">OPERATION: NEW DAWN</div>
  <div class="omega-badge">PROTOCOL OMEGA ACTIVE</div>
</div>

<!-- Hero reports -->
<div class="section-label">▸ hero field reports</div>
<div class="hero-grid">
{hero_cards_html}
</div>

<!-- Nick Fury synthesis -->
<div class="section-label">▸ director's synthesis</div>
<div class="fury-section">
  <div class="fury-panel">
    <div class="fury-byline">
      <span>NICK FURY — DIRECTOR, S.H.I.E.L.D.</span>
      <span>WORLD SECURITY COUNCIL BRIEF</span>
    </div>
    <div class="fury-synthesis">
{fury_html}
    </div>
  </div>
</div>

<!-- Footer -->
<div class="footer">
  AVENGERS ASSEMBLE · HACKATHON DEMO · GENERATED {ts}
</div>

<!-- Staggered card reveal driven by CSS animation-delay -->
<script>
  // Re-trigger animations after a short delay so the cards
  // light up sequentially even if the page was already loaded.
  document.querySelectorAll('.hero-card').forEach((card, i) => {{
    card.style.animationPlayState = 'paused';
    setTimeout(() => {{
      card.style.animationPlayState = 'running';
    }}, 200 + i * 400);
  }});
</script>

</body>
</html>"""


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    data = run_mission()

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    html = render_html(data)
    output_path = output_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Presentation rendered → {output_path}")
    print(f"  Open with:  open {output_path}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()
