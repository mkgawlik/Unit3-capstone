
from agents.tools_registry import TOOL_REGISTRY


EXPECTED_TOOLS = {"sql_agent", "retrieval_agent"}

assert set(TOOL_REGISTRY) == EXPECTED_TOOLS, (
    f"Expected {EXPECTED_TOOLS}, found {set(TOOL_REGISTRY)}"
)

for tool_name, tool_config in TOOL_REGISTRY.items():
    assert callable(tool_config["handler"]), (
        f"{tool_name} must have a callable handler"
    )
    description = tool_config["description"]
    assert isinstance(description, str) and description.strip(), (
        f"{tool_name} must have a non-empty description"
    )
    assert "Use" in description, f"{tool_name} needs a purpose"
    assert "Do not use" in description, f"{tool_name} needs an exclusion"

print("Step 3 passed: registry tools and descriptions are valid.")
