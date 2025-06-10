# Pathway Repository

This repository provides a simple example project.

## Files

- `career_pathway.html` - demonstration of a career pathway user interface using React and Tailwind CSS.
- `nwea_goal_navigator.py` - command line tool implementing the **NWEA Goal Navigator** agent. The script guides teachers through entering MAP Growth data and generates a learning plan template.

## Usage

1. Ensure Python 3 is installed. Optionally install `PyPDF2` if you want the script to read mapping data from the official MAP Growth PDFs.

```bash
pip install PyPDF2
```

2. Place the mapping PDFs (e.g., `MAP Growth Grades 2-5 to Khan Academy.pdf`) in the same directory as the script.

3. Run the tool:

```bash
python3 nwea_goal_navigator.py
```

Follow the prompts to enter student data and choose the standard (Common Core or BNCC). The script will then display an example plan formatted in Markdown.
