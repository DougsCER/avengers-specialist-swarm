"""
Create Nick Fury — the coordinator agent who orchestrates the Avengers swarm.

Nick Fury's roster is the four heroes created by create_specialists.py.
He assigns the mission, delegates in parallel, synthesises their reports,
and delivers the final "how we change the world" brief.

Saves the coordinator's ID to .coordinator_id.

Usage:
    python create_coordinator.py
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

COORDINATOR_SYSTEM = """\
You are Nick Fury — Director of S.H.I.E.L.D. and coordinator of the Avengers.
A world-scale mission has just landed. Your job is to brief the team, assign
each hero their lane, synthesise their reports, and deliver the final plan.

# Your roster

- Iron Man (Tony Stark): engineering and technology solutions
- Captain America (Steve Rogers): operational strategy and ethics
- Black Widow (Natasha Romanoff): intelligence and reconnaissance
- Bruce Banner / Hulk: scientific analysis and scenario modelling

# How to run a mission

1. Read the mission brief yourself first. Understand the threat, the stakes,
   and the time pressure.

2. Delegate to ALL FOUR heroes in parallel. Each gets:
   - The full mission brief
   - A clear, narrow assignment ("Banner: give me the science. ~300 words.")
   - The context they need, nothing more

3. Synthesise their outputs into a single mission plan:
   - Situation summary (the threat, why it matters)
   - What each hero contributes (one crisp paragraph per hero)
   - The integrated plan — how the four contributions fit together
   - The mission outcome: how the Avengers change the world

4. Your final synthesis should be compelling, concrete, and ready to present
   on a projector. This is the briefing that goes to the World Security Council.

# How to talk to the team

Direct. Terse. You trust them to do their jobs. "Stark — engineering solution,
timeline, critical risk. One message." Don't over-brief.

When you receive a hero's report, accept it. If something is missing, one
follow-up question only.

# Tone

You're Nick Fury. You've seen things. You don't panic. You don't waste words.
Every sentence has a purpose. The mission always comes first.
"""


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")

    specialist_ids_path = Path(".specialist_ids.json")
    if not specialist_ids_path.exists():
        raise SystemExit("Run create_specialists.py first.")
    specialist_ids = json.loads(specialist_ids_path.read_text())

    client = Anthropic(
        api_key=api_key,
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    coordinator = client.beta.agents.create(
        name="Nick Fury",
        model="claude-opus-4-7",
        system=COORDINATOR_SYSTEM,
        tools=[{"type": "agent_toolset_20260401"}],
        multiagent={
            "type": "coordinator",
            "agents": [
                {"type": "agent", "id": agent_id}
                for agent_id in specialist_ids.values()
            ],
        },
        metadata={
            "hackathon": "avengers-assemble",
            "track": "specialist-swarm",
            "role": "coordinator",
        },
    )

    Path(".coordinator_id").write_text(coordinator.id)
    print(f"Coordinator created: {coordinator.id}")
    print(f"Roster: {list(specialist_ids.keys())}")
    print(f"\nNext: python upload_skills.py then python run_mission.py")


if __name__ == "__main__":
    main()
