from agents.sql_agent import run_sql_agent
from agents.retrieval_agent import run_retrieval_agent

EXPECTED_KEYS = {"success", "answer", "sources", "metadata"}


def check_result(agent_name, result):
    assert set(result.keys()) == EXPECTED_KEYS, (
        f"{agent_name} returned incorrect keys: {result.keys()}"
    )
    assert isinstance(result["success"], bool)
    assert isinstance(result["answer"], str)
    assert isinstance(result["sources"], list)
    assert isinstance(result["metadata"], dict)
    print(f"{agent_name}: standardized response passed")


sql_result = run_sql_agent("How many active projects are there?")
retrieval_result = run_retrieval_agent(
    "What information is available in the project documents?"
)

check_result("SQL agent", sql_result)
check_result("Retrieval agent", retrieval_result)

print("TRUE PASS: both agents return standardized results.")
