import mongoengine
import subprocess

def global_init():
    subprocess.run(["sudo", "service", "mongod", "start"])
    p =  subprocess.Popen(["systemctl", "is-active",  "mongod"], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8').rstrip("\n")
    if output == "active":
        mongoengine.register_connection(alias='core', db='sploitstreet')
        print("[!]Started MongoDB")