import sqlite3

conn = sqlite3.connect("chinook.db")

def get_table_names(conn):
    """Return a list of table names."""
    table_names = []
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        table_names.append(table[0])
    return table_names


def get_column_names(conn, table_name):
    """Return a list of column names."""
    column_names = []
    columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    for col in columns:
        column_names.append(col[1])
    return column_names


def get_database_info(conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(conn):
        columns_names = get_column_names(conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts

database_schema_dict = get_database_info(conn)
database_schema_string = "\n".join(
    [
        f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
        for table in database_schema_dict
    ]
)

def pretty_print_conversation(messages):
    for message in messages:
        role = message["role"]
        content = message["content"]
        
        # 根据角色设置不同的颜色
        if role == "system":
            color = "\033[31m"  # 红色
        elif role == "user":
            color = "\033[32m"  # 绿色
        elif role == "assistant":
            color = "\033[34m"  # 蓝色
        elif role == "function":
            color = "\033[35m"  # 紫色
            # 特别处理函数调用的结果
            content = f"{message['name']}: {content}"
        else:
            color = "\033[0m"  # 默认颜色
        
        # 打印带颜色的消息
        print(f"{color}{role}: {content}\033[0m")
