from database.create_tables import create_tables

def main():

    print("Iniciando sistema...")

    create_tables()

    print("Banco de dados pronto!")

if __name__ == "__main__":
    main()