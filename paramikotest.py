import paramiko
with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='192.168.153.138',username='root',password='123')
    ssh.exec_command('cd /etc')
    stdin, stdout, stderr = ssh.exec_command('ls')
    print(stdout.read())
    sftp = ssh.open_sftp()
    sftp.get('/test.txt','D:\Downloads/test*.txt')
    #sftp.get('/test1.txt','D:\Downloads\\test1.txt')
    print(23333)


