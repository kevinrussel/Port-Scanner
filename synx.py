import cmd
import os
import subprocess

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


    do_exit = do_quit
synx().cmdloop()