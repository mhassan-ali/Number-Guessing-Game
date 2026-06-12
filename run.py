import sys
from gui import NumberGuessingApp

def main():
    try:
        app = NumberGuessingApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
