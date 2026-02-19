import sqlite3
import database_saver
import expenses_functions
from expenses_functions import DatabaseManager

# --- Initialization of the program's constants ---

# Set the Database name and path
DATABASE = database_saver.save_database()
# DATABASE = 'spese_2026.db'


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
# expenses_functions.createTable(manager, cursor, 'movement')
# expenses_functions.createTable(manager, cursor, 'debt_cred')
# expenses_functions.expensesRecap(manager, cursor, 'month_recap')
# expenses_functions.debtCredRecap(manager, cursor)

# -- Add row ---
# expenses_functions.addMovement(manager, cursor, '2026-07-15', 'Cena', 'San Valentino', 'Contanti', 10, 'uscita')
# expenses_functions.addDebtCred(manager, cursor, '2026-01-01', 'Regali', 'Pranzo', 'Mamma', 10, 0, 'debito')
# expenses_functions.addDebtCred(manager, cursor, '2026-02-01', 'Regali', 'Pranzo', 'Lori', 10, 5, 'credito')
# expenses_functions.addDebtCred(manager, cursor, '2026-03-01', 'Regali', 'Pranzo', 'Lori', 10, 0, 'debito')
# expenses_functions.addDebtCred(manager, cursor, '2026-03-01', 'Regali', 'Pranzo', 'Brigg', 10, 0, 'credito')

# --- Modify tables ---
# expenses_functions.modifyDeleteRow(cursor, 'modify', 'debt_cred', 1, 'amount', 100)
# expenses_functions.modifyDeleteRow(cursor, 'modify', 'debt_cred', 1, tag='paid', value=30)
# expenses_functions.modifyDeleteRow(cursor, 'delete', 'debt_cred', 9)

# --- Read Tables ---
# expenses_functions.readTable(cursor, 'debt_cred')
# expenses_functions.readTable(cursor, 'movement')
# expenses_functions.readTable(cursor, 'month_recap')
# expenses_functions.readTable(cursor, 'debt_cred_recap')

# --- Delete Tables ---
# expenses_functions.deleteTable(cursor, 'movement')
# expenses_functions.deleteTable(cursor, 'debt_cred')
# expenses_functions.deleteTable(cursor, 'expenses_recap')
# expenses_functions.deleteTable(cursor, 'debt_cred_recap')
# expenses_functions.deleteTable(cursor, 'january_recap')
# expenses_functions.deleteTable(cursor, 'february_recap')
# expenses_functions.deleteTable(cursor, 'march_recap')
# expenses_functions.deleteTable(cursor, 'april_recap')
# expenses_functions.deleteTable(cursor, 'may_recap')
# expenses_functions.deleteTable(cursor, 'june_recap')
# expenses_functions.deleteTable(cursor, 'july_recap')
# expenses_functions.deleteTable(cursor, 'august_recap')
# expenses_functions.deleteTable(cursor, 'september_recap')
# expenses_functions.deleteTable(cursor, 'october_recap')
# expenses_functions.deleteTable(cursor, 'november_recap')
# expenses_functions.deleteTable(cursor, 'december_recap')

#--------------------------------------------------------------------------------------------

connection.commit()
connection.close()
