"""Interactive tool for generating NWEA-based learning plans.

This module defines helper functions and dataclasses used by the example agent
scripts. It can be run directly as a CLI program or imported by other modules.
"""

import os
import re
from dataclasses import dataclass

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

@dataclass
class StudentData:
    """Data extracted from an NWEA MAP report."""
    name: str
    grade: str
    rit_score: int
    goal_areas: str
    instructional_areas: str

def request_input(prompt: str) -> str:
    """Prompt the user for input and return the stripped response."""
    return input(prompt).strip()


def request_int(prompt: str) -> int:
    """Prompt until a valid integer is entered."""
    while True:
        try:
            return int(request_input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def confirm_data(data: StudentData) -> bool:
    """Display the extracted student data and ask for confirmation."""
    print(f"\nPlease confirm the extracted data:\nName: {data.name}\nGrade: {data.grade}\nRIT Score: {data.rit_score}")
    ans = input("Is this correct? (y/n): ").strip().lower()
    return ans.startswith('y')


def choose_standard() -> str:
    """Prompt the user to select either Common Core or BNCC alignment."""
    while True:
        std = input("Choose the standard for alignment - type 'CC' for Common Core (US) or 'BNCC' for Brazil: ").strip().upper()
        if std in ('CC', 'BNCC'):
            return 'Common Core (US)' if std == 'CC' else 'BNCC (Brazil)'
        print("Invalid choice. Please enter 'CC' or 'BNCC'.")


def load_mapping(pdf_path: str):
    """Load RIT-to-resource mappings from a PDF if available."""
    if not PdfReader or not os.path.exists(pdf_path):
        return None
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception:
        return None
    pattern = re.compile(r"(\d+\s?-\s?\d+)\s+([^\n]+)")
    mapping = []
    for match in pattern.finditer(text):
        mapping.append((match.group(1), match.group(2)))
    return mapping


def recommend_resources(grade: str, rit: int):
    """Return up to two Khan Academy resources based on grade and RIT score."""
    pdf_map = {
        'K': 'MAP Growth Grades K-2 to Khan Academy.pdf',
        '1': 'MAP Growth Grades K-2 to Khan Academy.pdf',
        '2': 'MAP Growth Grades 2-5 to Khan Academy.pdf',
        '3': 'MAP Growth Grades 2-5 to Khan Academy.pdf',
        '4': 'MAP Growth Grades 2-5 to Khan Academy.pdf',
        '5': 'MAP Growth Grades 2-5 to Khan Academy.pdf',
    }
    key = grade.split()[0]
    pdf = pdf_map.get(key, 'MAP Growth Grades 6+ to Khan Academy.pdf')
    mapping = load_mapping(pdf)
    if mapping is None:
        return ["[Resource list requires PDF: {}]".format(pdf)]
    resources = []
    for rit_range, resource in mapping:
        low, high = [int(x) for x in rit_range.replace(' ', '').split('-')]
        if low <= rit <= high:
            resources.append(resource)
    return resources[:2]


def generate_plan(data: StudentData, standard: str):
    """Build the final Markdown learning plan for the student."""
    resources = recommend_resources(data.grade, data.rit_score)
    plan = (
        f"AI-Powered Plan for {data.name}\n"
        "---\n"
        "📈 Student Snapshot\n"
        f"* **Grade:** {data.grade}\n"
        f"* **Overall RIT Score:** {data.rit_score}\n"
        f"* **Standard Alignment:** {standard}\n"
        "---\n"
        "🚀 Foresight: Potential Growth Pathways\n"
        "To track progress effectively, it's crucial to use the student's specific growth projection provided by NWEA's normative data. This target is found in your official NWEA Growth Report. The pathways below outline potential strategies to meet and exceed that goal.\n\n"
        "**Official Growth Target:** `[Teacher to input the RIT growth goal from the NWEA Report]`\n"
        "---\n"
        "**Pathway 1: Steady & Foundational Growth**\n"
        "* **Focus:** Deep mastery of core concepts within the student's current learning zone.\n"
        "* **Key Accomplishments:** Consistent practice on recommended Khan Academy skills, closing skill gaps, >80% on unit quizzes.\n\n"
        "**Pathway 2: Accelerated Progress**\n"
        "* **Focus:** Master current-level concepts quickly and begin stretch topics from the next RIT band.\n"
        "* **Key Accomplishments:** Rapid completion of foundational exercises, tackling challenge problems, exploring next RIT range topics.\n"
        "---\n"
        "🎯 Learning Goals & Resources\n\n"
        "**Goal 1:** Strengthen priority skills\n"
        "* **Standard:** [Standard Code]\n"
        "* **Khan Academy Resources:**\n"
        f"    * {resources[0] if resources else 'Resource TBD'}\n\n"
        "**Goal 2:** Prepare for upcoming concepts\n"
        "* **Standard:** [Standard Code]\n"
        "* **Khan Academy Resources:**\n"
        f"    * {resources[1] if len(resources)>1 else 'Resource TBD'}\n"
        "---\n"
        "💡 Learning Strategies\n"
        "1. Schedule regular practice sessions using Khan Academy.\n"
        "2. Monitor progress with NWEA tools and adjust focus skills.\n"
        "3. Encourage reflective learning and goal setting.\n"
        "---\n"
        "📚 Content & Activity Ideas\n"
        "1. Create small-group instruction around the identified skills.\n"
        "2. Use manipulatives or visual aids to deepen understanding.\n"
    )
    return plan


def main():
    print("Welcome to the NWEA Goal Navigator\n")
    name = request_input("Enter Student Name: ")
    grade = request_input("Enter Grade Level (e.g., '3'): ")
    rit = request_int("Enter Overall RIT Score: ")
    goal_areas = request_input("Describe Goal Areas (optional): ")
    instructional = request_input("Describe Instructional Areas (optional): ")
    data = StudentData(name=name, grade=grade, rit_score=rit, goal_areas=goal_areas, instructional_areas=instructional)

    if not confirm_data(data):
        print("Data not confirmed. Exiting.")
        return

    standard = choose_standard()
    plan = generate_plan(data, standard)
    print(plan)

if __name__ == "__main__":
    main()
