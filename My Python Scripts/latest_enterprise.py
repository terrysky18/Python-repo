import sys
import os
import re
import pprint
import time
import operator
import shutil
import argparse

enterprise_re = re.compile (
    r"InvinceaEnterprise_Kit_(\d+)\.(\d+).(\d+)-(?P<revision>\d+)"
)

DEFAULT_PATH="\\\\beaver\\Builds"

parser = argparse.ArgumentParser ()
parser.add_argument (
    "-c",
    "--copy",
    dest="docopy",
    action='store_true',
    default=False,
)

parser.add_argument (
    "-f",
    "--forcecopy",
    dest="forcecopy",
    action='store_true',
    default=False,
)

parser.add_argument (
    "-l",
    "--launch",
    dest="dolaunch",
    action='store_true',
    default=False
)

parser.add_argument (
    "-r",
    "--revision",
    dest="revision",
    required=False,
    default=None
)

args = parser.parse_args ()

def get_installer(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".exe"):
                return os.path.join(root, f)

    return None    

def generate_sudo_cmd(installer):
    installer_base = os.path.basename(installer)
    sudo_cmd_file = os.path.join(
        os.environ["TEMP"],
        "sudo_" + installer_base + ".vbs"
    )
    
    with open(sudo_cmd_file, "w") as f:
        f.write("""
Set objShell = CreateObject("Shell.Application") 
args = Right("%s", (Len("{0}") - Len("{0}"))) 
objShell.ShellExecute "{0}",args,"","runas" 
            """.format(installer)
        )
        
    return sudo_cmd_file

def main ():
    files=os.listdir (DEFAULT_PATH)

    filtered = list ()
    for f in files:
        m = enterprise_re.match (f)
        if (m):
            if args.revision:
                if args.revision == m.group("revision"):
                    filtered.append(f)
            else:
                filtered.append(f)
    files = filtered
    # files = filter(lambda x: enterprise_re.match (x), files)
    mod_times = dict ()
    for file in files:      
        mod_times[file] = os.path.getmtime (
            os.path.join (DEFAULT_PATH, file)
        )

    sorted_mod_times = sorted (
        mod_times.iteritems (), 
        key=operator.itemgetter (1), 
        reverse=True
    )
    fname = sorted_mod_times[0][0]
    print "* Most recent:",fname

    if args.docopy:
        full_path = os.path.join (DEFAULT_PATH, fname)
        dst_path = os.path.join (os.getenv ("USERPROFILE"), "Downloads")
        dst_path = os.path.join (dst_path, fname)


        if not os.path.exists(dst_path) and not args.forcecopy:
            print "* copying to",dst_path
            shutil.copyfile (full_path, dst_path)

        if args.dolaunch:
            import subprocess
            print "* uncompressing ..."
            p = subprocess.Popen([dst_path])
            p.wait() 

            print "* upgrading/installing ..."
            newpath=dst_path[:-4]
            fname_base = os.path.basename(newpath)
                        
            try:
                installer = get_installer(newpath)
                sudo_cmd_file = generate_sudo_cmd(installer)
                cli_args = [
                    "c:/windows/system32/cscript.exe",
                    sudo_cmd_file
                ]
                print "Running:"
                pprint.pprint(cli_args)
                p = subprocess.Popen(cli_args)
                p.wait() 
            except WindowsError as we:
                if we.winerror == 740:
                    print "Need Admin to Run"
    
if __name__ == "__main__":
    main ()
