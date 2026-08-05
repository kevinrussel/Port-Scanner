import cmd
import os
import subprocess
import port_scanner


import argparse
import shlex

class ArgParseError(Exception):
    pass

class ShellArgParser(argparse.ArgumentParser):
    """argparse normally calls sys.exit() on error — override that
    so a bad command doesn't kill the whole cmd loop."""
    def error(self, message):
        raise ArgParseError(message)


class synx(cmd.Cmd):
    intro = r"""  _______     ___   ___   __
  / ____\ \   / / \ | \ \ / /
 | (___  \ \_/ /|  \| |\ V / 
  \___ \  \   / | . ` | > <  
  ____) |  | |  | |\  |/ . \ 
 |_____/   |_|  |_| \_/_/ \_\ 
 
 """
    prompt = "synx > "
    def do_hi(self,arg):
        print("this is working")

    def do_clear(self,arg):
        if os.name == 'nt':
            subprocess.run('cls')
        else:
            subprocess.run('clear')
        
    def do_quit(self,arg):
        '''This will quit the synx shell'''
        print("Thank you for trying SYNX \n")
        return True



    def do_port(self,arg):
        print(arg)    
        port_scanner.run()


    do_exit = do_quit
synx().cmdloop()