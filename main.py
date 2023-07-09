import questionary
import distro
import os
import logging
import logging_config

# config logging
logging_config.configure_logging(log_level=logging.INFO, log_file="setup.log")

# system detection
# check if system is Ubuntu
def system_check():
    # verify if system is ubuntu or debian
    if distro.like() == "ubuntu" or distro.like() == "debian":
        return True
    else:
        logging.error("System is not Ubuntu or Debian")
        exit(1)
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
        import modules.create_project as create_project
        create_project.start()
    elif action == "[2] Open a project":
        import modules.open_project as open_project
        open_project.start()
    elif action == "[3] Convert tools":
        pass


if __name__ == '__main__':
    system_check()
    start()