"""
A  program  for  a  small  business  to  help  it
manage  tasks  assigned  to  each  member  of  the  team
"""
# ===== Importing external modules ===========
import datetime


# ==== Task Class ====
class Task:
    """
    A class representing a task.
    """
    def __init__(self, user, title, description, due_date, made, completion):
        """
        Initialise a task object.

        Args:
            user (str): The user the task is assigned to
            title (str): The task title
            description (str): The task description
            due_date (datetime): The task due date
            made (datetime): The task creation date
            completion (str): The task completion status
        """
        self.user = user
        self.title = title
        self.description = description
        self.due = due_date
        self.date_created = made
        self.completion = completion

    def get_title(self):
        """
        Function that returns the task title.
        """
        return self.title

    def get_assigned(self):
        """
        Function that returns the assigned user.
        """
        return self.user

    def is_complete(self):
        """
        Function that returns True or False based on the completion
        status.
        """
        if self.completion == "No":
            return False
        else:
            return True

    def mark_as_complete(self):
        """
        Function that sets the task completion status as completed.
        """
        self.completion = "Yes"

    def change_assigned(self, new_name):
        """
        Function that replaces the assigned user.

        Args:
            new_name (str): The assigned user replacement.
        """
        self.user = new_name

    def change_due_date(self, new_date):
        """
        Function that replaces the due date.

        Args:
            new_date (str): The due date replacement.
        """
        try:
            new = new_date.split("/")
            self.due = datetime.datetime(int(new[2]), int(new[1]), int(new[0]))
        except (ValueError, IndexError):
            print("Invalid date format. Please use dd/mm/yyyy format.")

    def is_overdue(self):
        """
        Function that returns True or False based on the overdue status
        of the task
        """
        if self.due < datetime.datetime.now():
            return True
        else:
            return False

    def __str__(self):
        """
        Function that returns a string representation of the object.
        """
        task_details = [self.user, self.title, self.description,
                        date_str(self.due), date_str(self.date_created),
                        self.completion]
        return ", ".join(task_details)


# ==== Login Section ====
def login():
    """
    Function to prompts user login and returns the logged in username.
    """
    # Open file to get user details
    users = get_users()
    if users is None:
        exit()
    else:
        while True:
            try:
                # Prompt user login details
                print("LOGIN:")
                name = input("Username: ")
                password = input("Password: ")

                # Set validity default to false
                valid_name = False
                valid_password = False

                # Check validity
                if name in users.keys():
                    valid_name = True
                    if password == users.get(name):
                        valid_password = True

                # Print error messages accordingly
                if valid_name and valid_password is True:
                    print("Login successful!")
                    return name
                elif (valid_password is False) and (valid_name is True):
                    print("Incorrect password. Please try again.\n")
                else:
                    print("User not found. Please try again.\n")
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user. Goodbye!")
                exit()
            except Exception as e:
                print(f"An unexpected error occurred during login: {e}")
                print("Please try again.\n")


# ===== Menu Functions =====
def reg_user():
    """
    Function to register a new user.
    """
    # Open file to get user details
    users = get_users()
    if users is None:
        exit()
    else:
        try:
            # Prompt new user details
            print("\nUSER REGISTRATION:")
            # First check if username already exists, default as unique
            while True:
                name = input("Username: ")
                unique = True
                if name in users.keys():
                    print("Username already exists! Try again.")
                    unique = False

                # Prompt password if username is unique
                if unique is True:
                    while True:
                        password = input("Password: ")
                        # Confirm password
                        password_again = input("Confirm Password: ")
                        if password_again == password:
                            break
                        else:
                            print("Passwords do not match! Please try again.\n")
                    break

            # Append into user file when all is valid
            try:
                with open("user.txt", "a", encoding="utf-8") as user_file:
                    user_details = f"{name}, {password}"
                    user_file.write("\n"+user_details)
                print("User registered successfully!\n")
            except FileNotFoundError:
                print("\nCannot find file 'user.txt' in order to update.")
            except IOError:
                print("\nError writing to user file.")
        except KeyboardInterrupt:
            print("\n\nRegistration cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred during registration: {e}")


def view_all():
    """
    Function to display all tasks listed in tasks.txt.
    """
    try:
        tasks = get_tasks()
        for task in tasks:
            display_task(task)
    except Exception as e:
        print(f"Error viewing all tasks: {e}")


def view_mine(username):
    """
    Function to display the current user's tasks.
    """
    try:
        # get tasks
        tasks = get_tasks()
        my_tasks = []
        task_count = 0
        # Loop through each task and print if it's for the user
        if len(tasks) > 0:
            for task in tasks:
                if username == task.get_assigned():
                    print(f"Task {task_count}:")
                    display_task(task)
                    my_tasks.append(task)
                    task_count += 1
            # Print message if no tasks for the user, else allow edits
            if task_count == 0:
                print("\nYou do not have any tasks.\n")
            else:
                # run task selection to edit or complete tasks
                select_task(my_tasks)
        else:
            print("There are no tasks available for any user.")
    except Exception as e:
        print(f"Error viewing your tasks: {e}")


def add_task():
    """
    Function to add a task to tasks.txt with user prompted details.
    """
    try:
        # Get task details from the user
        users = get_users()
        while True:
            username = input("Please give the username of the person whom the task"
                             " is assigned to: ")
            if username in users.keys():
                break
            else:
                print("That username does not exist. Try again.")
        title = input("Please give the title of the task: ")
        description = input("Please give the description of the task:\n")
        user_date = input("Please give the due date of the task (dd/mm/yyyy): ")
        split_date = user_date.split("/")
        date = datetime.datetime(int(split_date[2]), int(split_date[1]),
                                 int(split_date[0]))
        # Create task object, with defaults
        created = datetime.datetime.now()
        completed = "No"
        task = Task(username, title, description, date, created, completed)
        # Write to task file
        try:
            with open('tasks.txt', "a", encoding="utf-8") as tasks:
                tasks.write("\n"+str(task))
            print("Task added successfuly!")
        except FileNotFoundError:
            print("\nUnable to locate 'tasks.txt' to add task. Please check the "
                  "directory and try again.")
        except IOError:
            print("\nError writing to tasks file.")
    except (ValueError, IndexError):
        print("Invalid date format. Please use dd/mm/yyyy format.")
    except KeyboardInterrupt:
        print("\n\nTask addition cancelled.")
    except Exception as e:
        print(f"An unexpected error occurred while adding task: {e}")


def view_completed():
    """
    Function to display all tasks marked as complete.
    """
    try:
        # get tasks
        tasks = get_tasks()
        # count tasks completed
        task_count = 0
        # Loop through each task and print if it's completed
        for task in tasks:
            if task.is_complete():
                display_task(task)
                task_count += 1
        # Print 'error' message if no tasks compeleted
        if task_count == 0:
            print("\nThere are currently no completed tasks.\n")
    except Exception as e:
        print(f"Error viewing completed tasks: {e}")


def delete_task():
    """
    Function to delete a user specified task.
    """
    # ref: "https://www.geeksforgeeks.org/python/python-program-to-
    # delete-specific-line-from-file/"

    try:
        tasks = get_tasks()
        if len(tasks) > 0:
            # print task titles with index and assignment
            print("\nAll tasks on record:")
            for index, task in enumerate(tasks):
                title = task.get_title()
                user = task.get_assigned()
                print(f"{index} - {title} (assigned to: {user})")
        else:
            print("There are no tasks available.")
            return

        # request index to delete from user
        while True:
            delete = input("Select the number of the task you wish to delete: ")
            try:
                delete_int = int(delete)
                # get delete index and rewrite task file without that line
                if delete_int in range(0, len(tasks)):
                    try:
                        with open("tasks.txt", "w", encoding="utf-8") as task_file:
                            for index, task in enumerate(tasks):
                                if index != delete_int:
                                    # remove newline tag and rewrite
                                    plain_task = str(task).strip("\n")
                                    if index == 0:
                                        task_file.write(plain_task)
                                    else:
                                        task_file.write("\n" + plain_task)
                        # print message to indicate it is completed
                        print("Task deleted.")
                        break
                    except IOError:
                        print("Error writing to tasks file.")
                else:
                    print("That selection is invalid. Please try again.")
            except (ValueError, TypeError):
                print("Invalid input. Please only use the numbers indicated.")
            except KeyboardInterrupt:
                print("\n\nDeletion cancelled.")
                break
    except Exception as e:
        print(f"Error deleting task: {e}")


def generate_reports():
    """
    Function to generate reports base on task and user information.
    """
    try:
        # get task overview
        print("Generating task overview...")
        task_overview()

        # get user overview
        print("Generating user overview...")
        user_overview()

        print("Reports generated.")
    except Exception as e:
        print(f"Error generating reports: {e}")


def display_statistics():
    """
    Function to display generated reports on task and user information.
    """
    try:
        # print task overview
        print("TASK OVERVIEW:")
        display_task_overview()

        # print user overview
        print("USERS OVERVIEW:")
        display_user_overview()
    except Exception as e:
        print(f"Error displaying statistics: {e}")


# ===== My Functions =====
def date_str(date):
    """
    Function that returns a datetime object as a string object.
    """
    return date.strftime("%d %b %Y")


def display_task_overview():
    """
    Function that gets task overview details and prints them.
    """
    try:
        # get details
        with open("task_overview.txt", "r", encoding="utf-8") as overview:
            raw_details = overview.readlines()
        task_overview_details = []
        for details in raw_details:
            stripped = details.strip("\n")
            task_overview_details.append(stripped)
        # display details
        print("\u2500"*50)
        print(f"Total tasks: {task_overview_details[0]}")
        print(f"Tasks completed: {task_overview_details[1]}")
        print(f"Tasks incomplete: {task_overview_details[2]}")
        print(f"Overdue tasks: {task_overview_details[3]}")
        print(f"Percentage incomplete: {task_overview_details[4]}%")
        print(f"Percentage overdue: {task_overview_details[5]}%")
        print("\u2500"*50)
    except FileNotFoundError:
        print("Cannot display task statistics. No reports were generated.")
    except IOError:
        print("Error reading task overview file.")
    except Exception as e:
        print(f"Error displaying task overview: {e}")


def display_user_overview():
    """
    Function that gets user overview details and prints them.
    """
    try:
        # get details
        with open("user_overview.txt", "r", encoding="utf-8") as overview:
            raw_details = overview.readlines()
        user_overview_details = []
        for index, details in enumerate(raw_details):
            stripped = details.strip("\n")
            if index <= 1:
                user_overview_details.append(stripped)
            else:
                individual_details = stripped.split(", ")
                user_overview_details.append(individual_details)

        # display details
        print("\u2500"*50)
        print(f"Total users: {user_overview_details[0]}")
        print(f"Total tasks: {user_overview_details[1]}")
        for index, user in enumerate(user_overview_details):
            if index > 1:
                print(f"User: {user[0]}")
                print(f"\t- Total tasks: {user[1]}")
                print(f"\t- Task percentage: {user[2]}%")
                print(f"\t- Percentage completed: {user[3]}%")
                print(f"\t- Percentage incomplete: {user[4]}%")
                print(f"\t- Percentage overdue: {user[5]}%")
        print("\u2500"*50)
    except FileNotFoundError:
        print("Cannot display user statistics. No reports were generated.")
    except IOError:
        print("Error reading user overview file.")
    except Exception as e:
        print(f"Error displaying user overview: {e}")


def get_users():
    """
    Function that returns a dictionary of users, with the key as the
    username and the value as the password.
    """
    try:
        # Get user details from file
        with open("user.txt", "r", encoding="utf-8") as users:
            user_details = users.readlines()

        # Split details, add to dictionary and return
        user_dict = {}
        for line in user_details:
            user = line.strip("\n")
            details = user.split(", ")
            user_dict[details[0]] = details[1]
        return user_dict
    except FileNotFoundError:
        print("\nCannot find file 'user.txt' in order to validate.")
        return None
    except IOError:
        print("\nError reading user file.")
        return None
    except Exception as e:
        print(f"Error getting users: {e}")
        return None


def display_task(task_object):
    """
    Function that displays the details of a task object.
    """
    try:
        # get details from object
        task_details = str(task_object).split(", ")
        # ref: "https://stackoverflow.com/questions/65561243/
        # print-a-horizontal-line-in-python"
        print("\u2500"*50)
        label = ["Task:", "Assigned to:", "Date assigned:", "Due date:",
                 "Task complete?", "Task Description:"]
        # ref: "https://labex.io/tutorials/python-how-to-customize-
        # column-display-in-python-421861"
        print(f"{label[0]:<20}{task_details[1]}")
        print(f"{label[1]:<20}{task_details[0]}")
        print(f"{label[2]:<20}{task_details[4]}")
        print(f"{label[3]:<20}{task_details[3]}")
        print(f"{label[4]:<20}{task_details[5]}")
        print(f"{label[5]}\n  {task_details[2]}")
        print("\u2500"*50)
    except Exception as e:
        print(f"Error displaying task: {e}")


def select_task(tasks):
    """
    Function that prompts user selection in order to modify the current
    user's tasks.
    """
    try:
        # prompt user selection, testing for errors and task completion
        while True:
            select = input("Enter the number of the task you wish to modify.\n"
                           "(enter -1 to return to main menu): ")
            try:
                select_int = int(select)
                if select_int in range(-1, len(tasks)):
                    if select_int == -1:
                        break
                    else:
                        if not tasks[select_int].is_complete():
                            modify_task(tasks[select_int])
                            update_task_file(tasks)
                            break
                        else:
                            print("The selected task is complete and cannot be"
                                  " modified. Try again.\n")
                else:
                    print("Invalid selection. Please try again.")
            except (ValueError, TypeError):
                print("Invalid input. Please only use the numbers indicated.")
            except KeyboardInterrupt:
                print("\n\nSelection cancelled.")
                break
    except Exception as e:
        print(f"Error selecting task: {e}")


def update_task_file(user_tasks):
    """
    Function to replace modified tasks and update the task file.
    """
    try:
        tasks = get_tasks()
        # replace modified user tasks
        for index, task in enumerate(tasks):
            for user_task in user_tasks:
                if task.get_title() == user_task.get_title():
                    tasks[index] = user_task

        # update task file
        with open("tasks.txt", "w", encoding="utf-8") as task_file:
            for index, task in enumerate(tasks):
                if index == 0:
                    task_file.write(str(task))
                else:
                    task_file.write("\n" + str(task))
    except IOError:
        print("Error updating task file.")
    except Exception as e:
        print(f"Error updating task file: {e}")


def modify_task(task):
    """
    Function to modify task details based on user prompted selection.
    """
    try:
        # display and prompt modification options
        while True:
            selection = input("\nWould you like to:\n1. Mark task as complete\n"
                              "2. Edit the task\nEnter your selection: ")
            if selection == '1':
                task.mark_as_complete()
                print("Task marked as completed!")
                break
            elif selection == '2':
                # prompt for user edit choices
                while True:
                    edit_user = input("Would you like to edit the assigned user?"
                                      "\n(1 = Yes, 2 = No): ")
                    if edit_user in ['1', '2']:
                        edit_date = input("Would you like to edit the due date?"
                                          "\n(1 = Yes, 2 = No): ")
                        if edit_date in ['1', '2']:
                            break
                    print("Invalid input. Please try again.")
                # prompt for changes, and change task details
                if edit_user == '1':
                    users = get_users()
                    while True:
                        print("Please enter the new details: ")
                        user_change = input("Assigned user: ")
                        if user_change in users:
                            task.change_assigned(user_change)
                            break
                        else:
                            print("That user does not exist.")
                if edit_date == '1':
                    print("Please enter the new details: ")
                    date_change = input("Due date (dd/mm/yyyy): ")
                    task.change_due_date(date_change)
                break
            else:
                print("Invalid selection. Please enter only the number.")
    except KeyboardInterrupt:
        print("\n\nModification cancelled.")
    except Exception as e:
        print(f"Error modifying task: {e}")


def get_tasks():
    """
    Function that returns a list of task objects retrieved from the
    task file.
    """
    # get tasks from file, returns list of objects
    tasks = []
    try:
        with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
            for line in tasks_file:
                clean_line = line.strip("\n")
                detail = clean_line.split(", ")
                due = datetime.datetime.strptime(detail[3], "%d %b %Y")
                created = datetime.datetime.strptime(detail[4], "%d %b %Y")
                task_object = Task(detail[0], detail[1], detail[2], due,
                                   created, detail[5])
                tasks.append(task_object)
        return tasks
    except FileNotFoundError:
        print("\nCannot find tasks.txt to access tasks.\n")
        return []
    except (ValueError, IndexError):
        print("\nError parsing tasks file. Check file format.\n")
        return []
    except Exception as e:
        print(f"\nError getting tasks: {e}\n")
        return []


def task_overview():
    """
    Function that retrieves and calculates task statistics, then saves
    the details onto a file.
    """
    try:
        # set defaults and get necessary details
        tasks = get_tasks()
        total_tasks = len(tasks)
        completed_tasks = 0
        incomplete_tasks = 0
        overdue = 0
        # count specific tasks
        for task in tasks:
            if not task.is_complete():
                incomplete_tasks += 1
                if task.is_overdue():
                    overdue += 1
            else:
                completed_tasks += 1
        # calculate task percentages
        incomplete_percentage = round(((incomplete_tasks/total_tasks)*100), 2) if total_tasks > 0 else 0
        overdue_percentage = round(((overdue/total_tasks)*100), 2) if total_tasks > 0 else 0
        # write to task overview file
        overview_details = [total_tasks, completed_tasks, incomplete_tasks,
                            overdue, incomplete_percentage, overdue_percentage]
        with open("task_overview.txt", "w", encoding="utf-8") as task_overview:
            for index, detail in enumerate(overview_details):
                if index == 0:
                    task_overview.write(str(detail))
                else:
                    task_overview.write("\n" + str(detail))
    except IOError:
        print("Error writing task overview file.")
    except Exception as e:
        print(f"Error generating task overview: {e}")


def user_overview():
    """
    Function that retrieves and calculates user statistics, then saves
    the details onto a file.
    """
    try:
        # set defaults and get necessary details
        tasks = get_tasks()
        total_tasks = len(tasks)
        users_dict = get_users()
        if users_dict is None:
            return
        users = list(users_dict.keys())
        user_details = []
        user_count = 0
        # count specific details per user
        for user in users:
            # Set user defaults
            user_tasks = 0
            user_completed = 0
            incomplete = 0
            user_overdue = 0
            user_count += 1
            for task in tasks:
                # count user details
                if task.get_assigned() == user:
                    user_tasks += 1
                    if task.is_complete():
                        user_completed += 1
                    else:
                        incomplete += 1
                        if task.is_overdue():
                            user_overdue += 1
            # calculate percentages
            task_percentage = round(((user_tasks/total_tasks)*100), 2) if total_tasks > 0 else 0
            if user_tasks == 0:
                completed_percentage = 0.00
                incomplete_percentage = 0.00
                overdue_percentage = 0.00
            else:
                completed_percentage = round(((user_completed/user_tasks)*100), 2)
                incomplete_percentage = round(((incomplete/user_tasks)*100), 2)
                overdue_percentage = round(((user_overdue/user_tasks)*100), 2)
            # create list of details and append to user details list
            details = [str(user), str(user_tasks), str(task_percentage),
                       str(completed_percentage), str(incomplete_percentage),
                       str(overdue_percentage)]
            user_details.append(details)
        # write to user overview file
        with open("user_overview.txt", "w", encoding="utf-8") as overview:
            overview.write(str(user_count))
            overview.write("\n" + str(total_tasks))
            for detail in user_details:
                overview.write("\n" + ", ".join(detail))
    except IOError:
        print("Error writing user overview file.")
    except Exception as e:
        print(f"Error generating user overview: {e}")


# ===== Main Menus =====
def main_menu(current_user):
    """
    Function that displays the main menu and prompts user selection.
    """
    while True:
        try:
            # Present the menu to the user and
            # make sure that the user input is converted to lower case.
            menu = input(
                '''\nSelect one of the following options:
a - add task
va - view all tasks
vm - view my tasks
l - log out
e - exit
: '''
            ).lower()

            if menu == 'a':
                add_task()

            elif menu == 'va':
                view_all()

            elif menu == 'vm':
                view_mine(current_user)

            elif menu == 'l':
                print("Logged out successfully.\n")
                break

            elif menu == 'e':
                print('Goodbye!!!')
                exit()

            else:
                print("You have entered an invalid input. Please try again.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            exit()
        except Exception as e:
            print(f"An unexpected error occurred in main menu: {e}")


def admin_menu(current_user):
    """
    Function that displays the admin-only menu and prompts user
    selection.
    """
    while True:
        try:
            # Present the menu to the user and
            # make sure that the user input is converted to lower case.
            menu = input(
                '''\nSelect one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete tasks
ds - display statistics
gr - generate report
l - log out
e - exit
: '''
            ).lower()

            if menu == 'r':
                reg_user()

            elif menu == 'a':
                add_task()

            elif menu == 'va':
                view_all()

            elif menu == 'vm':
                view_mine(current_user)

            elif menu == 'vc':
                view_completed()

            elif menu == 'del':
                delete_task()

            elif menu == 'ds':
                display_statistics()

            elif menu == 'gr':
                generate_reports()

            elif menu == 'l':
                print("Logged out successfully.\n")
                break

            elif menu == 'e':
                print('Goodbye!!!')
                exit()

            else:
                print("You have entered an invalid input. Please try again.\n")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            exit()
        except Exception as e:
            print(f"An unexpected error occurred in admin menu: {e}")


# ===== Main Program =====
def main():
    """
    Main program function with error handling.
    """
    try:
        while True:
            user = login()
            if user == "admin":
                admin_menu(user)
            else:
                main_menu(user)
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
    except Exception as e:
        print(f"A critical error occurred: {e}")
        print("Program terminated.")


if __name__ == "__main__":
    main()