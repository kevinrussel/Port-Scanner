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


synx().cmdloop()