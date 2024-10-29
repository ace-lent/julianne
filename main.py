from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Internal CSS for styling
CSS = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 20px;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    h2 {
        color: #333;
    }
    label {
        display: block;
        margin: 10px 0 5px;
    }
    input, select {
        padding: 10px;
        margin-bottom: 20px;
        width: 100%;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    button {
        padding: 10px;
        background-color: #5cb85c;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    button:hover {
        background-color: #4cae4c;
    }
    .result {
        margin-top: 20px;
        font-size: 1.2em;
        color: #333;
    }
</style>
"""

@app.get("/", response_class=HTMLResponse)
async def calculator_form():
    # HTML form embedded in the response
    html_content = f"""
    <html>
        <head>
            <title>Simple Calculator</title>
            {CSS}
        </head>
        <body>
            <h2>Calculator</h2>
            <form action="/calculate" method="post">
                <label for="a">First Number:</label>
                <input type="number" step="any" name="a" required><br>
                
                <label for="b">Second Number:</label>
                <input type="number" step="any" name="b" required><br>
                
                <label for="operation">Operation:</label>
                <select name="operation">
                    <option value="add">Add</option>
                    <option value="subtract">Subtract</option>
                    <option value="multiply">Multiply</option>
                    <option value="divide">Divide</option>
                </select><br>
                
                <button type="submit">Calculate</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(a: float = Form(...), b: float = Form(...), operation: str = Form(...)):
    # Performs the calculation based on the operation
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else HTTPException(status_code=400, detail="Cannot divide by zero")
    }
    
    result = operations.get(operation)
    if result is None:
        raise HTTPException(status_code=400, detail="Invalid operation")

    # Embedding the result in the HTML content
    html_content = f"""
    <html>
        <head>
            <title>Simple Calculator</title>
            {CSS}
        </head>
        <body>
            <h2>Calculator</h2>
            <form action="/calculate" method="post">
                <label for="a">First Number:</label>
                <input type="number" step="any" name="a" value="{a}" required><br>
                
                <label for="b">Second Number:</label>
                <input type="number" step="any" name="b" value="{b}" required><br>
                
                <label for="operation">Operation:</label>
                <select name="operation">
                    <option value="add" {"selected" if operation == "add" else ""}>Add</option>
                    <option value="subtract" {"selected" if operation == "subtract" else ""}>Subtract</option>
                    <option value="multiply" {"selected" if operation == "multiply" else ""}>Multiply</option>
                    <option value="divide" {"selected" if operation == "divide" else ""}>Divide</option>
                </select><br>
                
                <button type="submit">Calculate</button>
            </form>
            <div class="result">Result: {result}</div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
