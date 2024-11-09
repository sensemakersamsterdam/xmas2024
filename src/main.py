from time import sleep
from app import startup, effect_loop, full_help

def main():
    """Main function to run the device."""
    startup()
    print()
    print(full_help())

    while True:
        effect_loop()


if __name__ == "__main__":
    try:
        print("You have 5 seconds to press Ctrl+C to stop the program...")
        sleep(5)
    except KeyboardInterrupt:
        print("Program stopped by user.")
        exit(0)
        
    main()


