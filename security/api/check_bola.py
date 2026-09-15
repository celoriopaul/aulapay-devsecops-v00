"""
Prueba automatizada de autorizacion a nivel de objeto para AulaPay.

Escenario:
- El estudiante 1024 se autentica correctamente.
- Intenta consultar los pagos pertenecientes al estudiante 2048.
- Una implementacion segura debe responder HTTP 403 Forbidden.

Durante el baseline vulnerable se espera HTTP 200, por lo que
este control debe finalizar con FAIL.
"""

import json
import sys
import urllib.error
import urllib.request


API_BASE_URL = "http://host.docker.internal:8000/api/v1"

AUTHENTICATED_STUDENT = "1024"
TARGET_STUDENT = "2048"
AUTH_TOKEN = "student-1024-token"

EXPECTED_STATUS = 403


def execute_authorization_test() -> tuple[int, str]:
    """Ejecuta la solicitud de acceso cruzado."""

    url = f"{API_BASE_URL}/payments/{TARGET_STUDENT}"

    request = urllib.request.Request(
        url=url,
        method="GET",
        headers={
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as response:
            body = response.read().decode("utf-8")
            return response.status, body

    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        return error.code, body


def main() -> int:
    """Evalua si existe autorizacion adecuada sobre el recurso."""

    print("AulaPay DevSecOps - API Authorization Test")
    print("=" * 55)
    print(f"Authenticated student: {AUTHENTICATED_STUDENT}")
    print(f"Requested student: {TARGET_STUDENT}")
    print(f"Expected HTTP status: {EXPECTED_STATUS}")
    print()

    try:
        actual_status, response_body = execute_authorization_test()
    except Exception as error:
        print(f"Test execution error: {error}")
        print("API SECURITY RESULT: ERROR")
        return 2

    print(f"Actual HTTP status: {actual_status}")

    try:
        parsed_body = json.loads(response_body)
        print(
            "Response body:",
            json.dumps(
                parsed_body,
                ensure_ascii=False,
            ),
        )
    except json.JSONDecodeError:
        print(f"Response body: {response_body}")

    print()

    if actual_status == EXPECTED_STATUS:
        print("Object-level authorization: ENFORCED")
        print("API SECURITY RESULT: PASS")
        return 0

    print("Object-level authorization: NOT ENFORCED")
    print("Finding: BOLA/IDOR")
    print("Severity: CRITICAL")
    print("Status: CONFIRMED")
    print("API SECURITY RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())