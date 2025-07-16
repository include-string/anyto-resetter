import sys
import os
import subprocess
import ctypes
import time

# Check if program is running with administrator
def is_elevated():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Check elevation and relaunch if needed
def elevate_if_needed():
    if not is_elevated():
        print("Missing admin rights")
        input("Press ENTER to relaunch with admin rights")

        # Relaunch script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas",
            sys.executable,
            f'"{os.path.abspath(__file__)}"',
            None, 1
        )
        # Close current instance
        sys.exit()

# The "exploit" ; reset trial parameters in registry
def reset_trial():

    # Define Appdata folders
    folders = [
        os.path.expandvars("%AppData%\\iMyFone"),
        os.path.expandvars("%LocalAppData%\\iMyFone"),
        "C:\\ProgramData\\iMyFone"
    ]

    # Generate new GUID in hexidecimal format
    new_guid = os.urandom(16).hex().upper()
    print(f"[!] New GUID: {new_guid}\n")

    # List of labels/commands
    commands = [
        ('Deleting Anyto old GUID', 'reg delete "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /f'),
        ('Creating empty GUID key', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /f'),
        ('Updating GUID', f'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v guid /t REG_SZ /d "{new_guid}" /f'),
        ('Disabling version collection', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v bVersionCollect /t REG_SZ /d false /f'),
        ('Disabling AB test version', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v 697_ABTestVersion /t REG_SZ /d false /f'),
        ('Setting PackageSetting to A', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v 697_PackageSetting /t REG_SZ /d A /f'),
        ('Disabling AB test group', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v v697ABtest_NormalGroup /t REG_SZ /d false /f'),
        ('Resetting joystick limit', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\joystick" /v "(Default)" /t REG_DWORD /d 900 /f')
    ]

    # Loop through commands and execute through a subprocess
    for label, cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[+] {label}")
        except subprocess.CalledProcessError:
            print(f"[-] {label}")

    # Delete Appdata Folders to become a "new user"
    for folder in folders:
        if os.path.exists(folder):
            try:
                subprocess.run(f'rmdir /s /q "{folder}"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"[+] Deleted folder: {folder}")
            except subprocess.CalledProcessError:
                print(f"[-] Could not delete folder: {folder}")
        else:
            print(f"[SKIP] Folder not found: {folder}")

# Launch iMyFone AnyTo
def launch():

    # Define and check executable path
    app_path = "C:\\Program Files (x86)\\iMyFone\\iMyFone AnyTo\\AnyTo.exe"
    if not os.path.exists(app_path):
        print(f"[-] Default path not found: {app_path}")
        print("       Locate and launch AnyTo.exe manually.")
        return

    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", app_path, None, None, 1)
        print("[+] Launching iMyFone/AnyTo with admin rights...")
    except Exception as e:
        print(f"[-] Could not launch app: {e}")

# Program entry
if __name__ == '__main__':
    # Check elevation on startup
    elevate_if_needed()

    os.system("title iMyFone Trial Exploit")
    print("iMyFone Trial Exploit\n")
    print("[+] Instance is elevated")
    reset_trial()

    print("\nLaunch imyfone now? (y/n): ", end="")
    if input().strip().lower() == 'y':
        launch()
    else:
        print("Launching... Program will automatically close")
        time.sleep(2)
        sys.exit(0)