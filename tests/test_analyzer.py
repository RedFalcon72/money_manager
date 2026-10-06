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