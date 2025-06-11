import json
from pathlib import Path

import openai
import time
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI()

ASSISTANT_ID = "asst_tRt1rh52VQmr6vPZ86bsF98n"


def call_map_assistant(student_data: dict) -> str:
    """Return a learning plan from the MAP assistant."""
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=json.dumps(student_data),
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        if run.status == "completed":
            break
        if run.status == "failed":
            raise RuntimeError(f"Run failed: {run.last_error}")
        time.sleep(0.5)

    msgs = client.beta.threads.messages.list(thread_id=thread.id)
    return msgs.data[0].content[0].text.value


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
