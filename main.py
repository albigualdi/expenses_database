import sqlite3
import database_saver
import expenses_functions
from expenses_functions import DatabaseManager

# --- Initialization of the constants of the program ---

DATABASE = database_saver.save_database()   # Set the Database name and path
# DATABASE = 'spese_2026.db'


METHODS_OF_PAYMENT = [          # This list may be modified
    'Contanti',
    'Bonifico',
    'Bancomat',
    'Mastercard 5650',
    'Mastercard 6613',
    'PayPal'
]

CATEGORIES = [                  # This list may be modified
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

manager = DatabaseManager(METHODS_OF_PAYMENT, CATEGORIES) # Initialize the class DatabaseManager that collects the costants of the program

connection = sqlite3.connect(DATABASE)  # Create or open the database
cursor = connection.cursor()            # Set the cursor to navigate the database

#--------------------------------------------------------------------------------------------

# --- Create tables ---
# expenses_functions.create_table(manager, cursor, 'movement')
# expenses_functions.create_table(manager, cursor, 'debt_cred')
# expenses_functions.expenses_recap(manager, cursor, 'month_recap')
# expenses_functions.debt_cred_recap(manager, cursor)

# -- Add row ---
# expenses_functions.add_movement(manager, cursor, '2026-07-15', 'Cena', 'San Valentino', 'Contanti', 10, 'uscita')
# expenses_functions.add_debt_cred(manager, cursor, '2026-01-01', 'Regali', 'Pranzo', 'Mamma', 10, 0, 'debito')
# expenses_functions.add_debt_cred(manager, cursor, '2026-02-01', 'Regali', 'Pranzo', 'Lori', 10, 5, 'credito')
# expenses_functions.add_debt_cred(manager, cursor, '2026-03-01', 'Regali', 'Pranzo', 'Lori', 10, 0, 'debito')
# expenses_functions.add_debt_cred(manager, cursor, '2026-03-01', 'Regali', 'Pranzo', 'Brigg', 10, 0, 'credito')

# --- Modify tables ---
# expenses_functions.modify_delete_row(cursor, 'modify', 'debt_cred', 1, 'amount', 100)
# expenses_functions.modify_delete_row(cursor, 'modify', 'debt_cred', 1, tag='paid', value=30)
# expenses_functions.modify_delete_row(cursor, 'delete', 'debt_cred', 9)

# --- Read Tables ---
# expenses_functions.read_table(cursor, 'debt_cred')
# expenses_functions.read_table(cursor, 'movement')
# expenses_functions.read_table(cursor, 'month_recap')
# expenses_functions.read_table(cursor, 'debt_cred_recap')

# --- Delete Tables ---
# expenses_functions.delete_table(cursor, 'movement')
# expenses_functions.delete_table(cursor, 'debt_cred')
# expenses_functions.delete_table(cursor, 'expenses_recap')
# expenses_functions.delete_table(cursor, 'debt_cred_recap')
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
