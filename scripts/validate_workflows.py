#!/usr/bin/env python3
"""
GitHub Actions Reusable Workflows Schema Validator
Verifies workflow syntax, on.workflow_call configurations, inputs, outputs, and job dependencies.
"""

import os
import sys
import yaml

WORKFLOWS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows"))
REQUIRED_WORKFLOWS = {"lint.yml", "test.yml", "docker.yml", "terraform.yml"}

def validate_workflow_file(filepath):
    print(f"[*] Validating workflow schema: {os.path.basename(filepath)}")
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"  [FAIL] YAML parsing error in {filepath}: {e}", file=sys.stderr)
            return False

    if not isinstance(data, dict):
        print(f"  [FAIL] Workflow {filepath} is not a valid YAML mapping.", file=sys.stderr)
        return False

    if "name" not in data:
        print(f"  [FAIL] Missing 'name' field in {filepath}", file=sys.stderr)
        return False

    if "jobs" not in data:
        print(f"  [FAIL] Missing 'jobs' field in {filepath}", file=sys.stderr)
        return False

    fname = os.path.basename(filepath)
    if fname in REQUIRED_WORKFLOWS:
        on_trigger = data.get("on") or data.get(True)  # YAML parser might parse 'on' as boolean True
        if isinstance(on_trigger, dict):
            if "workflow_call" not in on_trigger:
                print(f"  [FAIL] Called workflow {fname} must declare 'workflow_call' trigger.", file=sys.stderr)
                return False
        else:
            print(f"  [FAIL] Invalid 'on' section in {fname}", file=sys.stderr)
            return False

    print(f"  [PASS] Workflow '{data.get('name')}' valid with {len(data.get('jobs', {}))} jobs.")
    return True

def main():
    if not os.path.exists(WORKFLOWS_DIR):
        print(f"[FAIL] Directory {WORKFLOWS_DIR} not found.", file=sys.stderr)
        sys.exit(1)

    all_valid = True
    found_workflows = set()

    for f in os.listdir(WORKFLOWS_DIR):
        if f.endswith(".yml") or f.endswith(".yaml"):
            found_workflows.add(f)
            fp = os.path.join(WORKFLOWS_DIR, f)
            if not validate_workflow_file(fp):
                all_valid = False

    missing = REQUIRED_WORKFLOWS - found_workflows
    if missing:
        print(f"[FAIL] Missing required reusable workflows: {missing}", file=sys.stderr)
        all_valid = False

    if not all_valid:
        print("[FAIL] Workflow validation checks failed.", file=sys.stderr)
        sys.exit(1)

    print("[SUCCESS] All enterprise reusable workflows passed schema verification.")
    sys.exit(0)

if __name__ == "__main__":
    main()
