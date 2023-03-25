from sqlalchemy import TextClause, text


def text_query_table_exists() -> TextClause:
    return text(
        """
        SELECT EXISTS (
            SELECT * FROM
                pg_tables
            WHERE
                schemaname = 'public' AND
                tablename  = :table
        );
        """
    )


def text_query_column_exists() -> TextClause:
    return text(
        """
        SELECT EXISTS (
            SELECT * FROM
                information_schema.columns
            WHERE
                table_name = :table AND
                column_name = :column
        );
        """
    )


def check_connection_query() -> TextClause:
    return text("SELECT 1;")
