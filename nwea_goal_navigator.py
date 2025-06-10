# NWEA Goal Navigator agent script

import os
import re
from dataclasses import dataclass

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

@dataclass
class StudentData:
    name: str
    grade: str
    rit_score: int
    goal_areas: str
    instructional_areas: str

def request_input(prompt: str) -> str:
    return input(prompt).strip()


def confirm_data(data: StudentData) -> bool:
    print(f"\nPlease confirm the extracted data:\nName: {data.name}\nGrade: {data.grade}\nRIT Score: {data.rit_score}")
    ans = input("Is this correct? (y/n): ").strip().lower()
    return ans.startswith('y')


def choose_standard() -> str:
    while True:
        std = input("Choose the standard for alignment - type 'CC' for Common Core (US) or 'BNCC' for Brazil: ").strip().upper()
        if std in ('CC', 'BNCC'):
            return 'Common Core (US)' if std == 'CC' else 'BNCC (Brazil)'
        print("Invalid choice. Please enter 'CC' or 'BNCC'.")


def load_mapping(pdf_path: str):
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
    resources = recommend_resources(data.grade, data.rit_score)
    plan = f"""AI-Powered Plan for {data.name}\n---\n📈 Student Snapshot\n* **Grade:** {data.grade}\n* **Overall RIT Score:** {data.rit_score}\n* **Standard Alignment:** {standard}\n---\n🚀 Foresight: Potential Growth Pathways\nTo track progress effectively, it's crucial to use the student's specific growth projection provided by NWEA's normative data. This target is found in your official NWEA Growth Report. The pathways below outline potential strategies to meet and exceed that goal.\n\n**Official Growth Target:** `[Teacher to input the RIT growth goal from the NWEA Report]`\n---\n**Pathway 1: Steady & Foundational Growth**\n* **Focus:** Deep mastery of core concepts within the student's current learning zone.\n* **Key Accomplishments:** Consistent practice on recommended Khan Academy skills, closing skill gaps, >80% on unit quizzes.\n\n**Pathway 2: Accelerated Progress**\n* **Focus:** Master current-level concepts quickly and begin stretch topics from the next RIT band.\n* **Key Accomplishments:** Rapid completion of foundational exercises, tackling challenge problems, exploring next RIT range topics.\n---\n🎯 Learning Goals & Resources\n\n**Goal 1:** Strengthen priority skills\n* **Standard:** [Standard Code]\n* **Khan Academy Resources:**\n    * {resources[0] if resources else 'Resource TBD'}\n\n**Goal 2:** Prepare for upcoming concepts\n* **Standard:** [Standard Code]\n* **Khan Academy Resources:**\n    * {resources[1] if len(resources)>1 else 'Resource TBD'}\n---\n💡 Learning Strategies\n1. Schedule regular practice sessions using Khan Academy.\n2. Monitor progress with NWEA tools and adjust focus skills.\n3. Encourage reflective learning and goal setting.\n---\n📚 Content & Activity Ideas\n1. Create small-group instruction around the identified skills.\n2. Use manipulatives or visual aids to deepen understanding.\n"""
    print(plan)


def main():
    print("Welcome to the NWEA Goal Navigator\n")
    name = request_input("Enter Student Name: ")
    grade = request_input("Enter Grade Level (e.g., '3'): ")
    rit = int(request_input("Enter Overall RIT Score: "))
    goal_areas = request_input("Describe Goal Areas (optional): ")
    instructional = request_input("Describe Instructional Areas (optional): ")
    data = StudentData(name=name, grade=grade, rit_score=rit, goal_areas=goal_areas, instructional_areas=instructional)

    if not confirm_data(data):
        print("Data not confirmed. Exiting.")
        return

    standard = choose_standard()
    generate_plan(data, standard)

if __name__ == "__main__":
    main()
