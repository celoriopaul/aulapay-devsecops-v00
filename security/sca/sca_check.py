"""
Control SCA reproducible para el escenario academico AulaPay.

El escenario proporciona una dependencia y vulnerabilidad simuladas.
Este control permite representar el hallazgo de forma automatizable
sin incorporar una dependencia inexistente al entorno Python real.
"""

import json
import sys
from pathlib import Path


MANIFEST_PATH = Path("/workspace/security/sca/dependencies.json")


def load_manifest() -> dict:
    """Carga el manifiesto de dependencias del escenario."""

    with MANIFEST_PATH.open(
        mode="r",
        encoding="utf-8",
    ) as manifest_file:
        return json.load(manifest_file)


def evaluate_dependencies(manifest: dict) -> list[dict]:
    """Identifica dependencias vulnerables declaradas en el escenario."""

    findings = []

    for dependency in manifest.get("dependencies", []):
        vulnerability = dependency.get("vulnerability")

        if vulnerability:
            findings.append(dependency)

    return findings


def main() -> int:
    """Ejecuta el control SCA y devuelve estado de gate."""

    manifest = load_manifest()
    findings = evaluate_dependencies(manifest)

    print("AulaPay DevSecOps - SCA")
    print("=" * 50)
    print(f"Component: {manifest.get('component')}")
    print(f"Dependencies analyzed: {len(manifest.get('dependencies', []))}")
    print(f"Vulnerable dependencies: {len(findings)}")
    print()

    for finding in findings:
        print(f"Dependency: {finding['name']} {finding['version']}")
        print(f"Vulnerability: {finding['vulnerability']}")
        print(f"Severity: {finding['severity']}")
        print(f"Fixed version: {finding['fixed_version']}")
        print(f"Usage: {finding['usage']}")
        print(f"Simulated: {finding['simulated']}")
        print("Status: VULNERABLE")
        print("-" * 50)

    if findings:
        print("SCA RESULT: FAIL")
        return 1

    print("SCA RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())