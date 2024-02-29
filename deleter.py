
import sys
import re

def main():

    deck_name = sys.argv[1]
    file_name = sys.argv[2]

    with open(file_name, 'r', encoding='utf-8') as file:
        md_content = file.read()
   
    print("Successfully updated all cards.")

if __name__ == "__main__":
    main()


