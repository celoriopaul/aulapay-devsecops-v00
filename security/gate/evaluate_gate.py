"""
Security Gate del proyecto AulaPay DevSecOps.

Evalua los hallazgos normalizados obtenidos por los controles de
seguridad y determina si el baseline puede continuar en el pipeline.

Exit codes:
    0 -> PASS
    1 -> BLOCK
    2 -> ERROR
"""

import json
import sys
from pathlib import Path


BASE_PATH = Path("/workspace/security/gate")
POLICY_PATH = BASE_PATH / "gate-policy.json"
FINDINGS_PATH = BASE_PATH / "before-findings.json"


def load_json(path: Path) -> dict:
    """Carga un documento JSON."""

    with path.open(
        mode="r",
        encoding="utf-8",
    ) as json_file:
        return json.load(json_file)


def evaluate_findings(
    policy: dict,
    findings: list[dict],
) -> tuple[bool, list[str]]:
    """
    Evalua los hallazgos según la política del proyecto.

    Retorna:
        blocked: indica si el pipeline debe bloquearse.
        reasons: razones técnicas de la decisión.
    """

    blocked = False
    reasons = []

    blocking_policy = policy["blocking_policy"]

    for finding in findings:
        finding_id = finding["id"]
        severity = finding["severity"]
        status = finding["status"]
        decision = finding["decision"]
        control = finding["control"]

        if (
            severity == "CRITICAL"
            and status == "CONFIRMED"
            and blocking_policy["critical_confirmed"]
        ):
            blocked = True
            reasons.append(
                f"{finding_id}: CRITICAL confirmado."
            )

        if (
            severity == "HIGH"
            and status == "CONFIRMED"
            and blocking_policy["high_confirmed"]
        ):
            blocked = True
            reasons.append(
                f"{finding_id}: HIGH confirmado."
            )

        if (
            control == "API_SECURITY"
            and status == "CONFIRMED"
            and decision == "UNRESOLVED"
            and blocking_policy["api_authorization_failure"]
        ):
            blocked = True
            reasons.append(
                f"{finding_id}: fallo de autorizacion API no resuelto."
            )

        if (
            control == "SECRET_SCAN"
            and status == "CONFIRMED_REAL_SECRET"
            and decision != "FIXED"
            and blocking_policy["unresolved_real_secret"]
        ):
            blocked = True
            reasons.append(
                f"{finding_id}: secreto real no resuelto."
            )

    return blocked, reasons


def main() -> int:
    """Ejecuta la evaluación completa del Security Gate."""

    try:
        policy = load_json(POLICY_PATH)
        assessment = load_json(FINDINGS_PATH)
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print(f"Security Gate configuration error: {error}")
        return 2

    findings = assessment.get("findings", [])

    print("AulaPay DevSecOps - Security Gate")
    print("=" * 60)
    print(f"Policy: {policy['policy_name']}")
    print(f"Policy version: {policy['version']}")
    print(f"Assessment: {assessment.get('assessment')}")
    print(f"Findings evaluated: {len(findings)}")
    print()

    for finding in findings:
        print(
            f"{finding['id']} | "
            f"{finding['control']} | "
            f"{finding['severity']} | "
            f"{finding['status']} | "
            f"{finding['decision']}"
        )

    blocked, reasons = evaluate_findings(
        policy=policy,
        findings=findings,
    )

    print()
    print("Gate evaluation")
    print("-" * 60)

    if blocked:
        for reason in reasons:
            print(f"BLOCK: {reason}")

        print()
        print("FINAL GATE DECISION: BLOCK")
        return 1

    print("No blocking conditions detected.")
    print()
    print("FINAL GATE DECISION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())