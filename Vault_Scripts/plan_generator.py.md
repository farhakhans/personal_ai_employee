# plan_generator.py
from pathlib import Path
import subprocess

VAULT_PATH = Path("/Vault")
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
PLANS = VAULT_PATH / "Plans"

for task_file in NEEDS_ACTION.glob("*.md"):
    plan_file = PLANS / f"PLAN_{task_file.stem}.md"
    prompt = f"""
Read the task in {task_file}
Create a plan in {plan_file}
Include:
- Objective
- Step by step actions
- Checkboxes for completion
- Human approval steps if needed
"""
    subprocess.run(["qwen", "-p", prompt])
    print(f"Plan generated for {task_file}")
