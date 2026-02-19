from pathlib import Path

class DatabaseConfig:
    HOME = Path.home()
    default_dir = 'Documenti'
    default_name = 'untitled'

    @classmethod
    def set_defaults(cls, folder: str = None, name: str = None):
        """Method to update the default values"""
        if folder:
            cls.default_dir = folder
        if name:
            cls.default_name = name


def save_database(folder_name : str = None, base_name : str = None) -> str:
    '''saveDatabase creates the directory (if doesn't exist)
    and returns a unique file path to avoid overwriting'''

    folder = folder_name or DatabaseConfig.default_dir
    name = base_name or DatabaseConfig.default_name

    target_dir = Path.joinpath(DatabaseConfig.HOME, folder)
    target_dir.mkdir(parents=True, exist_ok=True)


    clean_name = Path(name).stem
    file_path = Path.joinpath(target_dir, f"{clean_name}.db")

    counter = 1
    while file_path.exists():
        file_path = Path.joinpath(target_dir, f"{clean_name}_{counter}.db")
        counter += 1

    return file_path

# --- Per vedere come funziona ---
# print(save_database())
# DatabaseConfig.set_defaults(folder='Progetti/Database', name='backup_globale')
# print(save_database())