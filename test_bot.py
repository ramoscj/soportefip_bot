import subprocess

# completed = subprocess.call('echo $PATH', shell=True)
# print('returncode:', completed)

cp = subprocess.run(["mkdir", "prueba"],shell=True)

if cp.returncode:
    print(cp.returncode)