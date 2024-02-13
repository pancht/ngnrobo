"""
=====================CAUTION=======================
DO NOT DELETE THIS FILE SINCE IT IS PART OF NROBO
FRAMEWORK AND IT MAY CHANGE IN THE FUTURE UPGRADES
OF NROBO FRAMEWORK. THUS, TO BE ABLE TO SAFELY UPGRADE
TO LATEST NROBO VERSION, PLEASE DO NOT DELETE THIS
FILE OR ALTER ITS LOCATION OR ALTER ITS CONTENT!!!
===================================================

@author: Panchdev Singh Chauhan
@email: erpanchdev@gmail.com
"""
import os
import subprocess


def terminal_nogui(command) -> int:
    """run command without any terminal output"""
    return terminal(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def terminal(command=[], stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False,
             cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None,
             universal_newlines=None, debug=False):
    """
    Execute given command, command

    :param capture_output:
    :param command: command
    :return: status code
    """
    if debug is False:
        """check environment debug flag"""
        from nrobo import EnvKeys
        if str(os.environ[EnvKeys.DEBUG]) == "True":
            debug = True

    try:
        if text and capture_output:
            try:
                return subprocess.run(command, text=text, capture_output=capture_output)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with return code {e.returncode}: \n{e}")
                exit()
                return e.returncode

        if debug:
            try:
                subprocess.check_call(command)
            except subprocess.CalledProcessError as e:
                if not e.returncode == 1:
                    print(f"Command failed with return code {e.returncode}: \n{e}")
                return e.returncode
        if (stdout and stderr) or debug is False:
            try:
                subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                if not e.returncode == 1:
                    print(f"Command failed with return code {e.returncode}: \n{e}")
                return e.returncode
        else:
            try:
                subprocess.check_call(command)
            except subprocess.CalledProcessError as e:
                if not e.returncode == 1:
                    print(f"Command failed with return code {e.returncode}: \n{e}")
                return e.returncode
    except FileNotFoundError as e:
        print(f"Command failed with FileNotFoundError!\n{e}")
        return 100
    except Exception as e:
        print(f"Command failed with exception:\n\t{e}")
        return 100

    return 0
