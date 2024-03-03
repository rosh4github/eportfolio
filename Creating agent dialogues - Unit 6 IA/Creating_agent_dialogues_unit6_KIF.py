## Importing Libraries
# Imports necessary modules from the 'pyparsing' library to define and 
# parse (analyze/break down structured data into its individual components to understand/process it)
# KIF (Knowledge Interchange Format) expressions
# 
from pyparsing import Word, alphanums, Suppress, ZeroOrMore, Forward, Group, Optional, delimitedList

## Defining Syntax Elements  of KIF expressions using 'pyparsing'
# Includes symbols, parantheses, rules for constructing nested expressions

# Suppress function - specifies text patterns that should be suppressed during parsing
# 'Suppress("(")' - suppresses the opening parenthesis symbol, so it wouldn't be included in the 
# parsed output. This allows the parser to recognize nested expressions without including the 
# parentheses themselves in the parsed result.

# LPAR - left parenthesis - specifies the opening parenthesis symbol in KIF expressions
# RPAR - closing parenthesis 

# map() function applies Suppress function to each character in the string '   "()" + '"'   '
# which results ina  list of 3 Suppress objects
# This is done because we want to suppress the parsing of specific characters, 
# namely the left parenthesis '(', right parenthesis')', and double quotes ' " '.
# LPAR RPAR QUOTE - variable names assigned to results of map(). Each variable corresponds to a 
# specific character or symbol that we want to suppress during parsing
LPAR, RPAR, QUOTE = map(Suppress, "()" + '"')

# alphanums: This is a string containing all lowercase and uppercase letters (a-z, A-Z) and digits (0-9). 
# It is often used as an argument to Word to match words consisting of alphanumeric characters.
symbol = Word(alphanums + "+-*/<=>!@$%^&_:")

# Forward: This class is used to define a placeholder for a parser that is defined later. 
# It allows you to create parsers that reference each other recursively.
kif_string = Forward()

# Group: This class is used to define a parser that groups the matched tokens into a single result. 
# It allows you to apply operations to the entire group of tokens.
kif_item = Group(symbol | kif_string)

# ZeroOrMore: This class is used to define a parser that matches zero or more occurrences of a given expression.
kif_string <<= LPAR + symbol + ZeroOrMore(kif_item) + RPAR

## Define agents
# An Agent class is defined, which serves as a blueprint for creating agent objects. 
# Each agent has a name and methods to send and receive messages.
class Agent:
    # initiates a definition of a class named 'Agent'
    # __init__ method - special method called when an object of the class is created
    # ^^ initializes the object's state
    # takes 2 parameters - self: current instance of the class, and 
    # name: parameter passed when creating an instance of a class
    def __init__(self, name):
        # assigns the value of the "name" parameter passed to the __init__ method to the 'name' attribute
        # of the object 'self'
        # In other words, when an object of the Agent class is created, 
        # it will have a name attribute with the value passed during initialization.
        self.name = name

    def send_message(self, recipient, message):
        print(f"{self.name} sending message to {recipient.name}: {message}")
        # calls the receiver_message method of the 'recepient' agent, passing it to the current agent
        # 'self' as the sender and the message content 'message'
        # delivers the message
        recipient.receive_message(self, message)

    def receive_message(self, sender, message):
        print(f"{self.name} received message from {sender.name}: {message}")
        # calls the process_message method of the current agent 'self', passing it to the agent 'sender'
        # and the message content
        # processes/handles the message
        self.process_message(sender, message)

    def process_message(self, sender, message):
        # Agent specific message processing logic goes here

        # Since it is left as a pass, it doesn't contain any actual implementation.
        # 'pass' keyword = placeholder statement in Python that does nothing, allows code to be 
        # syntactically valid without any code
        pass
    
## Define agent-specific logic

class Agent1(Agent):
    def process_message(self, sender, message):
        pass

class Agent2(Agent):
    def process_message(self, sender, message):

        if message == "(Product information requested - 50inch TVs)":
            print(f"{self.name} received product info request from {sender.name}")
            stock_info = "(Stock Availability: Y)"
            hdmi_info = "(HDMI ports: 2)"
            self.send_message(sender, stock_info)
            self.send_message(sender, hdmi_info)

if __name__ == "__main__":

    # Create agents
    Alice = Agent1("Alice")
    Bob = Agent2("Bob")

    # Alice asks Bob about product info
    Alice.send_message(Bob, "(Product information requested - 50inch TVs)")
