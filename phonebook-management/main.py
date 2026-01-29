import database
import gui

def main():
    database.init_db()   
    gui.run_app()        

if __name__ == "__main__":
    main()
