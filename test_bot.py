import subprocess

# completed = subprocess.call('echo $PATH', shell=True)
# print('returncode:', completed)

cp = subprocess.run(["dir"],shell=True)

print(cp.returncode)