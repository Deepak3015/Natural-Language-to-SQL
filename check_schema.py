from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    tables = conn.execute(text("SHOW TABLES")).fetchall()
    print("Tables:", [t[0] for t in tables])

    for t in tables:
        name = t[0]
        print(f"\n--- {name} ---")
        cols = conn.execute(text(f"SHOW COLUMNS FROM {name}")).fetchall()
        for c in cols:
            print(f"  {c[0]} ({c[1]}) {'PK' if c[3] == 'PRI' else ''}")

        fks = conn.execute(text(f"""
            SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = 'sqlmind' AND TABLE_NAME = '{name}'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)).fetchall()
        for fk in fks:
            print(f"  FK: {fk[0]} -> {fk[1]}.{fk[2]}")
