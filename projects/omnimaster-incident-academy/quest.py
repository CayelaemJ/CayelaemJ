"""OmniMaster Incident Academy: a synthetic, offline engineering quiz game.

No secrets, accounts, personal data, network calls, randomness or persistence.
Fictional scenarios test reasoning, not formal professional certification.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class Incident:
    code: str
    domain: str
    scenario: str
    options: tuple[str, str, str]
    answer: int
    why: str


INCIDENTS: tuple[Incident, ...] = (
    Incident(
        "GRAIN-01", "Analytics", "One invoice has 2 deliveries and 3 inspection records. "
        "A join across all three repeats the invoice amount 6 times. What first?",
        ("Wrap SUM in DISTINCT and ship", "Define fact grain and reconcile joins",
         "Increase dashboard capacity"),
        2, "A many-to-many multiplication is a semantic problem. Model each fact "
        "at the right grain and reconcile to the invoice source."),
    Incident(
        "CDC-02", "Data Engineering", "Two legitimate updates share one second-resolution "
        "timestamp, and your extractor uses an exclusive timestamp watermark. What next?",
        ("Assume the later event did not matter",
         "Use reliable change positions or bounded replay and reconciliation",
         "Refresh the web page twice"),
        2, "An exclusive coarse watermark can miss changes; an inclusive one still "
        "does not reconstruct every transition or physical delete."),
    Incident(
        "TENANT-03", "Backend Security", "A UI hides a payroll export button. An ordinary "
        "user directly calls the endpoint with another tenant's ID. What protects it?",
        ("A CSS class on the button", "The browser's disabled flag",
         "Server-side role and tenant checks on every request"),
        3, "UI visibility is never a permission boundary. Check identity, tenant "
        "scope and operation authority server-side."),
    Incident(
        "AI-04", "Applied AI", "A model confidently quotes a fictional policy from a "
        "source that never contained that text. Which response is safest?",
        ("Reject unsupported evidence and route for correction",
         "Accept the answer because confidence is 0.98",
         "Ask the model to score its own honesty"),
        1, "An LLM's confidence is not grounded evidence. Require approved sources, "
        "validation and a meaningful review or no-answer path."),
    Incident(
        "CUTOVER-05", "Databases", "Your PostgreSQL target restored successfully, "
        "but old production writes continue and data is a day behind. What now?",
        ("Change live DNS immediately",
         "Block cutover until final sync, fencing, tests and rollback are verified",
         "Delete the old provider before testing"),
        2, "Schema restore and connectivity do not prove parity, sole-writer "
        "control, permission safety or rollback readiness."),
    Incident(
        "QUERY-06", "SQL Performance", "A date predicate wraps an indexed date column "
        "in a formatting function and the range seek disappears. Best experiment?",
        ("Test direct date bounds and compare plans and totals",
         "Add a bigger loading spinner",
         "Remove every index"),
        1, "A direct range may be sargable. Compare EXPLAIN output and verify the "
        "business aggregate stayed correct."),
    Incident(
        "MFA-07", "Identity", "An administrator has a valid password-only session "
        "but tries to perform a privileged mutation requiring fresh MFA.",
        ("Trust a frontend pop-up",
         "Allow it once because the user exists",
         "Deny server-side until valid step-up evidence is present"),
        3, "High-risk actions need enforced server-side proof. Factor enrolment "
        "and recovery must not create a parallel bypass."),
    Incident(
        "RELEASE-08", "Release Engineering", "All Python unit tests pass, but the new "
        "database role and browser flows have never been tested. Are we production ready?",
        ("No. Record missing gates and test the release artifact",
         "Yes. Green means everything",
         "Ignore permission tests because they are slow"),
        1, "CI evidence is scoped to what actually ran at a particular commit. "
        "Operational, identity and migration checks remain separate gates."),
)


def rank(correct: int, total: int = len(INCIDENTS)) -> str:
    if type(correct) is not int or type(total) is not int or total < 1 or not 0 <= correct <= total:
        raise ValueError("score must be an integer within the total")
    if correct >= 7 and total >= 8:
        return "Systems Architect"
    if correct * 4 >= total * 3:
        return "Incident Investigator"
    if correct * 2 >= total:
        return "Curious Builder"
    return "Explorer"


def grade(answers: Iterable[int]) -> dict[str, object]:
    submitted = list(answers)
    if len(submitted) != len(INCIDENTS):
        raise ValueError("provide one answer per incident")
    if any(type(choice) is not int or choice not in (0, 1, 2, 3) for choice in submitted):
        raise ValueError("answers must be 0 to skip or 1, 2, 3")
    correct = sum(
        chosen == item.answer for chosen, item in zip(submitted, INCIDENTS)
    )
    return {
        "correct": correct,
        "total": len(INCIDENTS),
        "xp": correct * 10,
        "rank": rank(correct),
        "review_codes": [
            item.code for chosen, item in zip(submitted, INCIDENTS)
            if chosen != item.answer
        ],
    }


def play(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> dict[str, object] | None:
    """Run an interactive session. Quit is safe and writes no saved state."""
    output_fn("=== OMNIMASTER INCIDENT ACADEMY ===")
    output_fn("8 fictional engineering incidents. No network, account or tracking.")
    output_fn("Choose 1, 2 or 3. Enter 0 to skip, q to quit.")
    choices: list[int] = []
    for number, item in enumerate(INCIDENTS, 1):
        output_fn(f"\nCASE {number}/8 | {item.code} | {item.domain}")
        output_fn(item.scenario)
        for position, option in enumerate(item.options, 1):
            output_fn(f"  {position}. {option}")
        while True:
            try:
                typed = input_fn("Decision [1/2/3, 0 to skip, q to quit]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                output_fn("\nSession ended safely. Nothing was saved.")
                return None
            if typed == "q":
                output_fn("Session ended. Nothing was saved.")
                return None
            if typed in ("0", "1", "2", "3"):
                selected = int(typed)
                break
            output_fn("Please choose 0, 1, 2, 3 or q.")
        choices.append(selected)
        if selected == item.answer:
            output_fn("CORRECT | +10 XP")
        elif selected == 0:
            output_fn(f"SKIPPED | Correct choice: {item.answer}")
        else:
            output_fn(f"NOT QUITE | Correct choice: {item.answer}")
        output_fn("WHY: " + item.why)
    report = grade(choices)
    output_fn(f"\nCOMPLETE | {report['correct']}/{report['total']} | "
              f"{report['xp']} XP | RANK: {report['rank']}")
    if report["review_codes"]:
        output_fn("Revisit: " + ", ".join(report["review_codes"]))
    output_fn("Run it again, then explain the decisions in your own words.")
    return report


if __name__ == "__main__":
    play()
