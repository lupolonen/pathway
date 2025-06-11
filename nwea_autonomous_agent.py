"""Run the NWEA Goal Navigator without interactive prompts.

This script reads student information from ``student_data.json`` and prints a
learning plan. It demonstrates how the simple agent framework can be used in a
fully automated mode.
"""

import asyncio
import json
from pathlib import Path

from agents import Agent, Runner
from nwea_goal_navigator import StudentData, generate_plan

DATA_FILE = Path("student_data.json")

async def plan_from_file(_: str) -> str:
    if not DATA_FILE.exists():
        return f"Data file {DATA_FILE} not found."
    data = json.loads(DATA_FILE.read_text())
    student = StudentData(
        name=data.get("name", "Unnamed"),
        grade=data.get("grade", ""),
        rit_score=int(data.get("rit_score", 0)),
        goal_areas=data.get("goal_areas", ""),
        instructional_areas=data.get("instructional_areas", ""),
    )
    standard = data.get("standard", "Common Core (US)")
    return generate_plan(student, standard)

planner_agent = Agent(
    name="autonomous_planner",
    instructions="Generate a learning plan from file data.",
    run_func=plan_from_file,
)

async def main() -> None:
    result = await Runner.run(planner_agent, "auto")
    for message in result.new_messages:
        print(message.content)

if __name__ == "__main__":
    asyncio.run(main())
