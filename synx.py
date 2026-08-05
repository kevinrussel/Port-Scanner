import cmd


class synx(cmd.Cmd):
    intro = "Welcome to synx!"
    prompt = "synx > "


synx().cmdloop()