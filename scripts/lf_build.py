from west.commands import WestCommand  # your extension must subclass this
from west import log                   # use this for user output

import subprocess

class LfBuild(WestCommand):
    def __init__(self):
        super().__init__(
            'lf-build',               # gets stored as self.name
            'Compile LF program and then run west build',  # self.help
            ""
        )
        # To use a specific lfc binary the following variable can be modified
        # or the path to the desired binary can be passed to `--lfc`
        self.lfcPath = "lfc"

    def do_add_parser(self, parser_adder):
        # This is a bit of boilerplate, which allows you full control over the
        # type of argparse handling you want. The "parser_adder" argument is
        # the return value of an argparse.ArgumentParser.add_subparsers() call.
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        # Add some example options using the standard argparse module API.
        # parser.add_argument('-o', '--optional', help='an optional argument')
        # parser.add_argument('project_root', help='Path to root of project')
        parser.add_argument('main_lf', help='Name of main LF file')
        parser.add_argument('-w', '--west-commands', help='Arguments to forward to west')
        parser.add_argument('-c', '--conf-overlays', help='Additional configuration overlays')
        parser.add_argument('--lfc', help='Path to LFC binary')

        return parser           # gets stored as self.parser

    def do_run(self, args, unknown_args):
        # FIXME: The problem is that we dont control where the output of lfc is
        # routed. This is a hack and it doesnt work if the LF program is e.g. at app/src/more_dirs/HelloWorld.lf.
        srcGenPath = args.main_lf.split(".")[0].replace("src", "src-gen")

        # 1. Invoke lfc with clean flag `-c` and without invoking target
        #    compiler `n`.
        if args.lfc:
            self.lfcPath = args.lfc
        
        lfcCmd = f"{self.lfcPath} -c -n {args.main_lf}"
        print(f"Executing lfc command: `{lfcCmd}`")
        res = subprocess.Popen(lfcCmd, shell=True)
        ret = res.wait()
        if ret != 0:
            exit(1)

        # FIXME: This is a not-intuitive limitation from the users prespective.
        # But we use `-DOVERLAY_CONFIG` to mix in the prj.conf from the app
        # directory with the prj_lf.conf in the `src-gen`
        if not args.west_commands:
            args.west_commands = ""
        
        if "-DOVERLAY_CONFIG" in args.west_commands:
            print("Error: Use `--conf-overlays` option to pass config overlays to west")

        # Add config overlays
        userConfigPaths="../../prj.conf"
        if args.conf_overlays:
            userConfigPaths += f";../../{args.conf_overlays}"

        # Copy the Kconfig file into the src-gen directory
        res = subprocess.Popen(f"cp Kconfig {srcGenPath}/", shell=True)
        ret = res.wait()
        if ret != 0:
            exit(1)


        # Invoke west in the `src-gen` directory. Pass in 
        westCmd = f"west build {srcGenPath} {args.west_commands} -- -DOVERLAY_CONFIG=\"{userConfigPaths}\""
        print(f"Executing west command: `{westCmd}`")
        res = subprocess.Popen(westCmd, shell=True)
        ret = res.wait()
        if ret != 0:
            exit(1)