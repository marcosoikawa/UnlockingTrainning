import json
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Inventory")

products = []
# Load products from JSON file
with open("products.json", "r") as file:
    data = json.load(file)
    products = data["value"]  # Extract the products array from the "value" field


# Add an inventory check tool
@mcp.tool()
def get_inventory_levels() -> dict:
    """
    Returns current inventory for all products.
    - Recommend restock if item inventory < 10  and weekly sales > 15
    - Recommend clearance if item inventory > 20 and weekly sales < 5
    """
    return {
        product["ProductName"]: product.get("UnitsInStock", 0)
        for product in products
    }


# Add a weekly sales tool
@mcp.tool()
def get_weekly_sales() -> dict:
    """Returns number of units sold last week."""
    return {
        product["ProductName"]: product.get("WeeklySales", 0)
        for product in products
    }

mcp.run()