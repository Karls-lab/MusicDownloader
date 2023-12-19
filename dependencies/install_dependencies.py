import subprocess
import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
packages_file = os.path.join(this_dir, 'package_list.txt')

with open(packages_file, 'r') as f:
    packages = f.read().splitlines()

for package in packages:
    if package.startswith('#'):
        continue
    elif package not in sys.modules:
        print(f"Installing package: {package}")
        subprocess.run(['pip', 'install', package])
    
