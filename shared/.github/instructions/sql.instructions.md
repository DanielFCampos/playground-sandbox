---
applyTo: "**/*.sql"
description: "Use when writing, reviewing, or modifying SQL code. Covers style, naming, query structure, performance, and safety practices."
---
# SQL Coding Standards

## Style
- Use `UPPER CASE` for SQL keywords (`SELECT`, `FROM`, `WHERE`, `JOIN`, etc.)
- Use `snake_case` for table names, column names, and aliases
- Place each major clause (`SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`) on its own line
- Use trailing commas in multi-line `SELECT` lists
- Indent join conditions, subqueries, and `CASE` expressions consistently

## Naming
- Name tables as plural nouns: `users`, `orders`, `line_items`
- Name columns descriptively: `created_at`, `is_active`, `total_amount`
- Prefix boolean columns with `is_`, `has_`, or `should_`
- Name foreign keys as `<referenced_table_singular>_id` (e.g., `user_id`, `order_id`)
- Name indexes as `idx_<table>_<columns>` and constraints as `chk_`, `uq_`, `fk_` prefixes

## Query Structure
- Use explicit `JOIN` syntax over implicit joins in `WHERE` clauses
- Always specify the join type (`INNER JOIN`, `LEFT JOIN`); never use bare `JOIN` without intent
- Prefer `EXISTS` over `IN` for correlated subqueries
- Use CTEs (`WITH` clauses) over deeply nested subqueries for readability
- Qualify column names with table aliases in multi-table queries to avoid ambiguity

## Safety & Correctness
- Never use `SELECT *` in production queries; always list columns explicitly
- Always include a `WHERE` clause in `UPDATE` and `DELETE` statements
- Use parameterized queries or prepared statements — never interpolate user input into SQL strings
- Wrap multi-statement changes in transactions (`BEGIN` / `COMMIT` / `ROLLBACK`)
- Test destructive migrations with a rollback plan before applying to production

## Performance
- Add indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses
- Avoid functions on indexed columns in `WHERE` clauses — they prevent index usage
- Use `LIMIT` for queries that don't need full result sets
- Prefer `UNION ALL` over `UNION` when duplicates are acceptable
- Analyze query plans (`EXPLAIN` / `EXPLAIN ANALYZE`) for slow queries

## Migrations & Schema Changes
- Use incremental, versioned migration files
- Make migrations reversible — include both `up` and `down` steps
- Add columns as nullable or with defaults to avoid locking large tables
- Never rename or drop columns without a deprecation path
