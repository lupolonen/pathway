import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from nwea_goal_navigator import StudentData, generate_plan
from nwea_autonomous_agent import fetch_google_snippets

load_dotenv()

DATA_FILE = Path("student_data.json")


def build_plan(entry: dict) -> str:
    """Generate a learning plan for a single student entry."""
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
    return plan


def main() -> None:
    st.title("NWEA Goal Navigator")

    mode = st.sidebar.selectbox("Data Source", ("Manual Entry", "From JSON File"))

    if mode == "Manual Entry":
        name = st.text_input("Student Name")
        grade = st.text_input("Grade Level (e.g., '3')")
        rit = st.number_input("Overall RIT Score", min_value=0, step=1)
        goal_areas = st.text_input("Goal Areas")
        instructional_areas = st.text_input("Instructional Areas")
        standard = st.selectbox(
            "Standard", ("Common Core (US)", "BNCC (Brazil)")
        )
        if st.button("Generate Plan"):
            entry = {
                "name": name,
                "grade": grade,
                "rit_score": rit,
                "goal_areas": goal_areas,
                "instructional_areas": instructional_areas,
                "standard": standard,
            }
            st.markdown(build_plan(entry))
    else:
        file = st.file_uploader("Upload student_data.json", type="json")
        if file is None and DATA_FILE.exists():
            file_data = DATA_FILE.read_text()
        elif file is not None:
            file_data = file.getvalue().decode("utf-8")
        else:
            file_data = None

        if file_data:
            try:
                data = json.loads(file_data)
                records = [data] if isinstance(data, dict) else data
                if st.button("Generate Plans"):
                    for idx, entry in enumerate(records, start=1):
                        st.subheader(f"Plan {idx}")
                        st.markdown(build_plan(entry))
            except json.JSONDecodeError as exc:
                st.error(f"Invalid JSON: {exc}")


if __name__ == "__main__":
    main()
