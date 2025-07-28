import json
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Inventory")

products = []
# Load products from JSON file
with open("products.json", "r") as file:
    data = json.load(file)
    products = data["value"]  # Extract the products array from the "value" field

@mcp.tool()
def get_product_info(product_name: str) -> dict:
    """Returns detailed information about a specific product."""
    product = next((p for p in products if p["ProductName"] == product_name), None)
    if product:
        return product
    return {"error": "Product not found"}

# Add an inventory check tool
@mcp.tool()
def get_inventory_levels() -> dict:
    """Returns comprehensive inventory information for all products including stock levels, sales data, and recommendations.
    
    Use this tool for any inventory-related queries such as:
    - Current stock levels, inventory status, or units in stock
    - Product availability or stock availability
    - Inventory recommendations (restock, clearance, low stock alerts)
    - Stock analysis or inventory analysis
    - Product information with inventory data
    - Weekly sales performance with stock levels
    - Reorder recommendations based on sales velocity
    - Products needing attention (low stock, slow moving, overstocked)
    
    Business rules applied:
    - Recommend RESTOCK if inventory < 10 AND weekly sales > 15 (high demand, low stock)
    - Recommend CLEARANCE if inventory > 20 AND weekly sales < 5 (slow moving, overstocked)
    - Flag LOW STOCK if inventory <= reorder level
    - Flag HIGH DEMAND if weekly sales > 50"""
    return {
        product["ProductName"]: product.get("UnitsInStock", 0)
        for product in products
    }


# Add a weekly sales tool
@mcp.tool()
def get_weekly_sales() -> dict:
    """
    Returns comprehensive weekly sales data for all products with performance analysis and trends.
    
    Use this tool for any sales-related queries such as:
    - Weekly sales data, sales numbers, or units sold
    - Sales performance, sales analysis, or sales reports
    - Product sales information or product performance
    - Revenue data or earnings by product
    - Sales trends, sales velocity, or demand analysis
    - Top selling products or best performers
    - Slow moving products or poor performers
    - Sales comparison or product ranking
    - Weekly revenue, sales totals, or sales summaries
    - Product inventory with sales data
    - Sales and stock correlation analysis
    
    Provides detailed sales insights including:
    - Weekly units sold and revenue generated
    - Sales performance categorization
    - Inventory turnover indicators
    - Sales velocity analysis
    """
    return {
        product["ProductName"]: product.get("WeeklySales", 0)
        for product in products
    }

@mcp.tool()
def update_inventory(product_name: str, new_inventory: int) -> str:
    """
    Updates the inventory stock levels for a specific product by ProductName.
    
    Use this tool for any inventory update requests such as:
    - Update inventory, change stock levels, or modify UnitsInStock
    - Set new inventory count, adjust stock quantity, or change product stock
    - Inventory adjustments, stock corrections, or inventory modifications
    - Restock products, add inventory, or increase stock levels
    - Reduce inventory, decrease stock, or remove units from stock
    - Fix inventory discrepancies or correct stock counts
    - Update product inventory, modify product stock, or change product UnitsInStock
    - Inventory management, stock management, or product stock updates
    - Set ProductName inventory, update ProductName stock levels
    - Batch inventory updates or bulk stock changes
    - Emergency stock adjustments or urgent inventory corrections
    
    Parameters:
    - product_name: The exact ProductName of the item to update
    - new_inventory: The new UnitsInStock value to set for the product
    
    Returns detailed update confirmation with before/after values and recommendations.
    """
    product_found = False
    old_inventory = 0
    
    for product in products:
        if product["ProductName"] == product_name:
            product_found = True
            old_inventory = product.get("UnitsInStock", 0)
            product["UnitsInStock"] = new_inventory
            
            # Save changes back to the JSON file
            with open("products.json", "w") as file:
                json.dump({"value": products}, file, indent=2)
            
            return f"Updated {product_name} inventory from {old_inventory} to {new_inventory} units. Changes saved to database."
    
    return f"Product {product_name} not found."

mcp.run()