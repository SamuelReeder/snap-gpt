import subprocess

condition = True

if condition:
    subprocess.run(["python", "src/login.py"])
else:
    subprocess.run(["python", "file2.py"])