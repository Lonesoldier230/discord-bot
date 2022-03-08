import platform
import subprocess
import os
import path
import json

def command(program):
    starting = subprocess.Popen(program, shell=True)
    starting.communicate()


def backup():
  dictionry = {"TOKEN": None, "Prefix": None, "8ball": True, "Custom_commands": {"hello": "hi how are you"}, "kick_settings": {"kick": True, "text": "[admin] kicked [member]"}, "ban_settings": {"ban": True, "text": "[admin] banned [member]"}, "unban_settings": {"unban": True, "text": "[admin] unbanned [member]"}, "role_settings": {
      "role": True, "text": "[admin] has roled [member]"}, "unrole_settings": {"unrole": True, "text": "[admin] has unroled [member]"}, "mute_settings": {"mute": True, "text": "[member] has been muted by [admin]"}, "unmute_settings": {"unmute": True, "text": "[member] has been unmuted by [admin]"}, "insult": ["people clap when they see you.They clap their hands over their eyes.,you are proof that god has a sense of humour.", "you sir are the reason god created the middle finger."], "banned_words": ["fuck", "bitch"], "banned_sites": ["https://www.pornhub", "https://xhamster"], "who_is": True, "randomn": True, "wikipedia": True}
  with open('main.json', 'w') as js:
    json.dump(dictionry,js ,indent=4)

#main program changes running location so that there is no issue
path1 = path.__file__.replace('path.py', '')
paths = os.path.join(path1)
print(paths)
os.chdir(paths)
try:
    che = open('main.py','r')
    che.close()
    chec = open("main.json","r")
    chec.close()
    a = str(input("?:"))
    a = a.lower()
    if a == "start" or a == "s" or a== "run" or a == "r" or a == "begin" or a == "b" or a == "yes" or a == "y":
        try:
            #this makes sure that necessary modules are downloaded and there is no issue when running the program
            if platform.system().lower()== "darwin":
                command("clear")
                try:
                    import discord
                except:
                    command("pip3 install discord")
                try:
                    import wikipedia
                except:
                    command("pip3 install wikipedia")
                try:
                    import requests
                except:
                    command("pip3 install requests")
                try:
                    from googlesearch import search
                except:
                    command("pip3 install beautifulsoup4")
                    command("pip3 install google")
                command("clear")
                command("python3 main.py")
            elif platform.system().lower() == "windows":
                command("cls")
                try:
                    import discord
                except:
                    command("pip install discord")
                try:
                    import wikipedia
                except:
                    command("pip install wikipedia")
                try:
                    import requests
                except:
                    command("pip install requests")
                try:
                    from googlesearch import search
                except:
                    command("pip install beautifulsoup4")
                    command("pip install google")
                command("cls")  
                command("python main.py")
            else:
                command("clear")
                try:
                    import discord
                except:
                    command("pip install discord")
                try:
                    import wikipedia
                except:
                    command("pip install wikipedia")
                try:
                    import requests
                except:
                    command("pip install requests")
                try:
                    from googlesearch import search
                except:
                    command("pip install beautifulsoup4")
                    command("pip install google")
                command("clear")
                command("python main.py")
        except:
            print("Error:Can't find the system")
    elif a == "backup" or "reset":
        #resets the json file
        with open("main.json","w") as back:
            backup()
            print("done")
    else:
        print("so get out of here")
except:
    print("ERROR")
