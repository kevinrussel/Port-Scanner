import cmd


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

    def do_quit(self,arg):
        print("Thank you for trying SYNX \n")
        return True

synx().cmdloop()