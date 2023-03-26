import sqlite3
import os
import sys
import subprocess
from tabulate import tabulate
import typer

cli = typer.Typer()
data = ""
result = ""
### welcome text for user
def welcome():
    ### check users input
    print("-- Hello There! --\nThis is a Command-Line Tool!",
        "\n What can you do with this tool?",
        "\n 1 - navigate the file system using Linux commands \n 2 - Enter Python script and execute",
        "\n Enter a database and search through using SQL queries or Python Script"
        "\n Save given results to file!")

### gets result by executin a sql query and saves them in given/not given file.
def addToFile(script = ""):
    global result
    resultTxt = "results.txt"
    if script.endswith("py"):
        try: 
            with open(resultTxt, "w") as f:
                for row in result:
                    f.write(",".join([str(x) for x in row]) + "\n")
            return 
        except:
            print("couldnt add result to file!")
    else:
        file = input("enter a file name - ")
        try: 
            with open(file, "w") as f:
                print("hello")
                for row in result:
                    print(row)
                    f.write(",".join([str(x) for x in row]) + "\n")
        except:
            print("couldnt add result to file")

### gets python script and result given by executin sql qeuries and manipulates that data with python script
def manipulateData(script):
    global result
    ### add result to file so it can run 
    resultTxt = addToFile(script)
    try:
        subprocess.run(['python', script,  resultTxt])
    except:
        print("error executin a script")

### gets python script from the command line and executes it
def pythonScriptExecute(script):
    try:
        subprocess.run(['python', script])
    except:
        print('Error executing Python script')
        sys.exit()

### gets argument checks if its correct linux command and executes it
def linuxExecute(command):
    cmd = command.split()
    if cmd[0] == "cd":
        try:
            os.chdir(cmd[1])
        except IndexError:
            os.chdir(os.path.expanduser("~"))
        except OSError as e:
            print(f"could change to directory {e}")
    if cmd[0] == "ls":
        try:
            files = os.listdir()
            for file in files:
                print(file)
        except OSError as e:
            print(f"could list files {e}")
    if cmd[0] == "pwd":
        print(os.getcwd())
            
### checks if given argument is a correct SQL Query
def checkNrunSQL(lstQuery):
    global data
    global result 
    query = ""
    table = []
    ### checks if given argument is a list, if it is, joins it and then executes.
    if isinstance(lstQuery, list):
        query = " ".join(lstQuery)
    else:
        query = lstQuery
    ### checks if given database exists
    if os.path.exists(data):
        try:
            if lstQuery is list:
                query = " ".join(lstQuery)
            conn = sqlite3.connect(data)
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            table.append(columns)
            result = cursor.fetchall()
            for row in result:
                table.append(row)
            ### prints out result for the user
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))  
        except sqlite3.Error as e:
            print(f"Error executin the query {e}")
    else:
        print("Database doesnt exist")

def check():
    ### create simple lists for keywords to help recognizing users input
    linuxKeywords = ["ls","cd","pwd"]
    sqlKeywords = ["SELECT","FROM"]
    global data
    global connection
    ### checks if given argument is SQL querie, Linux or Python script!
    if sys.argv[1] in sqlKeywords:
        checkNrunSQL(sys.argv[1:])
        print("Type Python Script to run it, \n 'save' To save results to file \n quit to stop the run \n or continue with SQL queries" )
        while True:
            sql = input(">> ")
            if sql.lower() == "quit":
                break
            elif sql.endswith("py"):
                manipulateData(sql)
            elif sql.lower() == "save":
                addToFile()
            else:
                checkNrunSQL(sql)
    ### checks if given argument was Python script
    elif sys.argv[1].endswith("py"):
        pythonScriptExecute(sys.argv[1])
    ### checks if given argument was linux command
    elif  sys.argv[1] in linuxKeywords:
        linuxExecute(sys.argv[1])
    else:
        print("error executin the code")

### check users input from command line
@cli.command()
def main(arg : str):
    global data
    data = input("Enter a database to get started! - ")
    check()
        
### run the program
if __name__ == "__main__":
    welcome()
    cli()