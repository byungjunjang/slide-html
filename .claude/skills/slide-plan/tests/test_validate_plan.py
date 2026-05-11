"""validate_plan.py — exit codes and stderr messages on the 3 fixtures."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "validate_plan.py"
FIXTURES = SKILL / "tests" / "fixtures"


def run(plan_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(plan_path)],
        capture_output=True,
        text=True,
    )


class ValidatePlanTest(unittest.TestCase):
    def test_valid_plan_exits_zero(self) -> None:
        r = run(FIXTURES / "valid-plan.json")
        self.assertEqual(
            r.returncode, 0,
            f"valid-plan should pass.\nstderr:\n{r.stderr}\nstdout:\n{r.stdout}",
        )

    def test_r2_missing_takeaway_exits_one(self) -> None:
        r = run(FIXTURES / "invalid-r2-missing-takeaway.json")
        self.assertEqual(r.returncode, 1, f"R2 violation must exit 1.\nstderr:\n{r.stderr}")
        self.assertIn("R2", r.stderr)

    def test_r5_empty_evidence_exits_one(self) -> None:
        r = run(FIXTURES / "invalid-r5-empty-evidence.json")
        self.assertEqual(r.returncode, 1, f"R5 violation must exit 1.\nstderr:\n{r.stderr}")
        self.assertIn("R5", r.stderr)


if __name__ == "__main__":
    unittest.main()
