from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from typing import List
from colorama import Fore, Back, Style
import time
import requests
import os
import webbrowser


# CONSTANTS --- TOGGLE IF NEEDED

TIMEOUT_SECONDS = 5000
DELAY_PER_ACTION = 0.1
DELAY_PER_WORD = 0.1

ADBLOCK_EXTENSION_PATH = os.path.join(os.getcwd(), 'extensions', 'adblocker')

class WBR_Console:
    @staticmethod
    def PrintError(msg: str):
        print(Fore.RED + Style.BRIGHT + "[ERROR] " +
            Style.RESET_ALL + Fore.YELLOW + msg + Style.RESET_ALL)
    
    @staticmethod
    def PrintInfo(msg: str):
        print(Fore.WHITE + Style.BRIGHT + "[INFO] " +
            Style.RESET_ALL + Fore.WHITE + msg + Style.RESET_ALL)
    
    @staticmethod
    def PrintSuccess(msg: str):
        print(Fore.GREEN + Style.BRIGHT + "[SUCCESS] " +
            Style.RESET_ALL + Fore.WHITE + msg + Style.RESET_ALL)
        
    @staticmethod
    def Clear():
        print("\n" * 100)

class WBR_Browser:
    def __init__(self, setupBrowser : bool = True, setupAdBlocker : bool = True):
        if setupBrowser:
            self.SetupBrowser(True)
            
        if setupAdBlocker:
            self.SetupAdBlocker()

    def SetupBrowser(self, setupWBR : bool = False):
        """
        Sets up the browser so this class will work correctly.
        """
        chrome_options = Options()

        WBR_Console.PrintInfo("Setting up chrome service...")
        
        self.Driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        WBR_Console.PrintSuccess("Chrome service setted up!")

        if setupWBR:
            self.SetupWBR()

    def SetupWBR(self):

        self.Driver.get("https://whatbeatsrock.com")
        WBR_Console.PrintSuccess("Opened what beats rock website.")
    
    def SetupAdBlocker(self):
        """
        Sets up the ad blocker
        """

        WBR_Console.PrintInfo("Setting up adblocker...")
        self.Driver.switch_to.new_window("window")
        self.Driver.get("chrome://extensions")

        script = """
        return document.querySelector('extensions-manager')
            .shadowRoot.querySelector('extensions-toolbar')
            .shadowRoot.querySelector('#devMode');
        """

        toggle = self.Driver.execute_script(script)
        toggle.click()

        WBR_Console.PrintSuccess("Enabled developer mode")
        time.sleep(1)

        load_unpacked_script = """
        return document.querySelector('extensions-manager')
            .shadowRoot.querySelector('extensions-toolbar')
            .shadowRoot.querySelector('#loadUnpacked');
        """

        load_button = self.Driver.execute_script(load_unpacked_script)
        load_button.click()

        WBR_Console.PrintSuccess("Pressed button to show extension folder.")

        print("-"*15)
        input(f"[SELECTION] Select folder in path '{ADBLOCK_EXTENSION_PATH}' for file upload prompt and once done press 'ENTER' if extension is loaded: ")
        print("-"*15)

        WBR_Console.PrintSuccess("Adblock setted up!")

        self.Driver.close()
        self.Driver.switch_to.window(self.Driver.window_handles[0])
        self.Driver.refresh()


    def PressGo(self) -> None:
        """
        Presses the 'GO' button
        """
        
        WebDriverWait(self.Driver, TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form button"))
        )
        Element_GoButton = self.Driver.find_element(By.CSS_SELECTOR, "form button")
        self.Driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Element_GoButton)
        Element_GoButton.click()
        

    def TypeWord(self, word: str) -> None:
        """
        Types a word and then press the 'GO' button
        """
        
        WebDriverWait(self.Driver, TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form input"))
        )

        Element_InputField = self.Driver.find_element(By.CSS_SELECTOR, "form input")
        self.Driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Element_InputField)
        Element_InputField.clear()
        Element_InputField.send_keys(word)

        self.PressGo()
    
    def ClickNextButton(self):
        WebDriverWait(self.Driver, TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'next')]"))
        )

        Element_GoButton = self.Driver.find_element(By.XPATH, "//button[contains(text(), 'next')]")
        self.Driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Element_GoButton)
        Element_GoButton.click()


class WBR_WordBank:
    def __init__(self):
        self.wordBank = []
    
    def GetWordBank(self) -> List[str]:
        """
        Returns the pointer to word bank list.
        """

        return self.wordBank
    

    def ParseURL(self, url: str = "", saveDirectory: str = "") -> bool:
        """
        Parse word bank from given URL that ends with .txt

        If no url is supplied, will get the source from https://nglam.dev/resources/wbr-auto.txt
        """

        if not url:
            url = "https://nglam.dev/resources/wbr-auto.txt"

        if not url.endswith(".txt"):
            WBR_Console.PrintError("Given link doesn't result in a .txt file!")
            return False
        
        response = requests.get(url)
        response.raise_for_status()

        wordBank = response.text

        if not saveDirectory:
            saveDirectory = os.path.join(os.getcwd(), "data", "data.txt")
        
        with open(saveDirectory, "w") as f:
            f.write(wordBank)

        self.wordBank = wordBank.strip().split("\n")

        self.ParseFile(saveDirectory)

        return True
    
    def ParseFile(self, filePath: str = "") -> bool:
        """
        Parse from .txt file in filePath.
        If no filePath is supplied, will get one in resources/data.txt
        """
        if not filePath:
            filePath = os.path.join(os.getcwd(), "data", "data.txt")

        if not filePath.endswith(".txt"):
            WBR_Console.PrintError("Given directory doesn't result in a .txt file!")
            return False
        
        with open(filePath, "r") as f:
            self.wordBank = f.read().strip().split("\n")

        return True
    
    @staticmethod
    def RemoveNumbers(s: str) -> str:
        """
        Removes all numbers inside the string 's'.

        For example string "abc123" -> "abconetwothree"
        """

        nums = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        finalized = ""

        for char in s:
            try:
                char = int(char)
                finalized += nums[char]
            except:
                finalized += char

        return finalized



class WBR_Main:
    def __init__(self):
        # retrieving word bank (default from the data folder first)
        self.word_bank_instance = WBR_WordBank()
        self.word_bank_instance.ParseFile()

        # set up the words
        self.words = self.word_bank_instance.GetWordBank()

    def _MainMenu(self):

        WBR_Console.Clear()

        # intro
        print(
"""
WBR-auto V2 [Fluentix]
---------------------
WBR-auto uses selenium to scrape the what beats rock website and the provided
word bank to auto-play the game what beats rock. 
Quit by pressing Control + C.
"""
        )

        option = input(
"""
Options ------------------------
[1] Start WBR-Auto
[2] Word bank settings
[3] Contribute
--------------------------------

Enter your option: """
        )

        self._ParseOption(option)
    
    def _WordBankMenu(self):
        WBR_Console.Clear()

        print(
"""
Upload your own word bank
-------------------------
[1] From file path (.txt)
[2] From URL (.txt)
[3] Refresh word bank (from contributed word bank)
[X] Back

"""
        )

        self._ParseOptionWordBank(input("Enter your option: "))


    def _ParseOptionWordBank(self, option):
        try:
            option = int(option)

        except:
            if option.lower() == "x":
                WBR_Console.Clear()
                self._MainMenu()
                return
            
            WBR_Console.PrintError("Invalid option, press enter to try again: ")
            input()
            self._WordBankMenu()
            return

        # it is an integer
        if option == 1:
            self.word_bank_instance.ParseFile(input("Provide path to text file: "))
        elif option == 2:
            self.word_bank_instance.ParseURL(input("Provide URL to text file: "), input("[Optional] Provide directory where the text file will be saved at: "))
        elif option == 3:
            self.word_bank_instance.ParseURL()
        else:
            WBR_Console.PrintError("Invalid option, press enter to try again: ")
            input()
            self._WordBankMenu()
            return

        WBR_Console.PrintSuccess("Operation completed successfully! Returning to menu screen...")
        time.sleep(3)
        self._MainMenu()

    def _Contribute(self):
        webbrowser.open_new("https://wbr.fluentix.dev")
        WBR_Console.Clear()
        self._MainMenu()

    def _ParseOption(self, option):
        try:
            option = int(option)
        except:
            # fall back for string input, etc.
            WBR_Console.PrintError("Given option is not valid, press enter to try again.")
            input()
            WBR_Console.Clear()
            self._MainMenu()

            return
        
        # it is an integer
        if option == 1:
            self.Run()
        elif option == 2:
            self._WordBankMenu()
        elif option == 3:
            self._Contribute()
        else:
            WBR_Console.PrintError("Given option is not valid, press enter to try again.")
            input()
            WBR_Console.Clear()
            self._MainMenu()

            return


    def Run(self):
        WBR_Console.Clear()
        self.browser_instance = WBR_Browser()
        print("----------------")
        input("Press enter to start wbr-auto: ")

        for i, word in enumerate(self.words):
            word = WBR_WordBank.RemoveNumbers(word)

            WBR_Console.PrintInfo(f"Word {i+1}/{len(self.words)}...")
            WBR_Console.PrintInfo(f"Word: {word}")

            self.browser_instance.TypeWord(word)
            time.sleep(DELAY_PER_ACTION)
            self.browser_instance.ClickNextButton()
            time.sleep(DELAY_PER_WORD)

        WBR_Console.PrintSuccess(f"Finished all {len(self.words)} words!")


if __name__ == "__main__":
    WBR_Main()._MainMenu()