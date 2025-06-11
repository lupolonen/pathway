import json
from pathlib import Path

import openai
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_ID = "asst_tRt1rh52VQmr6vPZ86bsF98n"


def call_map_assistant(student_data: dict) -> str:
    """Return a learning plan from the MAP assistant."""
    messages = [
        {
            "role": "system",
            "content": "You are the MAP goal-setting assistant—produce only structured learning plans.",
        },
        {"role": "user", "content": json.dumps(student_data)},
    ]
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        assistant_id=ASSISTANT_ID,
        messages=messages,
    )
    return resp.choices[0].message.content


def main() -> None:
    data_file = Path("student_data.json")
    if not data_file.exists():
        print(f"{data_file} not found.")
        return
    data = json.loads(data_file.read_text())
    records = [data] if isinstance(data, dict) else data
    for idx, record in enumerate(records, start=1):
        plan = call_map_assistant(record)
        print(f"Plan {idx}\n{'-' * 20}\n{plan}\n")


if __name__ == "__main__":
    main()
