import os
from colorama import init
init()
from colorama import Fore, Back, Style

def niceNumber(number):
    units = ["byte", "KB", "MB", "GB", "TB"]
    colors = [Fore.WHITE, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.BLUE]
    unitIdx = 0
    while number>1024:
        unitIdx += 1
        number/= 1024
    
    unit = units[unitIdx]
    color = colors[unitIdx]
    number = str(int(number))
    if len(number) <= 3: return number, unit, color

    startIdx = 3
    numberAsList = list(number[::-1])
    while startIdx < len(numberAsList):
        numberAsList.insert(startIdx, ",")
        startIdx += 4
    
    number = (''.join(numberAsList))[::-1]
    return number, unit, color

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
        
    return total_size

def getFolderData(start_path = '.'):
    files = os.listdir(start_path)
    
    for file in files:
        filePath = os.path.join(start_path, file)
        
        try:
            if os.path.isfile(filePath):
                if not os.path.islink(filePath):
                    total_size = os.path.getsize(filePath)
                    printFileFolderDetails(file, total_size, False, True)
                
            if os.path.isdir(filePath):
                total_size = get_size(start_path=filePath)
                printFileFolderDetails(file, total_size, True, False)
        except OSError as oserror:
            print("Failde to Load file/folder: " + filePath)
        
        

def printFileFolderDetails(name, total_size, isDir, isFile):
    appendingString = ""
    if isFile:
        appendingString += "File"
        name = "-" + name
    if isDir:
        appendingString += "Dir"
        name = "+" + name
    totale_size, units, color = niceNumber(total_size)
    print(color + "|%-30s|%-7s|%-7s|%-7s|"%(name, totale_size, units, appendingString))
    print(Fore.RESET + "------------------------------------------------------")


if __name__ == "__main__":
    import time 
    print(Fore.BLACK + Back.WHITE + "wellcome to folders manager V1.0.0" + Fore.RESET + Back.RESET)
    print()
    running = True

    while running:
        print(Fore.RED + Back.WHITE + "Pleas set the path:" + Fore.RESET + Back.RESET, end="")
        start_path = input()

        print("------------------------------------------------------")
        print("|%-30s|%-7s|%-7s|%-7s|"%("Name", "Size", "Unit", "Type"))
        print("------------------------------------------------------")
        
        try:
            startTime = time.time()
            getFolderData(start_path=start_path)
            print("Totale time took {}s".format(time.time()-startTime))
        except Exception as e:
            print(type(e).__name__)
            input("System Failed to Load Data, Press Enter To EXIT!")
            exit()
        
        user_input = input("To Exit press Enter, any other key+Enter to Continue")
        if len(user_input) == 0:
            exit()
    