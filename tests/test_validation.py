import os
import unittest
import yaml

class TestReusableWorkflowsSuite(unittest.TestCase):
    def setUp(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.wf_dir = os.path.join(self.root, ".github", "workflows")

    def test_core_files_exist(self):
        required = [
            "README.md",
            "Makefile",
            "SECURITY.md",
            ".gitattributes",
            "scripts/validate_workflows.py",
            "scripts/healthcheck.sh",
            "docs/architecture.svg",
            ".github/workflows/lint.yml",
            ".github/workflows/test.yml",
            ".github/workflows/docker.yml",
            ".github/workflows/terraform.yml",
            ".github/workflows/caller-full-pipeline.yml",
            ".github/workflows/ci.yml"
        ]
        for f in required:
            p = os.path.join(self.root, f)
            self.assertTrue(os.path.exists(p), f"Required file '{f}' must exist")

    def test_called_workflows_have_workflow_call(self):
        called = ["lint.yml", "test.yml", "docker.yml", "terraform.yml"]
        for c in called:
            p = os.path.join(self.wf_dir, c)
            with open(p, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            on_val = data.get("on") or data.get(True)
            self.assertIn("workflow_call", on_val, f"{c} must define on.workflow_call")

    def test_gitattributes_content(self):
        path = os.path.join(self.root, ".gitattributes")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("* text=auto eol=lf", content)
        self.assertIn("Makefile linguist-vendored=true", content)

if __name__ == "__main__":
    unittest.main()
