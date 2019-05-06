import subprocess

#Example 1
#subprocess.check_call(['ls'])

#Example 2
# output = subprocess.check_output(['ls'])
# output = output.decode('utf-8')
# print(output)

#Example 3
try:
    output = subprocess.check_output(['ls', '-z'], stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    print(output)
except subprocess.CalledProcessError as e:
    print("command returned with return code {}".format(e.returncode))
    print(e.output.decode('utf-8'))



#Example 4
