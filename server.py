import os
from fastmcp import FastMCP
from tools import (
    get_credit_hours,
    grade_to_points,
    calculate_cgpa,
    required_gpa,
    check_target,
)

mcp = FastMCP("cgpa")

# turn every function into an MCP tool
mcp.tool(get_credit_hours)
mcp.tool(grade_to_points)
mcp.tool(calculate_cgpa)
mcp.tool(required_gpa)
mcp.tool(check_target)

if __name__ == "__main__":
    # Hosting services (like Render) give the port in the PORT env variable.
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
    mcp.run(transport="http", host=host, port=port, path="/mcp")  # http://127.0.0.1:8000/mcp
