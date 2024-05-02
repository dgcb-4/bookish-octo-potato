# ---- CAPSTONE PROJECT ------------

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#==== Opening Section====
''' This section opens the txt file and creates one with default values if not exist
'''
# If not user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    

# =========== Function 1. Register a new user ===========
def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username
        new_username = input("New Username: ").strip()         # Remove whitespaces

       if new_username in username_password:                   # Conditional to check if the user exists 
            print("Error! Username already exists. Please choose another.")
            continue
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        
        if new_password == confirm_password:                    # Conditional to check if both passwords match 
            username_password[new_username] = new_password
            with open("user.txt", "w") as out_file:
                user_data = [f"{k};{username_password[k]}" for k in username_password]              # Format user data
                out_file.write("\n".join(user_data))
            print("New user added")
            break
        else:                                                
            print("Passwords do not match")


# =========== Function 2. Add a new task ===========       
def add_task():
    '''Allow a user to add a new task to task.txt file'''
    
    task_username = input("Name of person assigned to task: ")                # Input for user's name 
    if task_username not in username_password.keys():                         # Conditional to check in file if user exists 
        print("User does not exist. Please enter a valid username")
        return                                                                # Return to main options 

    # If user exists on file: 
    task_title = input("Title of Task: ")                                     # Inputs task information
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
            
 
    curr_date = date.today()                                        # Then get the current date
    new_task = {                                                    # Adds task info in a dictionary 
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)                                      # Adds new task into the txt file "tasks" or creates a new one too 
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# =========== Function 3. View all tasks ===========
def view_all():
    ''' Reads the tasks from task.txt file and prints to the console'''
    
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("-" * 35)                                                # Prints line to improve readability 

# =========== Function 4. View tasks for current user ===========         
def view_mine(): 
    ''' This function reads the task on the txt file assigned to the current user and allows them to edit 
        and mark them as completed
        '''
    task_indices = {}  # Dictionary to relate the shown index to the actual task index
    index = 1          # Starting the index instead of 0
    for i, t in enumerate(task_list):                   # To generate indices of tasks
            if t['username'] == curr_user:
                task_indices[index] = i
                disp_str = f"Task no. {index}: \t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                disp_str += f"Task Completed: \n {t['completed']}\n"
                index += 1 
                print(disp_str)
                print("-" * 35)                                 # Separator
                
 if not any(t['username'] == curr_user for t in task_list):
        print(f"\tThere isn't any task assigned for: {curr_user}")

# Ask the user to select a specific task or return to the main menu
    task_chose = int(input("\nEnter the specific task number or -1 to return to the main menu \n"))
    if task_chose == -1:
      return  # Return from the function (go back to the main menu)
        
# Check if the chosen number is valid 
    elif 0 < task_chose <= len(task_list) and task_chose in task_indices:
      selected_task_index = task_indices[task_chose - 1]     #Provide the actual index of the task selected 
      selected_task = task_list[selected_task_index]

      if selected_task['completed']:
        print("\nThis task has already been completed and cannot be edited.")
      else:
        task_action  = input("Action: Mark / Edit: ").lower()

        if task_action == "mark":
            task_list[selected_task_index]["completed"] = True
            print(task_list[selected_task_index]["title"], "Task marked as completed")

        # Update tasks.txt with the new completion status
            with open("tasks.txt", "r") as task_file:
                tasks = task_file.readlines()
            tasks[selected_task_index] = tasks[selected_task_index].replace("No", "Yes")

            with open("tasks.txt", "w") as task_file:
                task_file.writelines(tasks)

    elif task_action == "edit":
          # Edit username and due date
          new_username = input("Enter new username (current: " + selected_task["username"] + "): ")
          new_due_date = input("Enter new due date (current: " + selected_task["due date"] + "): ")

          selected_task["username"] = new_username
          selected_task["due date"] = new_due_date

        # Update tasks.txt with the edited task details
          with open("tasks.txt", "r") as task_file:
            tasks = task_file.readlines()

          with open("tasks.txt", "w") as task_file:
            task_file.writelines(tasks)  

          print(selected_task["title"], "Task edited successfully!")

    else:
        print("Invalid input. Please enter a number between 1 and", len(task_list), "or -1 to exit.")


# =========== Function 5. Generate text files as reports ===========         
def generating_reports():

# Overall task calculations
  total_tasks = len(task_list)
  completed_tasks = sum(task["completed"] for task in task_list)
  uncompleted_tasks = total_tasks - completed_tasks

  overdue_tasks = 0                   # Initializing the variable
  today = datetime.today()            # Obtaining today's date for the comparison
  for task in task_list:              # Loop to check all the tasks' dates
    if not task["completed"] and task["due_date"] < today:   #  Conditonal to evaluate if task is overdue or not
      overdue_tasks += 1                


  # Calculations of percentages
  percent_incomplete = (uncompleted_tasks / total_tasks) * 100
  percent_overdue = (overdue_tasks / total_tasks) * 100

  # Creates Task overview content:
  report_content = f"""
    Task Overview Report

    Total Tasks: {total_tasks}
    Completed Tasks: {completed_tasks}
    Uncompleted Tasks: {uncompleted_tasks}
    Overdue Tasks: {overdue_tasks}
    Percentage Incomplete: {percent_incomplete:.2f}%
    Percentage Overdue: {percent_overdue:.2f}%
"""

# Dictionary 'User tasks' from each user
  user_tasks = {}                                  # Dictionary to store user's tasks 
  for task in task_list:                           # Loop to check the user's tasks in the task_list 
    user = task["username"]
    if user not in user_tasks:
      user_tasks[user] = {"assigned": 0, "completed": 0, "uncompleted": 0, "overdue": 0}
    user_tasks[user]["assigned"] += 1

# Evaluating the status of the tasks 
    if task["completed"]:
      user_tasks[user]["completed"] += 1
    else:
      if task["due_date"] < today:
        user_tasks[user]["overdue"] += 1
      else:
        user_tasks[user]["uncompleted"] += 1
  

# Generates user overview content
  user_report_content = f"\nUser Overview Report\n\n"
  user_report_content += f"Total Tasks: {total_tasks}\n\n"

  for user, stats in user_tasks.items():                # Loop to obtain tasks status from each user
    assigned_tasks = stats["assigned"]
    completed_tasks = stats["completed"]
    uncompleted_tasks = stats["uncompleted"]
    overdue_tasks = stats["overdue"]

    # Percentage calculations
    percent_assigned = (assigned_tasks / total_tasks) * 100
    percent_completed = (completed_tasks / assigned_tasks) * 100 if assigned_tasks > 0 else 0
    percent_uncompleted = (uncompleted_tasks / assigned_tasks) * 100 if assigned_tasks > 0 else 0
    percent_overdue_or_uncompleted = (overdue_tasks + uncompleted_tasks) / assigned_tasks * 100 if assigned_tasks > 0 else 0

    # Report content in user file 
    user_report_content += f"\nUser: {user}\n"
    user_report_content += f"  Total Tasks Assigned: {assigned_tasks}\n"
    user_report_content += f"  Percentage of Total Tasks: {percent_assigned:.2f}%\n"
    user_report_content += f"  Percentage Completed: {percent_completed:.2f}%\n"
    user_report_content += f"  Percentage Uncompleted: {percent_uncompleted:.2f}%\n"
    user_report_content += f"  Percentage Overdue or Uncompleted: {percent_overdue_or_uncompleted:.2f}%\n\n"

  # Generate txt files (Task & user overview)
  filename = "task_overview.txt"
  with open(filename, "w") as f:
    f.write(report_content)

  filename2 = "user_overview.txt"
  with open(filename2, "w") as f:
    f.write(user_report_content)
  
  print(f"\tReports generated in files: {filename} and {filename2}")         # Successfull message for user
    

# ======== MAIN CODE AND MENU =========
''' This code reads usernames and passwords from the user.txt file  allowing the user to login.
'''
# Main code to login 
# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


#======== Main menu options =========
while True:
    # Presenting the menu to the user and ensuring that the input is converted to lowercase.
    print()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports                 
ds - Display statistics
e - Exit
: ''').lower()

# Conditionals to call the specific functions for each option selected 
    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
        
    elif menu == 'gr':
        generating_reports()
      
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about the number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")            
