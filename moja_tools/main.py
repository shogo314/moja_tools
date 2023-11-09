import sys
import moja_tools.commands


def main(argv):
    module_commands_dot = "moja_tools.commands."

    if len(argv) >= 1:
        module_name = module_commands_dot+argv[0]
        if module_name in sys.modules:
            module = sys.modules[module_name]
            return module.main(argv[1:])
        else:
            print(f"Command {argv[0]} does not exist.")

    d = {}
    for module_name, module in sys.modules.items():
        if module_name.startswith(module_commands_dot):
            command = module_name.removeprefix(module_commands_dot)
            d[command] = module
    print("Commands:")
    for command, module in d.items():
        print("  {:<15} {}".format(command, module.__doc__.split("\n")[0]))
    return 0
