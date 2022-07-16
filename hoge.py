import subprocess
cmd = 'bash check.sh | grep temp'
res = subprocess.run(cmd,shell=True,encoding='utf-8', stdout=subprocess.PIPE)
print(res.stdout.replace('\n',''))
