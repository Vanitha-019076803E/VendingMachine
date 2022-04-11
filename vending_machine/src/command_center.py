import enum

class Command(enum.Enum):
   ENTER = "ENTER"
   SHOW = "SHOW"
   RETURN = "RETURN"
   SELECT = "SELECT"
   NEW_LINE = "\n"
   TERMINATE = "TERMINATE"
   
class CommandCenter():

    def get_command(self):
        command_text = input('\nType your command: ').upper()
        if(command_text == ""):
            return (Command.NEW_LINE, [])
        else:
            command = Command[command_text.split()[0]]
            arguments = command_text.split()[1:]
            return (command, arguments)
