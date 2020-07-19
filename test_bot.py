import subprocess

# completed = subprocess.call('echo $PATH', shell=True)
# print('returncode:', completed)

# , '-s', '<', 'C:\Users\Administrator\Documents\my_key.dat'
programa = 'vpncli.exe'
parametros = 'my_key.dat'
cp = subprocess.run(['C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\%s' % programa, '-s', '<', '..\..\%s' % parametros], shell=True)
# print('"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\%s"' % programa)
if cp.returncode:
    print(cp.returncode)