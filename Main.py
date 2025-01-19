from SystemManagement.Library import Library
from SystemManagement.ManageCSV import ManageCSV
from SystemManagement.InitFiles import InitFiles

def init_files():
    InitFiles.init_books_csv()
    InitFiles.ensure_required_columns()
    InitFiles.initialize_waiting_list()
    InitFiles.initialize_csv_files()
    InitFiles.sort_books()
    InitFiles.init_users_csv()


if __name__ == "__main__":
    library = Library.get_instance()
    init_files()

