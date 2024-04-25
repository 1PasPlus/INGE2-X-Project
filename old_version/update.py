import subprocess

# Obtenir la liste des bibliothèques
output = subprocess.check_output(['pip', 'list', '--format=freeze']).decode()
packages = [line.split('==')[0] for line in output.split('\n') if line]

# Mettre à jour chaque bibliothèque
for package in packages:
    subprocess.call(['pip', 'install', '-U', package])
