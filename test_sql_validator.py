

from agents.sql_validator import execute_validated_query, validate_sql


TEST_CASES = [
    ("valid SELECT", "SELECT project_id FROM projects", True),
    ("DROP blocked", "DROP TABLE projects", False),
    ("DELETE blocked", "DELETE FROM projects", False),
    ("UPDATE blocked", "UPDATE projects SET name = 'x'", False),
    ("INSERT blocked", "INSERT INTO projects VALUES (1)", False),
    ("deleted_at allowed", "SELECT deleted_at FROM projects", True),
    (
        "stacked query with blocked keyword",
        "SELECT * FROM projects; DELETE FROM projects",
        False,
    ),
    (
        "stacked SELECT statements",
        "SELECT * FROM projects; SELECT * FROM invoices",
        False,
    ),
]


for name, query, expected in TEST_CASES:
    actual, reason = validate_sql(query)
    assert actual == expected, f"{name} failed: {reason}"
    print(f"PASS: {name}")


class FakeCursor:
    def __init__(self):
        self.execute_count = 0

    def execute(self, query, parameters=None):
        self.execute_count += 1

    def fetchall(self):
        return []

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_count = 0
        self.cursor_instance = FakeCursor()

    def cursor(self):
        self.cursor_count += 1
        return self.cursor_instance


connection = FakeConnection()

try:
    execute_validated_query(
        connection,
        "SELECT * FROM projects; SELECT * FROM invoices",
    )
    raise AssertionError("Unsafe query was not rejected.")
except ValueError:
    pass

assert connection.cursor_count == 0
assert connection.cursor_instance.execute_count == 0
print("PASS: rejected query never reached the database.")

print("Step 5 passed.")
