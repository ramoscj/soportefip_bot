import subprocess

# completed = subprocess.call('echo $PATH', shell=True)
# print('returncode:', completed)

# , '-s', '<', 'D:\Python\my_key.dat'
programa = 'vpncli.exe'
cp = subprocess.run(['C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\%s' % programa, '-s', '<', 'D:\Python\my_key.dat'], shell=True)
# print('"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\%s"' % programa)
if cp.returncode:
    print(cp.returncode)