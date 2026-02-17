from deepagents.backends.utils import create_file_data
import os, glob

SKILLS_FILES = {}

SKILL_DIR = "./src/skills/"

for skill_file in glob.glob("**/SKILL.md", recursive=True):
    with open(skill_file, "rb") as response:
        skill_content = response.read().decode("utf-8")
        SKILLS_FILES[skill_file] = create_file_data(skill_content)
