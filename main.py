"""
The start
"""

import sys
import requests
from bs4 import BeautifulSoup
import wbr.main
import wbr.main2


def one():
    a = sys.platform

    if a in ['win32', 'cygwin']:
        wbr.main.main()
    else:
        wbr.main2.main()

def two():

    print("Retrieving data....")
    url = "https://nglam.dev/resources/wbr/"
    try:
        response = requests.get(url)
    except:
        # no internet
        print("An error occured while retrieving data, please try again later.")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    code_block = soup.find("pre").find("code")

    if code_block:
        text = code_block.get_text().strip()
        with open('wbr/data.txt', 'w') as f:
            f.write(text)
        print("Updated word list successfully.")
        inp()
    else:
        print("An error occured while retrieving data, please try again later.")
        sys.exit(1)

def inp():
    print("-"*30)
    print()
    print("""WBR-auto v1.1: automatically plays What Beats Rock for you.
--Made by Fluentix (https://fluentix.dev)--

Get involved: https://contribute.fluentix.dev
Contribute to this project here: https://wbr.fluentix.dev/contribute
""")
    print("""
Options:
[1] : Start WBR-auto
[2] : Update word list (recommended)""")
    option = int(input("Enter a valid option: "))

    if option == 1:
        one()
    elif option == 2:
        two()
    else:
        print("Not a valid option, try again")
        inp()

if __name__ == '__main__':
    inp()
