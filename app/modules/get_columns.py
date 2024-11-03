from typing import Callable, List

def get_columns(table: str, connect: Callable[[], any]) -> List[str]:
    connection = connect()

    cursor = connection.cursor()

    sql = f"""
    SELECT COLUMN_NAME
    FROM ALL_TAB_COLUMNS
    WHERE TABLE_NAME = '{table}';
    """
    cursor.execute(sql)
    columns = [column[0] for column in cursor.fetchall()]
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    return columns
