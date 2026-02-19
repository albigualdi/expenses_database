from enum import Enum
from datetime import datetime
from typing import Annotated

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
    def __init__(self, METHODS_OF_PAYMENT, CATEGORIES):
        '''This function initializes the database.'''

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
        
        self.METHODS_OF_PAYMENT = METHODS_OF_PAYMENT
        self.CATEGORIES = CATEGORIES

    # --- Accessor Methods ---

    def getMovementTags(self) -> dict:
        return self.MOVEMENT_TAGS
    
    def getDebtCredTags(self) -> dict:
        return self.DEBT_CRED_TAGS
    
    def getDebtCredRecapTags(self) -> dict: 
        return self.DEBT_CRED_RECAP_TAGS
    
    def getMethodsOfPayment(self) -> list:
        return self.METHODS_OF_PAYMENT
    
    def getCategories(self) -> list: 
        return self.CATEGORIES



# --- Principal -----------------------------------------------------------

def createTable(manager, cursor, table : TableName, index = 1) -> str:
    '''This function initialize the database. It creates all the needed tables.'''

    # match table:
        # 'movement':
            # ;
        # 'dept_cred':
            # ;

    # Table movements
    if table == TableName.MOVEMENT.value:
        movement_columns = ", ".join([f"{key} {value}" for key, value in manager.getMovementTags().items()])
        cursor.execute(f'''
            create TABLE IF NOT EXISTS {TableName.MOVEMENT.value}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {movement_columns}
            )
        ''')
        
        print(f"Table {TableName.MOVEMENT.value} successfully created!")

    # Table debts creds
    if table == TableName.DEBT_CRED.value:
        debt_cred_columns = ", ".join([f"{key} {value}" for key, value in manager.getDebtCredTags().items()])
        cursor.execute(f'''
            create TABLE IF NOT EXISTS {TableName.DEBT_CRED.value}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {debt_cred_columns}
                )
        ''')

        print(f"Table {TableName.DEBT_CRED.value} successfully created!")
    
    # Table recap of expenses
    if table == TableName.EXPENSES_RECAP.value:
        expenses_recap_columns = "Method_of_payment TEXT, " + ", ".join([f"{cat} REAL" for cat in manager.getCategories()])
        cursor.execute(f'''
            create TABLE IF NOT EXISTS {TableName.EXPENSES_RECAP.value}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {expenses_recap_columns}
            )
        ''')

        print(f"Table {TableName.EXPENSES_RECAP.value} successfully created!")

    # Table monthly recap of expenses
    if table == TableName.EXPENSES_MONTH_RECAP.value:
        month_name = datetime(2020, int(index), 1).strftime('%B').lower() + "_recap"

        expenses_recap_columns = "Method_of_payment TEXT, " + ", ".join([f"{cat} REAL" for cat in manager.getCategories()])
        cursor.execute(f'''
            create TABLE IF NOT EXISTS {month_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {expenses_recap_columns}
            )
        ''')

        print(f'Table {month_name} successfully created!')

        return month_name
    
    # Table debts and creds recap
    if table == TableName.DEBT_CRED_RECAP.value:
        debt_cred_recap_columns = ", ".join([f"{key} {value}" for key, value in manager.getDebtCredRecapTags().items()])
        cursor.execute(f'''
            create TABLE IF NOT EXISTS {TableName.DEBT_CRED_RECAP.value}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {debt_cred_recap_columns}
            )
        ''')

        print(f"Table {TableName.DEBT_CRED_RECAP.value} successfully created!")

#   --- --- --- --- --- --- --- --- 

def createTable(cursor, table : TableName):
    '''This function deletes the table set as input.'''

    cursor.execute(f"DROP TABLE IF EXISTS {table}")
    print(f'Table {table} successfully deleted!')

#   --- --- --- --- --- --- --- --- 

def addMovement(
    manager,
    cursor,
    date : str,
    category : DatabaseManager,
    description : str,
    method : DatabaseManager,
    amount : float,
    type : MovementTypes):
    '''This function inserts new rows to the table movements.
    It requires the values associated to the query.'''
    
    q = ", ".join(manager.getMovementTags())
    v = ", ".join("?" for _ in manager.getMovementTags())
    query = f"INSERT INTO {TableName.MOVEMENT.value} ({q}) VALUES ({v})"
    values = (date, category, description, method, amount, type)
    cursor.execute(query, values)

    print("Dati inseriti con successo!")

#   --- --- --- --- --- --- --- --- 

def addDebtCred(
    manager,
    cursor,
    date : str,
    category : DatabaseManager,
    description : str,
    subject : str,
    amount : float,
    paid : float,
    type: MovementTypes):
    '''This function inserts new rows to the table debt_cred.'''
    
    q = ", ".join(manager.getDebtCredTags())
    v = ", ".join("?" for _ in manager.getDebtCredTags())
    query = f"INSERT INTO {TableName.DEBT_CRED.value} ({q}) VALUES ({v})"
    due = amount - paid
    values = (date, category, description, subject, amount, paid, due, type)
    cursor.execute(query, values)

    print("Dati inseriti con successo!")

#   --- --- --- --- --- --- --- --- 

def modifyDeleteRow(cursor, operation : Operations, table : TableName, row_id : int, tag = '', value = 0):
    '''This function modifies or deletes the row's values from table movement and debt_cred.
    It requires the operation's type, the table's name, the tag and the row's id.'''

    if operation == Operations.MODIFY.value:
        cursor.execute(f"UPDATE {table} SET {tag} = {value} WHERE id = {row_id}")
        
        if table == TableName.DEBT_CRED.value and (tag == 'amount' or tag == 'paid'): #TODO cambiare amount 4 paid 5 due 6 
            cursor.execute(f"SELECT * FROM {table} WHERE id = {row_id}")
            (id_row, date, category, description, subject, amount, paid, due, type) = cursor.fetchone()
            due =  amount - paid
            cursor.execute(f"UPDATE {table} SET {'due'} = {due} WHERE id = {row_id}")

    if operation == Operations.DELETE.value:
        cursor.execute(f"DELETE FROM {table} WHERE id = {row_id}")

#   --- --- --- --- --- --- --- ---

def readTable(cursor, table : TableName):
    '''This function prints the input table.
    The input tables can be: movement, debt_cred, expenses_recap, 'Month_name'_recap, or month_recap.
    In the last case the function prints all the 'Month_name'_recap tables.'''

    if table == TableName.EXPENSES_MONTH_RECAP.value:
        for i in range(1, 13):
            month_name = datetime(2020, int(i), 1).strftime('%B').lower() + "_recap"
            cursor.execute(f"SELECT * FROM {month_name}")
            rows = cursor.fetchall()
            print(f"Table {month_name}")

            for row in rows:
                print(row)

    else:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        print(f"Table {table}")
        
        for row in rows:
            print(row)

#   --- --- --- --- --- --- --- --- 

def expensesRecap(manager, cursor, filter = 0):
    '''This function fills the table recap based on the tables movement
    The filter can be set to 'month_recap': in this case it fills all the recap tables filtered by month.
    The filter can be set equal to a specific month (es: filter = 1 -> January): in this case it fills the chosen monhtly recap tables.'''

    cursor.execute(f"SELECT * FROM {TableName.MOVEMENT.value}")
    rows = cursor.fetchall()

    recap_amount = [[[
                0 for _ in manager.getCategories()
            ] for _ in manager.getMethodsOfPayment()
        ] for _ in range(12)
    ]
    
    q = "Method_of_payment, " + ", ".join(manager.getCategories())
    v = "?, " + ", ".join("?" for _ in manager.getCategories())

    for row in rows:
        id_mov, date, category, description, method, amount, type = row

        id_met = manager.getMethodsOfPayment().index(method)
        id_cat =  manager.getCategories().index(category)

        # Changing the amount's sign if it's an exit
        if type == MovementTypes.EXIT.value:
            amount = - amount

        # Saving the amounts in an array for the table expenses_recap
        if filter:
            id_mon = datetime.strptime(date, '%Y-%m-%d').month      # If filter month_recap is applied then we use all the needed matrices for the recap
            recap_amount[id_mon-1][id_met][id_cat] += amount
            
        else:                                                       # If no filter is applied then we use only the first matrices    
            recap_amount[0][id_met][id_cat] += amount

    if not filter:
        createTable(cursor, TableName.EXPENSES_RECAP.value)
        createTable(manager, cursor, TableName.EXPENSES_RECAP.value)

        for i in range(len(manager.getMethodsOfPayment())):
            query = f"INSERT INTO {TableName.EXPENSES_RECAP.value} ({q}) VALUES ({v})"
            values = manager.getMethodsOfPayment()[i], *recap_amount[0][i][:]

            cursor.execute(query, values)

    
    if filter == TableName.EXPENSES_MONTH_RECAP.value:
        table = []

        for k in range(1, 13):
            table.insert(k-1, createTable(manager, cursor, TableName.EXPENSES_MONTH_RECAP.value, k))
            cursor.execute(f"DELETE FROM {table[k-1]}")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table[k-1]}'")

            for i in range(len(manager.getMethodsOfPayment())):
                query = f"INSERT INTO {table[k-1]} ({q}) VALUES ({v})"
                values = manager.getMethodsOfPayment()[i], *recap_amount[k-1][i][:]

                cursor.execute(query, values)

    if filter != 0 and filter != TableName.EXPENSES_MONTH_RECAP.value:
        table = createTable(manager, cursor, TableName.EXPENSES_MONTH_RECAP.value, filter)
        cursor.execute(f"DELETE FROM {table}")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")

        for i in range(len(manager.getMethodsOfPayment())):
                query = f"INSERT INTO {table} ({q}) VALUES ({v})"
                values = manager.getMethodsOfPayment()[i], *recap_amount[filter-1][i][:]

                cursor.execute(query, values)

#   --- --- --- --- --- --- --- --- 

def debtCredRecap(manager, cursor):
    '''This function creates the table debt_crted_recap.
    Table 1st column: Subject name.
    Table 2nd column: Status.
    Table 3rd column: Amount.'''

    subject_names = []
    recap_amount = []
    q = ", ".join(manager.getDebtCredRecapTags())
    v = ", ".join("?" for _ in manager.getDebtCredRecapTags())
    print()
    createTable(cursor, TableName.DEBT_CRED_RECAP.value)
    createTable(manager, cursor, TableName.DEBT_CRED_RECAP.value)

    cursor.execute(f"SELECT * FROM {TableName.DEBT_CRED.value}")
    rows = cursor.fetchall()

    for row in rows:
        id_dc, date, category, description, subject, amount, paid, due, type = row

        if type == MovementTypes.DEBT.value:
            due = - due

        if subject not in subject_names:
            subject_names.append(subject)
            recap_amount.append(0)
                
        recap_amount[subject_names.index(subject)] += due

    for subject in subject_names:
        amount = recap_amount[subject_names.index(subject)]
        if amount < 0:
            prompt = 'sono in debito di:'

        if amount == 0:
            prompt = 'sono in pari'

        if amount > 0:
            prompt = 'sono in credito di:'

        query = f"INSERT INTO {TableName.DEBT_CRED_RECAP.value} ({q}) VALUES ({v})"
        values = subject, prompt, amount

        cursor.execute(query, values)