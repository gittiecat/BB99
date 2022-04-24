import subprocess
import platform

STATUS = "status"

class ValheimClass():    
    def __init__(self, comm):
        self.command = comm
        if self.command == STATUS:
            self.response = ValheimClass.status(self)


    def status(self):
        print("we have entered")
        #shell script to check status of docker container
        if platform.system() == "Windows":
            return
        output = subprocess.run(['docker ps | grep valheim-server'], shell=True, capture_output=True)
        parse_output = str(output.stdout).strip(',').split(' ')
        filtered = list(filter(None, parse_output))
        if (len(filtered) > 1):
            return "Server is up and running!"
        else:
            return "Server is down, you need to restart it."