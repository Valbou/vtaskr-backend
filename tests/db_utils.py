from sqlalchemy import text, TextClause


def text_query_table_exists() -> TextClause:
    return text(
        """
        SELECT EXISTS (
            SELECT FROM
                pg_tables
            WHERE
                schemaname = 'public' AND
                tablename  = :table
        );
        """
    )


def check_connection_query() -> TextClause:
    return text("SELECT 1;")
