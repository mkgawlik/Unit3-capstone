
import re
from typing import Any


BLOCKED_PATTERN = re.compile(
    r"\b(?:DROP|DELETE|UPDATE|INSERT)\b",
    re.IGNORECASE,
)


def validate_sql(query: str) -> tuple[bool, str]:
    if not isinstance(query, str) or not query.strip():
        return False, "SQL query is empty."

    statement = query.strip()

    # Allow one trailing semicolon, but reject all other semicolons.
    body = statement[:-1].rstrip() if statement.endswith(";") else statement

    if ";" in body:
        return False, "Multiple SQL statements are not allowed."

    blocked_match = BLOCKED_PATTERN.search(body)
    if blocked_match:
        return False, f"Blocked SQL keyword: {blocked_match.group(0)}"

    if not re.match(r"^SELECT\b", body, re.IGNORECASE):
        return False, "Only SELECT statements are allowed."

    return True, "Valid SELECT statement."


def execute_validated_query(
    connection: Any,
    query: str,
    parameters: Any = None,
) -> list[Any]:
    allowed, reason = validate_sql(query)

    if not allowed:
        raise ValueError(f"SQL rejected: {reason}")

    cursor = connection.cursor()

    try:
        if parameters is None:
            cursor.execute(query)
        else:
            cursor.execute(query, parameters)

        return cursor.fetchall()
    finally:
        cursor.close()
