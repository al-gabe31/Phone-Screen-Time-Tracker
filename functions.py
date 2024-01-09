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
            if line_num == 1:
                date_str = line
            else:
                line_data = line.split(':')
                # app_data[line_data[0]] = line_data[1]
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

# RESUME
def execute_result(result:dict):
    """
    Executes the result from read_command (i.e. add new data into the database)

    returns: None
    """

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
    print(f"{file} Successfully Executed")

    connection.close()

# END OF FILE