import sqlite3
import database_saver
import expenses_functions
from expenses_functions import DatabaseManager, TableName, MovementTypes, Operations

# --- Initialization of the program's constants ---

# Set the Database name and path
DATABASE = database_saver.save_database('', 'spese.db')


# This list may be modified
METHODS_OF_PAYMENT = [
    'Contanti',
    'Bonifico',
    'Bancomat',
    'Mastercard 5650',
    'Mastercard 6613',
    'PayPal'
]

# This list may be modified
CATEGORIES = [
    'Cibo',
    'Svago',
    'Spesa',
    'Vestiti',
    'Informatica',
    'Farmacia',
    'Ferramenta',
    'Regali',
    'Viaggi',
    'Trasporti',
    'Generico'
]

# Initialize the class DatabaseManager that collects the constants of the program
manager = DatabaseManager(METHODS_OF_PAYMENT, CATEGORIES)

# Create or open the database
connection = sqlite3.connect(DATABASE)
# Set the cursor to navigate the database
cursor: sqlite3.Cursor = connection.cursor()

#--------------------------------------------------------------------------------------------

# --- Create tables ---
# expenses_functions.create_table(manager, cursor, TableName.MOVEMENT)
# expenses_functions.create_table(manager, cursor, TableName.DEBT_CRED)

# expenses_functions.expenses_recap(manager, cursor)
# expenses_functions.expenses_recap(manager, cursor, TableName.EXPENSES_MONTH_RECAP)
# expenses_functions.expenses_recap(manager, cursor, 1)
# expenses_functions.debt_cred_recap(manager, cursor)

# -- Add row ---
# expenses_functions.add_movement(manager, cursor, '2026-01-01', 'Cibo', 'Cena', 'Contanti', 10, MovementTypes.EXIT)
# expenses_functions.add_movement(manager, cursor, '2026-01-01', 'Svago', 'Cinema', 'Contanti', 10, MovementTypes.EXIT)
# expenses_functions.add_movement(manager, cursor, '2026-02-01', 'Vestiti', 'Maglia', 'Contanti', 10, MovementTypes.EXIT)
# expenses_functions.add_movement(manager, cursor, '2026-03-01', 'Cibo', 'Anniversario', 'Contanti', 10, MovementTypes.EXIT)
# expenses_functions.add_debt_cred(manager, cursor, '2026-01-01', 'Regali', 'Pensieri', 'Mamma', 10, 0, MovementTypes.DEBT)
# expenses_functions.add_debt_cred(manager, cursor, '2026-02-01', 'Regali', 'Pensieri', 'Lori', 10, 5, MovementTypes.CRED)
# expenses_functions.add_debt_cred(manager, cursor, '2026-03-01', 'Regali', 'Pensieri', 'Lori', 10, 0, MovementTypes.DEBT)
# expenses_functions.add_debt_cred(manager, cursor, '2026-03-01', 'Regali', 'Pensieri', 'Brigg', 10, 0, MovementTypes.CRED)

# --- Modify tables ---
# expenses_functions.modify_delete_row(cursor, Operations.MODIFY, TableName.DEBT_CRED, 1, 'amount', 100)
# expenses_functions.modify_delete_row(cursor, Operations.MODIFY, TableName.DEBT_CRED, 1, 'paid', 30)
# expenses_functions.modify_delete_row(cursor, Operations.DELETE, TableName.DEBT_CRED, 9)

# --- Read Tables ---
# expenses_functions.read_table(cursor, TableName.MOVEMENT)
# expenses_functions.read_table(cursor, TableName.DEBT_CRED)
# expenses_functions.read_table(cursor, TableName.EXPENSES_RECAP)
# expenses_functions.read_table(cursor, TableName.EXPENSES_MONTH_RECAP)
# expenses_functions.read_table(cursor, TableName.EXPENSES_MONTH_RECAP, month_ind = 1)
# expenses_functions.read_table(cursor, TableName.DEBT_CRED_RECAP)

# --- Delete Tables ---
# expenses_functions.delete_table(cursor, TableName.MOVEMENT)
# expenses_functions.delete_table(cursor, TableName.DEBT_CRED)
# expenses_functions.delete_table(cursor, TableName.EXPENSES_RECAP)
# expenses_functions.delete_table(cursor, TableName.DEBT_CRED_RECAP)
# expenses_functions.delete_table(cursor, 'january_recap')
# expenses_functions.delete_table(cursor, 'february_recap')
# expenses_functions.delete_table(cursor, 'march_recap')
# expenses_functions.delete_table(cursor, 'april_recap')
# expenses_functions.delete_table(cursor, 'may_recap')
# expenses_functions.delete_table(cursor, 'june_recap')
# expenses_functions.delete_table(cursor, 'july_recap')
# expenses_functions.delete_table(cursor, 'august_recap')
# expenses_functions.delete_table(cursor, 'september_recap')
# expenses_functions.delete_table(cursor, 'october_recap')
# expenses_functions.delete_table(cursor, 'november_recap')
# expenses_functions.delete_table(cursor, 'december_recap')

#--------------------------------------------------------------------------------------------

connection.commit()
connection.close()