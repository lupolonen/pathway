"""Run the NWEA Goal Navigator without interactive prompts.

This script reads student information from ``student_data.json`` and prints a
learning plan. It demonstrates how the simple agent framework can be used in a
fully automated mode.
"""

import asyncio
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from agents import Agent, Runner
from nwea_goal_navigator import StudentData, generate_plan

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("CX")

def fetch_google_snippets(query: str) -> str:
    """Return top snippets from Google Custom Search."""
    if not GOOGLE_API_KEY or not CX:
        return ""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": CX, "q": query}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        snippets = [item.get("snippet", "") for item in data.get("items", [])]
        return "\n".join(snippets[:3])
    except Exception as exc:
        return f"Error retrieving snippets: {exc}"

DATA_FILE = Path("student_data.json")

async def plan_from_file(_: str) -> str:
    if not DATA_FILE.exists():
        return f"Data file {DATA_FILE} not found."
    data = json.loads(DATA_FILE.read_text())

    # ``student_data.json`` can contain either a single object or a list of
    # objects. Normalize to a list so we can iterate over multiple students.
    if isinstance(data, dict):
        records = [data]
    else:
        records = data

    plans = []
    for entry in records:
        student = StudentData(
            name=entry.get("name", "Unnamed"),
            grade=entry.get("grade", ""),
            rit_score=int(entry.get("rit_score", 0)),
            goal_areas=entry.get("goal_areas", ""),
            instructional_areas=entry.get("instructional_areas", ""),
        )
        standard = entry.get("standard", "Common Core (US)")
        query = f"{student.grade} grade {student.goal_areas}".strip()
        snippets = fetch_google_snippets(query)
        plan = generate_plan(student, standard)
        if snippets:
            plan += "\n\n🔍 Search Snippets\n" + snippets
        plans.append(plan)

    # Join multiple plans with a separator for clarity
    return "\n\n".join(plans)

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
