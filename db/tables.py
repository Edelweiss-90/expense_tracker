from utils.constants import DeletedStatuses, TableName

user = f"""
    CREATE TABLE IF NOT EXISTS {TableName.USER.value} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE, 
        password TEXT,
        deleted_status TEXT DEFAULT '{DeletedStatuses.NOT_DELETED.value}' NOT NULL
        )
"""

category = f"""
    CREATE TABLE IF NOT EXISTS {TableName.CATEGORY.value} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT, 
        deleted_status TEXT DEFAULT '{DeletedStatuses.NOT_DELETED.value}' NOT NULL,
        FOREIGN KEY (user_id) REFERENCES {TableName.USER.value} (id)
        )
"""

transaction = f"""
    CREATE TABLE IF NOT EXISTS "{TableName.TRANSACTION.value}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        amount INTEGER NOT NULL, 
        transaction_date TEXT DEFAULT (datetime('now', 'localtime')),
        deleted_status TEXT DEFAULT '{DeletedStatuses.NOT_DELETED.value}' NOT NULL,
        FOREIGN KEY (user_id) REFERENCES "{TableName.USER.value}" (id),
        FOREIGN KEY (category_id) REFERENCES "{TableName.CATEGORY.value}" (id)
    )
"""
