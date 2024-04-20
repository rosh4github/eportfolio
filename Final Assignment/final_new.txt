#### Assignment - An agent-based digital forensics system in Python

#### Importing Modules

import re # Regex for email address matching
import nltk # For NLP tasks
import threading # For running multiple threads (subprocess) concurrently in Python
import os # For using operating-system dependent functionality. In this case - to open a .txt email file, 
          # read contents, and properly close the file (Python Software Foundation, 2024).
from collections import Counter # To count the occurences of elements in an iterable or mapping object
from nltk.tokenize import word_tokenize # To split text into word or tokens
from nltk.corpus import stopwords # Common words (the, and, is) that are often filtered out from text data 
                                  # for lack of significant meaning
#nltk.download('stopwords') # If the package is not already installed in the user's system
#nltk.download('punkt') # If the package is not already installed in the user's system

# Directory containing email text files
# For the presentation, the dataset was downloaded (Cohen, 2015).
EMAIL_DATA_DIR = "/Users/rosh/Documents/GitHub/eportfolio/Final Assignment/Directory_all"
# Defines a set of stopwords in English
stop_words = set(stopwords.words('english'))

#### Define agents

### Coordinator Agent 
class CoordinatorAgent:
    # Method takes 2 parameters - 
    # 1. self: current instance of the class; 
    # 2. evidence: expected parameter by method when creating an instance of the class
    def __init__(self, evidence):
        # - allows each instance of the class to have its own 'evidence' value
        # Evidence = suspect personnel names (as an example) for this case
        self.evidence = evidence

        # The following lines initialize the 'results', 'frequent_terms', and 
        # 'top_senders' attributes of the class instance to an empty list

        # - stores the results of the analysis performed by the digital forensics system as
        #   they are generated during investigation
        self.results = []

        # - stores the frequently used terms discovered during the analysis performed by 
        # the digital forensics system 
        self.frequent_terms = []

        # - stores the information about the top senders of emails discovered during
        # the analysis performed by the digital forensics system
        self.top_senders = []

    def coordinate_search(self):
            print("Coordinator Agent: Starting search coordination...")

            # Dataset that is being used for design has a mix of file types (.cats and .txt)
            # The following line creates a list of filenames 'email_files' in the
            # directory specified by EMAIL_DATA_DIR that have the .txt extension
            # These filenames represent text files containing email data that will be
            # processed further in the code

            # 1. os.listdir(EMAIL_DATA_DIR) - function - returns a list os strings representing
            #    all files/directory names in the specified directory
            # 2. if f.endswith('.txt') - conditional statement - filters list of files
            #    obtained from #1. It conducts a T/F check if each filename 'f' ends with .txt extension
            # 3. f for f in... - list comprehension - iterates over each 'f' obtained
            #    from function and filters them based on the condition
            email_files = [f for f in os.listdir(EMAIL_DATA_DIR) if f.endswith('.txt')]

            print(f"Coordinator Agent: Found {len(email_files)} email files.")

            ## Read emails from each text file

            # Empty list - stores contents of all email files
            emails = []

            # Loop iterates over each filename in 'email_files' list
            for file in email_files:

                # Opens each email file 'file' located in the directory for reading 'r' mode
                # 1. 'os.path.join() - function - constructs the full path to the email file being opened
                #     - joins 1 or more path components (in this case - joins the directory path
                #       with the filename 'file' to create the full path to the email file
                # 2. open(...) - built-in Python function - used to open a file and return a corresponding file object
                # 3. as f: assigns the file object returned by open() to 'f' variable
                # 4. 'f' - variable - used as a file handle within the indented block of 
                #          code following the 'with' statement
                # 5. with - statement - ensures file is properly closed after its suite
                #           finishes
                with open(os.path.join(EMAIL_DATA_DIR, file), 'r') as f:

                    # Reads contents of the current email file 'f' and splits it 
                    # into individual emails based the delimiter "---"
                    # Each email stored as a separate element in the email_content list
                    email_content = f.read().split('---')

                    # Extends the 'emails' list with the contents of the email_content list
                    # Combines all emails from all files into a single list
                    emails.extend(email_content)

            ## Create and start search agent instances that will search for evidence in the emails
                    
            # Creates a list of new instances of the 'SearchAgent' class (i.e. 'search_agents') for each email
            # 1. Each object is initialized with an email content 'email.strip()', the evidence
            #    'self.evidence' and reference to the CoordinatorAgent object 'self'         
            # 2. for email in emails - iteraters over each email in the 'emails' list. 
            #    - each 'email' represents the content of an email as a string
            # 3. email.strip - 'strip()' method is called on each 'email' which removes 
            #                   leading and trailing whitespace (whitespace characters such
            #                   as newline characters) from the string (email content)
            search_agents = [SearchAgent(email.strip(), self.evidence, self) for email in emails]

            print(f"Coordinator Agent: Activating {len(search_agents)} search agents...")
            
            # Loop - iterates over each 'SearchAgent' object in the 'search_agents' list
            for agent in search_agents:

                # Method - starts execution of run() method of each 'SearchAgent' object
                # in a  separate thread. Each thread will search for evidence in the
                # email content assigned to it
                agent.start()

            ## Loop - waits for each 'SearchAgent' thread to finish its execution before next steps
            for agent in search_agents:

                # Method ensures that main thread waits for all search agents to
                # finish their tasks before proceeding
                # Important to ensure all email searches are completed before moving
                # on to the analysis phase
                agent.join()

            ## Method called on the self object after all search agents have finished
            ## execution. Performs analysis on the results obtained from the search
            self.analyze_results()

    # Method to extract emails from the text files
    # Additionally added to support the analyze_results method, because it was originally unable 
    # to extract all relevant email addresses
    # The following code now splits each line, and the sender email is therefore easily extracted
    def extract_email(self, text):

        email_lines = text.split('\n')
        for line in email_lines:
            if "From:" in line:
                return line.split(":")[1].strip()
        return ""
    
    # Method processes emails that matched the evidence, counts the occurrences
    # of the words and sender email addresses, and prints out the results
    def analyze_results(self): 
        
            ## Count frequently used terms

            # Tokenization and stopword removal -
            # Helps system to modify the raw text to be able to better focus on relevant
            # words, and improves accuracy of entity detection (Mielke et al., 2021)
            all_words = [word_tokenize(email.lower()) for email in self.results]
            all_words = [word for sublist in all_words for word in sublist if word.isalnum() and word not in stop_words]
            
            # Creates a Counter object 'word_counts' from the list of all words
            # Counter - to count occurences of elements in a list
            word_counts = Counter(all_words)

            # Extracts five most common words + their counts from 'word_counts'
            # and assigns them to attribute 'self.frequent_terms'
            self.frequent_terms = word_counts.most_common(5)

            ## Count top senders

            # Extracts the sender information from each email in self.results

            sender_emails = []
            for email in self.results:
                email_header = self.extract_email(email)
                #print(email)

                # Define a regular expression pattern to match email addresses
                email_sender = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_header)
                #print(email_sender)
                if email_sender:
                    sender_emails.extend(email_sender)
                    #print(sender_emails)
            sender_counts = Counter(sender_emails)
            #print(sender_counts)

            # Extracts two most common sender email addresses and their counts
            self.top_senders = sender_counts.most_common(2)
            
            ## Print results
            print("Coordinator Agent: Analysis completed.")
            
            # The following prints out frequently used terms (along with their counts)
            print("Frequently used terms:", self.frequent_terms)
            # The following prints out top sender email addresses (along with their counts)
            print("Top senders:", self.top_senders)

'''
    def save_results(self): 

            # Placeholder for saving results to a file/database
            pass    

            
    def display_results(self): 
            print("Frequently used terms:")
            
            # Iterates over each item in the self.frequent_terms list 
            # Each item in the list = tuple containing a term and its count
            for term, count in self.frequent_terms:
                print(f"{term}: {count}")

            print("\nTop senders:")

            # Each item in the list = tuple containing a sender's email address and its count
            for sender, count in self.top_senders:
                print(f"{sender}: {count}")
'''

### Search Agent 
# Inherits from threading.Thread (i.e. SearchAgent is a thread that can run concurrently
# with other threads (Python Software Foundation, 2024).
# Thread that searches for evidence in the email content and communicates findings
# to CoordinatorAgent (if matches are found)        

# Threading is important for this system to achieve concurrent execution of tasks, by
# allowing for multi-core parallelism (granted smooth coordination between multi-threaded parties)
# (Malakhov, 2016)
class SearchAgent(threading.Thread): 

    # Constructor method takes these parameters:
    # 1. Email - email content to be searched for evidence
    # 2. Evidence - list of evidence to be searched for
    # 3. Coordinator - a reference to the 'CoordinatorAgent' instance, allowing the
    #                  'SearchAgent' to communicate its findings
    def __init__(self, email, evidence, coordinator): 
        threading.Thread.__init__(self)
        self.email = email
        self.evidence = evidence
        self.coordinator = coordinator

    # Method called when 'SearchAgent' thread starts executing
    # Overrides the 'run' method of the 'Thread' class
    def run(self): 

        print(f"Search Agent: Starting search for evidence in email: {self.email[:50]}...")

        # Search_email method called to search for evidence in the email content
        matches = self.search_email(self.email, self.evidence)
        
        # If matches is not empty/evidence is found, email content and evidence 
        # matches are appended to the 'results' list of the 'CoordinatorAgent'
        if matches:
            self.coordinator.results.append(self.email)
            print(f"Search Agent: Evidence found in email: {self.email[:50]}")
        else:
            print(f"Search Agent: No evidence found in email: {self.email[:50]}")    

    # Helper method used by 'run' method to search for evidence in email content
    def search_email(self, email, evidence): 

        # Tokenizes email, converts text to lowercase, and removes stopwords
        tokens = word_tokenize(email.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

        # Checks for matches between the filtered tokens and the provided evidence
        matches = [word for word in filtered_tokens if word in evidence]

        return matches

### Analysis Agent 
class AnalysisAgent: 

    def __init__(self, data): 
        self.data = data
    
    def analyze_data(self): 

        # Placeholder for analysis logic
        pass

if __name__ == "__main__":

    # Sample evidence
    # Remediation for error - make sure strings are lowercase
    evidence = ["term1", "term2"]

    # Create and start CoordinatorAgent
    coordinator = CoordinatorAgent(evidence)
    coordinator.coordinate_search()

'''
    # Save and display results
    coordinator.save_results()
    coordinator.display_results()
'''




