"""
FastMango MCP Demo Application
"""

from fastmango import MangoApp
from fastmango.mcp import MCPConfig

# Create MCP configuration
mcp_config = MCPConfig(
    name="FastMango MCP Demo",
    version="1.0.0",
    enable_dashboard=True,
    enable_health_check=True,
    enable_swagger=True,
)

# Create FastMango app with MCP support
app = MangoApp(mcp_config=mcp_config)

# Define MCP tools
@app.mcp_tool()
async def get_weather(city: str, units: str = "metric") -> dict:
    """
    Get current weather information for a city.
    
    Args:
        city: Name of the city
        units: Temperature units (metric, imperial, kelvin)
    
    Returns:
        Weather data including temperature, condition, and humidity
    """
    # Mock weather data
    import random
    
    conditions = ["sunny", "cloudy", "rainy", "snowy"]
    temperature = random.randint(-10, 30) if units == "metric" else random.randint(14, 86)
    
    return {
        "city": city,
        "temperature": temperature,
        "condition": random.choice(conditions),
        "humidity": random.randint(30, 90),
        "units": units
    }


@app.mcp_tool()
async def calculate(expression: str) -> dict:
    """
    Calculate the result of a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4")
    
    Returns:
        The result of the calculation
    """
    try:
        # Simple and safe evaluation
        import ast
        import operator
        
        # Define allowed operators
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        
        def eval_expr(node):
            if isinstance(node, ast.Num):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                left = eval_expr(node.left)
                right = eval_expr(node.right)
                return operators[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                operand = eval_expr(node.operand)
                return operators[type(node.op)](operand)
            else:
                raise TypeError(f"Unsupported type: {type(node)}")
        
        result = eval_expr(ast.parse(expression, mode='eval').body)
        
        return {
            "expression": expression,
            "result": result,
            "success": True
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e),
            "success": False
        }


@app.mcp_tool()
async def generate_joke(topic: str = "programming") -> dict:
    """
    Generate a joke about a specific topic.
    
    Args:
        topic: Topic for the joke (e.g., programming, science, animals)
    
    Returns:
        A joke about the specified topic
    """
    # Mock joke generation
    jokes = {
        "programming": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why do Java developers wear glasses? Because they don't C#.",
            "How many programmers does it take to change a light bulb? None. It's a hardware problem."
        ],
        "science": [
            "Why did the biologist break up with the physicist? They had no chemistry.",
            "Why can't you trust an atom? Because they make up everything.",
            "Why did the scarecrow win an award? He was outstanding in his field."
        ],
        "animals": [
            "Why don't scientists trust atoms? Because they make up everything.",
            "What do you call a fake noodle? An impasta.",
            "Why did the scarecrow win an award? He was outstanding in his field."
        ]
    }
    
    import random
    
    if topic not in jokes:
        topic = "programming"
    
    joke = random.choice(jokes[topic])
    
    return {
        "topic": topic,
        "joke": joke
    }


# Define regular API endpoints
@app.get("/")
async def root():
    return {"message": "FastMango MCP Demo Application"}


@app.get("/info")
async def info():
    return {
        "name": "FastMango MCP Demo",
        "version": "1.0.0",
        "mcp_dashboard": "/mcp-dashboard",
        "health_check": "/health",
        "swagger_docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)