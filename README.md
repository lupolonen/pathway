# Pathway Repository

This repository provides a simple example project.

## Files

- `career_pathway.html` - demonstration of a career pathway user interface using React and Tailwind CSS.
- `nwea_goal_navigator.py` - command line tool implementing the **NWEA Goal Navigator** agent. The script guides teachers through entering MAP Growth data and generates a learning plan template.
- `agents.py` - minimal helper module providing `Agent` and `Runner` classes for agent-style workflows.
- `nwea_goal_agent.py` - example showing how to build the NWEA agent using the `Agent`/`Runner` interface.
- `nwea_autonomous_agent.py` - reads `student_data.json` and generates a plan without interactive prompts.
- `requirements.txt` - Python dependencies.

## Career Pathway Demo

To view the sample career pathway interface, open `career_pathway.html` in any web browser. The file loads React and Tailwind CSS from public CDNs, so an internet connection is required when you first open the page.

## Usage

1. Ensure Python 3 is installed and install the required packages:

```bash
pip install -r requirements.txt
```

2. Place the mapping PDFs (e.g., `MAP Growth Grades 2-5 to Khan Academy.pdf`) in the same directory as the script.

3. Run the tool:

```bash
python3 nwea_goal_navigator.py
```

Follow the prompts to enter student data and choose the standard (Common Core or BNCC). The script will then display an example plan formatted in Markdown.

### Autonomous Example

For a fully automated run place your student information in ``student_data.json`` and run:

```bash
python3 nwea_autonomous_agent.py
```

The agent will read the JSON file and print the generated plan without further prompts.

### Agent Example

You can also run the simplified agent version:

```bash
python3 nwea_goal_agent.py
```

This script uses the `Agent` and `Runner` classes to orchestrate the workflow, mimicking the style of OpenAI's agent platform.

## Deploying on OpenAI

To run this code on the OpenAI Assistants platform, create a new assistant and
enable the **Code Interpreter** tool. Upload the repository files and specify
``nwea_goal_agent.py`` (or ``nwea_autonomous_agent.py`` for unattended runs) as
the entry point. When you invoke the assistant it will execute the script and
return the generated learning plan.

## License

This project is licensed under the [MIT License](LICENSE).

