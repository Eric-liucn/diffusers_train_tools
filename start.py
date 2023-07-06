import questionary
import platform
import os
import logging
import logging_config

# config logging
logging_config.configure_logging(log_level=logging.INFO, log_file="setup.log")

# system detection
# check if system is Ubuntu
def system_check():
    if platform.system() == "Linux":
        return True
    else:
        return False


# main function
def start():
    # ask what the user wants to do
    # [1] Create new project
    # [2] Open a project
    # [3] Convert tools
    action = questionary.select(
        "What do you want to do?",
        choices=[
            "[1] Create new project",
            "[2] Open a project",
            "[3] Convert tools"
        ]
    ).ask()

    if action == "[1] Create new project":
        import create_project
        create_project.start()
    elif action == "[2] Open a project":
        import open_project
        open_project.start()
    elif action == "[3] Convert tools":
        pass


if __name__ == '__main__':
    # check if system is Linux, if not, log error and exit
    if system_check() == False:
        logging.error("System is not Linux, exiting...")
        exit()
    
    # check if system is Ubuntu, if not, log warning
    if platform.dist()[0] != "Ubuntu":
        logging.warning("This scipt only tested on Ubuntu, some packages may not work properly")

    start()