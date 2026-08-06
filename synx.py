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
    intro = r"""   _______     ___   ___   __
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

    def print_open_ports(self,filename = "open_port.txt"):
        with open(filename,"r") as f:
            for line in f:
                print(line.strip())

    def _build_synscan_parser(self):
        parser = ShellArgParser(prog="synscan", add_help=False)
        parser.add_argument("--port", dest="port", type=int, nargs=2,
                            metavar=("START", "END"), required=True,
                            help="start and end port")
        return parser

    def do_synscan(self,arg):
        parser = self._build_synscan_parser()

        try:
            args = parser.parse_args(shlex.split(arg))
        except ArgParseError as e:
            print(f"Error: {e}")
            return
        except ValueError:
            print("Error: start/end must be integers")
            return
        start,end = sorted(args.port)
        if(start == None and end == None):
            port_scanner.run()
        else:
            port_scanner.run(start, end)
        self.print_open_ports()
       


    do_exit = do_quit
synx().cmdloop()