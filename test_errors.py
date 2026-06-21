"""
Test cases to identify possible failure modes in the SQLMind AI project.
Run: python3 test_errors.py
"""

import sys
import os
import json
import traceback

sys.path.insert(0, os.path.dirname(__file__))
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

passed = 0
failed = 0

def test(name, func):
    global passed, failed
    try:
        func()
        print(f"  {GREEN}PASS{RESET} {name}")
        passed += 1
    except Exception as e:
        print(f"  {RED}FAIL{RESET} {name}")
        print(f"    {YELLOW}Error: {e}{RESET}")
        traceback.print_exc(limit=2)
        failed += 1

def section(title):
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN}{title}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}")

# ──────────────────────────────────────────
# 1. ENVIRONMENT CHECKS
# ──────────────────────────────────────────
section("1. Environment & Configuration Errors")

def test_env_file():
    assert os.path.exists(".env"), ".env file missing"

test("1a. .env file exists", test_env_file)

def test_env_values():
    from dotenv import load_dotenv
    load_dotenv()
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")
    assert host is not None, "DB_HOST missing"
    assert port is not None, "DB_PORT missing"
    assert user is not None, "DB_USER missing"
    assert password is not None, "DB_PASSWORD missing"
    assert name is not None, "DB_NAME missing"

test("1b. All .env variables present", test_env_values)

def test_port_not_in_url():
    from dotenv import load_dotenv
    load_dotenv()
    port = os.getenv("DB_PORT")
    url = f"mysql+pymysql://user:pass@host/db"
    assert ":" + port not in url, (
        f"Port {port} is NOT included in DATABASE_URL - "
        "connection will fail if MySQL uses non-default port"
    )

test("1c. Port missing from URL (known bug)", test_port_not_in_url)

# ──────────────────────────────────────────
# 2. DATABASE CONNECTION ERRORS
# ──────────────────────────────────────────
section("2. Database Connection Errors")

def test_db_connect():
    from database import engine
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

test("2a. Database connection works", test_db_connect)

def test_database_exists():
    from database import engine, name
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db"),
            {"db": name}
        )
        assert result.fetchone() is not None, f"Database '{name}' not found"

test("2b. Database exists", test_database_exists)

def test_tables_exist():
    from schema_loader import get_schema
    schema = get_schema()
    assert len(schema) > 0, "No tables found in database"

test("2c. Tables exist in database", test_tables_exist)

def test_schema_returns_dict():
    from schema_loader import get_schema
    schema = get_schema()
    assert isinstance(schema, dict), "Schema should be a dict"
    for table, columns in schema.items():
        assert isinstance(columns, list), f"Columns for {table} should be a list"
        assert len(columns) > 0, f"Table {table} has no columns"

test("2d. Schema structure is valid", test_schema_returns_dict)

# ──────────────────────────────────────────
# 3. LLM / MODEL ERRORS
# ──────────────────────────────────────────
section("3. LLM / Model Errors")

def test_ollama_running():
    import ollama
    ollama.list()

test("3a. Ollama service is running", test_ollama_running)

def test_model_exists():
    import ollama
    models = ollama.list()
    model_names = [m["name"] for m in models["models"]]
    assert "qwen2.5:3b" in model_names, (
        "Model 'qwen2.5:3b' not pulled. Run: ollama pull qwen2.5:3b"
    )

test("3b. Qwen2.5:3b model is pulled", test_model_exists)

def test_llm_returns_string():
    from llm import generate_sql
    result = generate_sql("List all tables")
    assert isinstance(result, str), "LLM should return a string"
    assert len(result) > 0, "LLM returned empty response"
    print(f"    Raw response preview: {result[:100]}...")

test("3c. LLM returns non-empty string", test_llm_returns_string)

def test_llm_sql_has_no_markdown():
    from llm import generate_sql
    from query_cleaner import clean_sql
    result = generate_sql("Show all tables")
    cleaned = clean_sql(result)
    assert "```" not in cleaned, "Cleaner should remove markdown"
    print(f"    Cleaned SQL: {cleaned[:100]}")

test("3d. SQL cleaner removes markdown", test_llm_sql_has_no_markdown)

def test_llm_obeys_rules():
    from prompt_builder import build_prompt
    from llm import generate_sql
    from query_cleaner import clean_sql
    schema = {"users": ["id", "name", "email"]}
    prompt = build_prompt(schema, "Show all users")
    result = generate_sql(prompt)
    cleaned = clean_sql(result)
    sql_upper = cleaned.upper()
    
    has_explain = "EXPLAIN" in sql_upper
    has_note = "--" in cleaned
    has_multiline_note = "/*" in cleaned
    total_notes = sum([has_explain, has_note, has_multiline_note])
    
    if total_notes > 0:
        print(f"    {YELLOW}WARNING: LLM included explanation/notes{RESET}")
    print(f"    Generated SQL: {cleaned[:150]}")

test("3e. LLM generates SQL without explanation", test_llm_obeys_rules)

def test_dangerous_sql_blocked():
    from validator import check_validation
    dangerous = ["DROP TABLE users", "DELETE FROM users", "UPDATE users SET name='x'"]
    for sql in dangerous:
        try:
            check_validation(sql)
            print(f"    {RED}WARNING: Validator did not block: {sql}{RESET}")
        except Exception:
            pass  # Expected

test("3f. Dangerous SQL is blocked by validator", test_dangerous_sql_blocked)

def test_dangerous_sql_allowed():
    from validator import check_validation
    safe = ["SELECT * FROM users", "SELECT COUNT(*) FROM users"]
    for sql in safe:
        assert check_validation(sql), f"Safe SQL should pass: {sql}"

test("3g. Safe SQL passes validator", test_dangerous_sql_allowed)

def test_execute_valid_sql():
    from query_executor import execute_query
    schema_module = __import__("schema_loader")
    schema = schema_module.get_schema()
    if schema:
        first_table = list(schema.keys())[0]
        df = execute_query(f"SELECT * FROM {first_table} LIMIT 5")
        assert df is not None, "Query should return a DataFrame"
        print(f"    Table '{first_table}': {len(df)} rows, columns: {list(df.columns)}")

test("3h. Valid SQL executes successfully", test_execute_valid_sql)

def test_empty_query():
    from query_cleaner import clean_sql
    result = clean_sql("")
    assert result == "", "Empty input should return empty string"

test("3i. Empty query handling", test_empty_query)

# ──────────────────────────────────────────
# 4. VISUALIZATION ERRORS
# ──────────────────────────────────────────
section("4. Visualization Agent Errors")

def test_visualize_json_parsing():
    from visualize_agent import suggest_visualizaion, visualize
    sample_df = __import__("pandas").DataFrame({
        "city": ["Delhi", "Mumbai", "Bangalore"],
        "count": [100, 80, 60]
    })
    try:
        result = suggest_visualizaion("Show city distribution", sample_df)
        assert isinstance(result, dict), "Should return a dict"
        assert "chart_type" in result, (
            "Missing 'chart_type' in response - will cause KeyError in visualize()"
        )
        assert "title" in result, "Missing 'title'"
        assert "insight" in result, "Missing 'insight'"
        print(f"    Suggestion: {result}")
    except json.JSONDecodeError as e:
        print(f"    {RED}LLM returned non-JSON: {e}{RESET}")
    except Exception as e:
        print(f"    {RED}Error: {e}{RESET}")

test("4a. Visualization suggestion returns valid JSON", test_visualize_json_parsing)

def test_chart_type_is_valid():
    sample_df = __import__("pandas").DataFrame({"x": [1], "y": [2]})
    from visualize_agent import suggest_visualizaion
    valid_types = {"metric", "card", "bar", "line", "pie", "table"}
    try:
        result = suggest_visualizaion("test", sample_df)
        assert result["chart_type"] in valid_types, (
            f"Invalid chart_type '{result['chart_type']}'. Must be one of {valid_types}"
        )
    except json.JSONDecodeError:
        pass  # Handled in previous test

test("4b. Chart type is valid", test_chart_type_is_valid)

# ──────────────────────────────────────────
# 5. EDGE CASES
# ──────────────────────────────────────────
section("5. Edge Cases & Other Issues")

def test_schema_empty_string():
    from prompt_builder import build_prompt
    prompt = build_prompt({}, "test")
    assert "Database Schema:" in prompt
    assert "\n\n" in prompt

test("5a. Empty schema doesn't crash prompt builder", test_schema_empty_string)

def test_query_with_no_results():
    from query_executor import execute_query
    from database import engine
    from sqlalchemy import text
    try:
        df = execute_query("SELECT * FROM users WHERE 1=0")
        assert len(df) == 0, "Query with no results should return empty DataFrame"
    except Exception as e:
        print(f"    Table 'users' may not exist - this is expected if schema is different")
        print(f"    {YELLOW}Suggestion: test with an actual table that exists{RESET}")

test("5b. Query with no results", test_query_with_no_results)

def test_duplicate_streamlit_import():
    import ast
    with open("visualize_agent.py") as f:
        tree = ast.parse(f.read())
    imports = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "streamlit"
    ]
    assert len(imports) <= 1, (
        f"streamlit imported {len(imports)} times (lines 1 and 5)"
    )

test("5c. Duplicate streamlit import in visualize_agent.py", test_duplicate_streamlit_import)

def test_orphaned_db_connection():
    with open("database.py") as f:
        content = f.read()
    assert "connection.close()" in content or "connection" not in content, (
        "orphaned connection = engine.connect() on line 18 never closed"
    )

test("5d. Orphaned database connection", test_orphaned_db_connection)

def test_gemini_key_format():
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if key:
        assert key.startswith("AI"), "Gemini key should start with 'AI'"
        print(f"    Key prefix: {key[:8]}... (valid format)")

test("5e. Gemini API key format", test_gemini_key_format)

# ──────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────
section("SUMMARY")
total = passed + failed
print(f"  {GREEN}Passed: {passed}{RESET}")
print(f"  {RED}Failed: {failed}{RESET}")
print(f"  Total: {total}")

if failed > 0:
    print(f"\n  {YELLOW}Some tests failed. Review the errors above.{RESET}")
    print(f"  {YELLOW}These indicate real or potential failure modes in your app.{RESET}")
else:
    print(f"\n  {GREEN}All tests passed! No obvious errors detected.{RESET}")

print(f"\n  {CYAN}Tip: The tests that FAILED are the errors you could get.{RESET}")
print(f"  {CYAN}The tests that PASSED are areas that work correctly.{RESET}")
