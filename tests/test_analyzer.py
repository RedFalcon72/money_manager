from tracker import database


def test_update_category_updates_target_even_if_already_categorized(tmp_path, monkeypatch):
    db_path = tmp_path / "money.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)
    database.init_db()

    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO transactions (date, amount, description, source, category)
            VALUES
                ('2026-01-01', -1000, 'コンビニ', 'a.csv', '食費'),
                ('2026-01-02', -500, 'コンビニ', 'b.csv', '未分類'),
                ('2026-01-03', -300, 'コンビニ', 'c.csv', '交通費')
            """
        )

    database.update_category(1, "日用品")

    with database.get_connection() as conn:
        rows = conn.execute(
            "SELECT id, category FROM transactions ORDER BY id"
        ).fetchall()

    assert rows == [(1, "日用品"), (2, "日用品"), (3, "交通費")]


def test_category_summary_keeps_previous_category_after_last_transaction_moves(
    tmp_path, monkeypatch
):
    db_path = tmp_path / "money.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)
    database.init_db()

    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO transactions (date, amount, description, source, category)
            VALUES ('2026-01-01', -1000, '税務署', 'a.csv', '税金')
            """
        )
        conn.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            ("税金",)
        )

    database.update_category(1, "交通費")

    assert database.get_category_summary("2026-01-01", "2026-01-31") == [
        {"category": "交通費", "total": -1000},
        {"category": "税金", "total": 0},
    ]