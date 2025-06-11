"""Lightweight agent framework used by the NWEA examples.

This module provides very small ``Agent`` and ``Runner`` helpers that mimic the
style of OpenAI's agent interface. ``Agent`` objects can either execute a
``run_func`` coroutine directly or expose that function as a ``Tool`` which can
be called by other agents.
"""

import asyncio
from typing import Callable, List, Optional

class Tool:
    """Represents a callable capability that an :class:`Agent` can use."""

    def __init__(self, name: str, description: str, func: Callable[[str], asyncio.Future]):
        self.name = name
        self.description = description
        self.func = func

class Agent:
    """Simple agent that can run a coroutine or call tools."""

    def __init__(self, name: str, instructions: str, tools: Optional[List[Tool]] = None, run_func: Optional[Callable[[str], asyncio.Future]] = None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.run_func = run_func

    def as_tool(self, tool_name: str, tool_description: str):
        """Expose this agent's ``run`` method as a :class:`Tool`."""

        async def _tool(message: str):
            return await self.run(message)

        return Tool(tool_name, tool_description, _tool)

    async def run(self, message: str):
        """Execute the agent or its first tool with the given ``message``."""
        if self.run_func:
            return await self.run_func(message)
        if self.tools:
            return await self.tools[0].func(message)
        return f"{self.instructions}\nUser message: {message}"

class Runner:
    @staticmethod
    async def run(agent: Agent, message: str):
        """Run an agent and return a simple output container."""

        content = await agent.run(message)

        class Output:
            def __init__(self, text):
                self.new_messages = [type('Msg', (), {'content': text})]

        return Output(content)
