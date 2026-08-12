import cmd
import os
import subprocess

from port_scanner import ScanPort


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
   

    def do_clear(self,arg):
        ''' Clears the terminal.'''
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

    def _build_scan_parser(self,scan_type):
        parser = ShellArgParser(prog=scan_type, add_help=False)
        parser.add_argument("-p", dest="port", type=int, nargs=2,
                            metavar=("START", "END"), required=True,
                            help="start and end port")
        return parser

    def help_synscan(self):
        parser = self._build_scan_parser("synscan")
        parser.print_help() 

    def help_finscan(self):
        parser = self._build_scan_parser("finscan")
        parser.print_help()

    def help_nullscan(self):
            parser = self._build_scan_parser("nullscan")
            parser.print_help()
    def help_xmasscan(self):
            parser = self._build_scan_parser("synscan")
            parser.print_help() 

    def do_synscan(self,arg):
        port_scanner = ScanPort()
        parser = self._build_scan_parser("synscan")

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
            port_scanner.run(type_of_scan="synscan")
        else:
            port_scanner.run(start, end,"synscan")
        self.print_open_ports()

    def do_finscan(self,arg):
        port_scanner = ScanPort()
        parser = self._build_scan_parser("finscan")


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
            port_scanner.run(type_of_scan="finscan")
        else:
            port_scanner.run(start, end,"finscan")
        self.print_open_ports()


    def do_nullscan(self,arg):
        port_scanner = ScanPort()
        parser = self._build_scan_parser("nullscan")
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
            port_scanner.run(type_of_scan="nullscan")
        else:
            port_scanner.run(start, end,"nullscan")
        self.print_open_ports()
    do_exit = do_quit
synx().cmdloop()