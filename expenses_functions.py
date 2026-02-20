import sqlite3
from enum import Enum
from datetime import datetime


class TableName(Enum):
    MOVEMENT = 'movement'
    DEBT_CRED = 'debt_cred'
    EXPENSES_RECAP = 'expenses_recap'
    EXPENSES_MONTH_RECAP = 'month_recap'
    DEBT_CRED_RECAP = 'debt_cred_recap'

class Operations(Enum):
    MODIFY = 'modify'
    DELETE = 'delete'

class MovementTypes(Enum):
    ENTRY = 'entrata'
    EXIT = 'uscita'
    CRED = 'credito'
    DEBT = 'debito'

class DatabaseManager:
    def __init__(self, methods_of_payment, categories) -> None:
        """This function initializes the database."""

        self.MOVEMENT_TAGS = {
            'date' : 'TEXT',
            'category' : 'TEXT',
            'description' : 'TEXT',
            'method' : 'TEXT',
            'amount' : 'REAL',
            'type' : 'TEXT'
        }
        
        self.DEBT_CRED_TAGS = {
            'date' : 'TEXT',
            'category' : 'TEXT',
            'description' : 'TEXT',
            'subject' : 'TEXT',
            'amount' : 'REAL',
            'paid' : 'REAL',
            'due' : 'REAL',
            'type' : 'TEXT'
        }

        self.DEBT_CRED_RECAP_TAGS = {
            'Subject': 'TEXT',
            'Status': 'TEXT',
            'Amount': 'REAL',
        }
        
        self.METHODS_OF_PAYMENT = methods_of_payment
        self.CATEGORIES = categories

    # --- Accessor Methods ---

    def get_movement_tags(self) -> dict:
        return self.MOVEMENT_TAGS
    
    def get_debt_cred_tags(self) -> dict:
        return self.DEBT_CRED_TAGS
    
    def get_debt_cred_recap_tags(self) -> dict:
        return self.DEBT_CRED_RECAP_TAGS
    
    def get_methods_of_payment(self) -> list:
        return self.METHODS_OF_PAYMENT
    
    def get_categories(self) -> list:
        return self.CATEGORIES



# --- Principal -----------------------------------------------------------

'''This function initialize the database. It creates all the needed tables.'''
def create_table(manager: DatabaseManager, cursor: sqlite3.Cursor, table: TableName, index: int = 1) -> str:
    match table:
        case TableName.MOVEMENT:
            # Table movements
            movement_columns = ", ".join([f"{key} {value}" for key, value in manager.get_movement_tags().items()])
            cursor.execute(f'''
                create TABLE IF NOT EXISTS {TableName.MOVEMENT.value}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {movement_columns}
                )
            ''')

            print(f"Table {TableName.MOVEMENT.value} successfully created!")
        case TableName.DEBT_CRED:
            # Table debts creds
            debt_cred_columns = ", ".join([f"{key} {value}" for key, value in manager.get_debt_cred_tags().items()])
            cursor.execute(f'''
                create TABLE IF NOT EXISTS {TableName.DEBT_CRED.value}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {debt_cred_columns}
                    )
            ''')

            print(f"Table {TableName.DEBT_CRED.value} successfully created!")
        case TableName.EXPENSES_RECAP:
            # Table recap of expenses
            expenses_recap_columns = "Method_of_payment TEXT, " + ", ".join([f"{cat} REAL" for cat in manager.get_categories()])
            cursor.execute(f'''
                create TABLE IF NOT EXISTS {TableName.EXPENSES_RECAP.value}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {expenses_recap_columns}
                )
            ''')

            print(f"Table {TableName.EXPENSES_RECAP.value} successfully created!")
        case TableName.EXPENSES_MONTH_RECAP:
            # Table monthly recap of expenses
            month_name = datetime(2020, int(index), 1).strftime('%B').lower() + "_recap"

            expenses_recap_columns = "Method_of_payment TEXT, " + ", ".join([f"{cat} REAL" for cat in manager.get_categories()])
            cursor.execute(f'''
                create TABLE IF NOT EXISTS {month_name}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {expenses_recap_columns}
                )
            ''')

            print(f'Table {month_name} successfully created!')
            return month_name
        case TableName.DEBT_CRED_RECAP:
            # Table debts and creds recap
            debt_cred_recap_columns = ", ".join([f"{key} {value}" for key, value in manager.get_debt_cred_recap_tags().items()])
            cursor.execute(f'''
                create TABLE IF NOT EXISTS {TableName.DEBT_CRED_RECAP.value}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {debt_cred_recap_columns}
                )
            ''')

            print(f"Table {TableName.DEBT_CRED_RECAP.value} successfully created!")

    return ''

#   --- --- --- --- --- --- --- --- 

def add_movement(
    manager: DatabaseManager,
    cursor: sqlite3.Cursor,
    date : str,
    category,
    description : str,
    method,
    amount : float,
    movement : MovementTypes) -> None:
    """This function inserts new rows to the table movements.
    It requires the values associated with the query."""
    
    q = ", ".join(manager.get_movement_tags())
    v = ", ".join("?" for _ in manager.get_movement_tags())
    query = f"INSERT INTO {TableName.MOVEMENT.value} ({q}) VALUES ({v})"
    values = (date, category, description, method, amount, movement.value)
    cursor.execute(query, values)

    print("Dati inseriti con successo!")

#   --- --- --- --- --- --- --- --- 

def add_debt_cred(
    manager: DatabaseManager,
    cursor: sqlite3.Cursor,
    date : str,
    category,
    description : str,
    subject : str,
    amount : float,
    paid : float,
    movement: MovementTypes) -> None:
    """This function inserts new rows to the table debt_cred."""
    
    q = ", ".join(manager.get_debt_cred_tags())
    v = ", ".join("?" for _ in manager.get_debt_cred_tags())
    query = f"INSERT INTO {TableName.DEBT_CRED.value} ({q}) VALUES ({v})"
    due = amount - paid
    values = (date, category, description, subject, amount, paid, due, movement.value)
    cursor.execute(query, values)

    print("Dati inseriti con successo!")

#   --- --- --- --- --- --- --- --- 

def modify_delete_row(cursor: sqlite3.Cursor, operation : Operations, table : TableName, row_id : int, tag = '', value = 0) -> None:
    """This function modifies or deletes the row's values from table movement and debt_cred.
    It requires the operation's type, the table's name, the tag, and the row's id."""

    if operation == Operations.MODIFY:
        cursor.execute(f"UPDATE {table.value} SET {tag} = {value} WHERE id = {row_id}")
        
        if table == TableName.DEBT_CRED and (tag == 'amount' or tag == 'paid'): #TODO cambiare amount 4 paid 5 due 6
            cursor.execute(f"SELECT * FROM {table.value} WHERE id = {row_id}")
            (id_row, date, category, description, subject, amount, paid, due, movement) = cursor.fetchone()
            due =  amount - paid
            cursor.execute(f"UPDATE {table.value} SET {'due'} = {due} WHERE id = {row_id}")

    if operation == Operations.DELETE:
        cursor.execute(f"DELETE FROM {table.value} WHERE id = {row_id}")

#   --- --- --- --- --- --- --- ---

def read_table(cursor: sqlite3.Cursor, table : TableName) -> None:
    """
    This function prints the input table.
    The input tables can be: movement, debt_cred, expenses_recap, 'Month_name'_recap, or month_recap.
    In the last case the function prints all the 'Month_name'_recap tables.
    """

    if table == TableName.EXPENSES_MONTH_RECAP:
        for i in range(1, 13):
            month_name = datetime(2020, int(i), 1).strftime('%B').lower() + "_recap"
            cursor.execute(f"SELECT * FROM {month_name}")
            rows = cursor.fetchall()
            print(f"Table {month_name}")

            for row in rows:
                print(row)

    else:
        cursor.execute(f"SELECT * FROM {table.value}")
        rows = cursor.fetchall()
        print(f"Table {table.value}")
        
        for row in rows:
            print(row)

#   --- --- --- --- --- --- --- --- 

def expenses_recap(manager: DatabaseManager, cursor: sqlite3.Cursor, month = 0) -> None:
    """
    This function fills the table recap based on the table movement
    The month can be set to 'month_recap': in this case it fills all the recap tables filtered by the month.
    The month can be set equal to a specific month (es: filter = 1 -> January): in this case it fills the chosen monthly recap tables.
    """

    cursor.execute(f"SELECT * FROM {TableName.MOVEMENT.value}")
    rows = cursor.fetchall()

    recap_amount = [[[
                0 for _ in manager.get_categories()
            ] for _ in manager.get_methods_of_payment()
        ] for _ in range(12)
    ]
    
    q = "Method_of_payment, " + ", ".join(manager.get_categories())
    v = "?, " + ", ".join("?" for _ in manager.get_categories())

    for row in rows:
        id_mov, date, category, description, method, amount, movement = row

        id_met = manager.get_methods_of_payment().index(method)
        id_cat =  manager.get_categories().index(category)

        # Changing the amount's sign if it's an exit
        if movement == MovementTypes.EXIT:
            amount = - amount

        # Saving the amounts in an array for the table expenses_recap
        if month:
            # If filter month_recap is applied, then we use all the necessary matrices for the recap
            id_mon = datetime.strptime(date, '%Y-%m-%d').month
            recap_amount[id_mon-1][id_met][id_cat] += amount
            
        else:
            # If no filter is applied, then we use only the first matrices
            recap_amount[0][id_met][id_cat] += amount

    if not month:
        create_table(manager, cursor, TableName.EXPENSES_RECAP)

        for i in range(len(manager.get_methods_of_payment())):
            query = f"INSERT INTO {TableName.EXPENSES_RECAP.value} ({q}) VALUES ({v})"
            values = manager.get_methods_of_payment()[i], *recap_amount[0][i][:]

            cursor.execute(query, values)

    
    if month == TableName.EXPENSES_MONTH_RECAP:
        table = []

        for k in range(1, 13):
            table.insert(k-1, create_table(manager, cursor, TableName.EXPENSES_MONTH_RECAP, k))
            cursor.execute(f"DELETE FROM {table[k-1]}")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table[k-1]}'")

            for i in range(len(manager.get_methods_of_payment())):
                query = f"INSERT INTO {table[k-1]} ({q}) VALUES ({v})"
                values = manager.get_methods_of_payment()[i], *recap_amount[k-1][i][:]

                cursor.execute(query, values)

    if month != 0 and month != TableName.EXPENSES_MONTH_RECAP:
        table = create_table(manager, cursor, TableName.EXPENSES_MONTH_RECAP, month)
        cursor.execute(f"DELETE FROM {table}")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")

        for i in range(len(manager.get_methods_of_payment())):
                query = f"INSERT INTO {table} ({q}) VALUES ({v})"
                values = manager.get_methods_of_payment()[i], *recap_amount[month - 1][i][:]

                cursor.execute(query, values)

#   --- --- --- --- --- --- --- --- 

def debt_cred_recap(manager: DatabaseManager, cursor: sqlite3.Cursor) -> None:
    """
    This function creates the table debt_carted_recap.
    Table 1st column: Subject name.
    Table 2nd column: Status.
    Table 3rd column: Amount.
    """

    subject_names = []
    recap_amount = []
    q = ", ".join(manager.get_debt_cred_recap_tags())
    v = ", ".join("?" for _ in manager.get_debt_cred_recap_tags())

    create_table(manager, cursor, TableName.DEBT_CRED_RECAP)

    cursor.execute(f"SELECT * FROM {TableName.DEBT_CRED.value}")
    rows = cursor.fetchall()

    for row in rows:
        id_dc, date, category, description, subject, amount, paid, due, movement = row

        if movement == MovementTypes.DEBT:
            due = - due

        if subject not in subject_names:
            subject_names.append(subject)
            recap_amount.append(0)
                
        recap_amount[subject_names.index(subject)] += due

    for subject in subject_names:
        amount = recap_amount[subject_names.index(subject)]

        if amount < 0:
            prompt = 'sono in debito di:'
        elif amount == 0:
            prompt = 'sono in pari'
        else:
            prompt = 'sono in credito di:'

        query = f"INSERT INTO {TableName.DEBT_CRED_RECAP.value} ({q}) VALUES ({v})"
        values = subject, prompt, amount

        cursor.execute(query, values)