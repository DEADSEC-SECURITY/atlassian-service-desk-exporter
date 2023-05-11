#  Copyright (c) 2023.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

# Built-In Imports
import subprocess

# 3rd-Party Imports


# Local Imports

def check_chromedriver_installed() -> bool:
    """
    Checks if the chromedriver is installed

    :return:
    """
    try:
        subprocess.check_output(['chromedriver', '-v'])
        return True
    except subprocess.CalledProcessError:
        return False

