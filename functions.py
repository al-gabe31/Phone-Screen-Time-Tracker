import sqlite3

def get_time_length(time_str:str) -> int:
    """
    Converts a time string in the format Xh XXm or XXm into the number of minutes (integer)

    time_str: The time string format as either Xh XXm or XXm

    returns: The number of minutes as an integer
    """

    data = time_str.split(' ')

    # Format is XXm or Xh
    if len(data) == 1:
        # XXm format
        if data[0][-1] == "m": # minute
            return int(data[0][:len(data[0]) - 1])
        
        # Xh format
        elif data[0][-1] == "h": # hour
            return int(data[0][:len(data[0]) - 1]) * 60

    # Format is Xh XXm
    elif len(data) == 2:
        return (int(data[0][:len(data[0]) - 1]) * 60) + int(data[1][:len(data[1]) - 1])

def read_command() -> dict:
    """
    Reads the data in command.txt and returns a dictionary containing the date string as well as all apps and their time duration for that day

    returns: A dictionary of the stuff I just said earlier lol
    """

    date_str = ""
    app_data = {}

    with open('command.txt', 'r') as file:
        line_num = 1
        
        for line in file:
            line = line.strip()
            # Adds the date string (which should be the first line in command.txt)
            if line_num == 1:
                date_str = line
            # Adds each app data where the app name is the key and the number of minutes is the value
            else:
                line_data = line.split(':')
                app_data[line_data[0]] = get_time_length(line_data[1])

            line_num += 1
    
    return {
        "date_str": date_str,
        "app_data": app_data
    }

def read_result(result:dict):
    """
    Reads the result from read_command and prints its contents

    returns: None
    """

    print(result["date_str"])
    for data in result["app_data"]:
        print(f"{data} - {result['app_data'][data]}")

def value_in_table_column(table:str, column:str, value) -> bool:
    """
    Checks if a certain value in a table at a specific column exists

    table: The table we want to check
    column: The name of the column we want to check
    value: The value we want to check if it exists in the table

    returns: Boolean that tells us if the value exists in the table
    """
    
    connection = sqlite3.connect('screen_time.sqlite')
    cursor = connection.cursor()

    cursor.execute(f"SELECT {column} FROM {table}")
    query = cursor.fetchall()

    # Table is empty
    if len(query) == 0:
        connection.close()
        return False
    
    for result in query:
        # Match found
        if result[0] == value:
            connection.close()
            return True
    
    connection.close()

    return False

# RESUME
def execute_result():
    """
    Executes the result from read_command (i.e. add new data into the database)

    returns: None
    """

    result = read_command()

    # We first have the check that the date string currently isn't in the Entry database (to prevent duplicate entries)
    if value_in_table_column("Entry", "date_str", result["date_str"]) == True:
        print(f"DATE {result['date_str']} IS CURRENTLY IN THE DATABASE. CANCELED EXECUTION")
        return # Stops the function
    else:
        print(f"DATE {result['date_str']} IS NEW. PROCEED")

    # Then, go through each app and checks if any of them are new
    # If any of them are new (i.e. currently not in the App_List database), verify to the user that new apps are detected
    # If the user responds with "y", then proceed; otherwise, cancel the process (typo might've been made)
    new_app_found = False
    new_apps = []
    for app in result["app_data"]:
        if value_in_table_column("App_List", "app_name", app) == False: # New app found
            new_app_found = True
            new_apps.append(app)
    
    if new_app_found:
        print("NEW APPS DETECTED")
        for app in new_apps:
            print(f"\t- {app}")
        
        verification = str(input("VERIFY THAT YOU WANT TO CONTINUE [y]: "))

        if verification == "y":
            print("ADDING NEW APPS TO App_List DATABASE")
            connection = sqlite3.connect('screen_time.sqlite')
            cursor = connection.cursor()

            for app in new_apps:
                cursor.execute(f"""
                                INSERT INTO App_List (app_name)
                                VALUES ('{app}');
                """)
            
            connection.commit()
            connection.close()
        else:
            print("CANCELED EXECUTION")
            return # Stops the function
    
    # Once all verifications are done, we continue with adding all the data to the database
    connection = sqlite3.connect('screen_time.sqlite')
    cursor = connection.cursor()
    
    # First, add the new entry data
    cursor.execute(f"""
                    INSERT INTO Entry (date_str)
                    VALUES ('{result['date_str']}')
    """)

    # Then, go through each app data and add it to the database
    # It contains the app at that particular date as well as how many minutes of screentime it was used on that day
    for app in result['app_data']:
        cursor.execute(f"""
                        INSERT INTO App_Data (entry_ID, app_name, time_duration)
                        VALUES ()
        """) # RESUME
    
    print("EXECUTION FINISHED")
    connection.commit()
    connection.close()

def read_SQL(file:str):
    """
    Reads an executes an SQL file using sqlite3

    file: The SQL file to read

    returns: None
    """

    connection = sqlite3.connect('screen_time.sqlite')
    cursor = connection.cursor()

    command = "" # The SQL command we want to execute

    # Reads the SQL file
    with open(file, 'r') as file:
        for line in file:
            command += line.strip() + '\n'
    
    command = command.split(';') # Splits the commands instruction by instruction

    # Executes the SQL commands line by line
    for i in range(len(command)):
        cursor.execute(command[i])
    
    connection.commit()
    print(f"{file.name} Successfully Executed")

    connection.close()

# END OF FILE