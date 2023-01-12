import os
import runpy


CODE_PATH = "code.py"
code_content = os.environ.get("JOB_CODE")

if not code_content:
    print("JOB_CODE is empty or not defined.")
    exit

with open(CODE_PATH, "w", encoding="utf-8") as f:
    f.write(code_content)

runpy.run_path(CODE_PATH, run_name="__main__")
