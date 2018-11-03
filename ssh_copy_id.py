import pexpect, sys, os

pwd = os.getcwd()
ssh_key_path = os.path.join(os.path.expanduser('~') + '/.ssh')
os.chdir(ssh_key_path)
if 'id_rsa.pub' not in os.listdir():
    print("making rsa key")
    make_key = pexpect.spawn('ssh-keygen -t rsa', )
    make_key.expect("file")
    make_key.sendline()
    make_key.expect("passphrase")
    make_key.sendline()
    make_key.expect("same")
    make_key.sendline()
    make_key.expect(pexpect.EOF)
    print('OK')
else:
    print("found rsa-key...")
print('staring ssh-copy-id')
with open(pwd + '/host.txt', "r") as f:
    for line in f:
        server_pass = line.rstrip().split()
        ssh_client = pexpect.spawn("ssh-copy-id " + server_pass[0])
        # s123sh_client.logfile=sys.stdout.buffer
        index = ssh_client.expect(["yes/no", "password", "exist","changed"])
        if index == 0:
            ssh_client.sendline("yes")
            index = ssh_client.expect(["password"])
            if index == 0:
                ssh_client.sendline(server_pass[1])
        elif index == 1:
            ssh_client.sendline(server_pass[1])
        elif index == 2:
            print(" already exist", server_pass[0])
        else:
            print(ssh_client.read().decode())
        try:
            ssh_client.expect(pexpect.EOF)
        except:
            print("wrong password", server_pass[0])
