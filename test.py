import subprocess


output = subprocess.check_output(['pwd'],shell=True,universal_newlines=True)
print(output)
