"""Example showing how to orchestrate the learning-plan workflow with agents."""

import asyncio
from agents import Agent, Runner
from nwea_goal_navigator import (
    StudentData,
    generate_plan,
    confirm_data,
    choose_standard,
    request_int,
)

async def plan_tool(message: str) -> str:
    name = input("Enter Student Name: ")
    grade = input("Enter Grade Level (e.g., '3'): ")
    rit = request_int("Enter Overall RIT Score: ")
    goal_areas = input("Describe Goal Areas (optional): ")
    instructional = input("Describe Instructional Areas (optional): ")
    data = StudentData(name=name, grade=grade, rit_score=rit, goal_areas=goal_areas, instructional_areas=instructional)
    if not confirm_data(data):
        return "Data not confirmed."
    standard = choose_standard()
    return generate_plan(data, standard)

planner_agent = Agent(
    name="planner_agent",
    instructions="Collect student MAP data and create a learning plan.",
    run_func=plan_tool,
)

planner_tool = planner_agent.as_tool(
    tool_name="build_plan",
    tool_description="Generate NWEA learning plan from user input",
)

manager_agent = Agent(
    name="manager_agent",
    instructions=(
        "You are the NWEA Goal Navigator. Use the tools to build a learning plan."
    ),
    tools=[planner_tool],
)

async def main():
    start_msg = "Let's create a learning plan."
    result = await Runner.run(manager_agent, start_msg)
    for message in result.new_messages:
        print(message.content)

if __name__ == "__main__":
    asyncio.run(main())
