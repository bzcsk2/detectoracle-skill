from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DetectorOracleCliBrandingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (
            Path(__file__).resolve().parent.parent
            / "skills"
            / "detectoracle"
            / "scripts"
            / "detectoracle.py"
        )
        cls.python = sys.executable

    def _run(self, *args: str, home: Path) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["DETECTORACLE_HOME"] = str(home)
        env.pop("ISSUEORACLE_HOME", None)
        return subprocess.run(
            [self.python, str(self.script), *args],
            capture_output=True,
            env=env,
            text=True,
            timeout=30,
        )

    def test_doctor_uses_detectoracle_public_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run("doctor", home=Path(tmp))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DETECTORACLE_HOME", result.stdout)
        self.assertIn("/detectoracle scan .", result.stdout)
        self.assertNotIn("ISSUEORACLE_HOME", result.stdout)
        self.assertNotIn("/issueoracle scan .", result.stdout)

    def test_experience_missing_data_mentions_detectoracle(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run("experience", "list", home=Path(tmp))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run `detectoracle mine` first", result.stderr)
        self.assertNotIn("issueoracle", result.stderr.lower())

    def test_experience_list_reads_legacy_candidates_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            legacy_dir = home / "bugplay" / "candidates"
            legacy_dir.mkdir(parents=True)
            legacy_path = legacy_dir / "experience.json"
            legacy_path.write_text(
                json.dumps(
                    {
                        "experiences": [
                            {
                                "id": "exp-legacy-001",
                                "title": "Legacy Candidate",
                                "status": "candidate",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = self._run("experience", "list", home=home)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Legacy Candidate", result.stdout)
        self.assertNotIn("issueoracle", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
