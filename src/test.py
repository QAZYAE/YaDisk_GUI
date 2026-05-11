import subprocess


res = subprocess.run(['yandex-disk', 'status'], capture_output=True)
print(res.stdout.decode())