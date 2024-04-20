# Multi-Agent Digital Forensics System


## Overview
Python script that implements a multi-agent digital forensics system using 
multi-agent system (MAS) decentralized architecture and natural language 
processing (NLP) techniques. 

The system coordinates the search process within an evironment (dataset) of
email text files. It first reads the text files to identify any emails that
have the respective evidence (provided by an actor that serves as an input 
to this system). The system then analyzes the discovered data, and presents
the results.

There are three (3) types of agents that make up the system:
1. CoordinatorAgent 
- coordinates the search within the available email dataset
(environment) using the initial evidence provided by the actor (such as 
suspect personnel names), and the developing feedback/evidence (such as 
resulting query matches, frequently used terms within the emails, and 
top senders of the said emails),
- saves and displays the progress and results.
2. SearchAgent 
- reads and searches the emails for a match to the initial evidence,
3. AnalysisAgent 
- analyses the discovered data and reports back to the coordinator. This 
has not been explicitly used in the provided code but the placeholder/concept
has been integrated.


## Features and Libraries
- NLTK: for NLP tasks such as tokenization and stop-word removal
- Implements multi-threading for parallel execution of search agents. These 
  threads search for evidence in the email content and communicates findings
  to CoordinatorAgent (if matches are found)
- Provides functional testing to ensure the correctness of system functionalities
  (within final_new.py)
- Provides unit testing (within final_new_unittest.py)


## Usage - final_new.py 
1. Ensure that each text file contains the content of one or more emails 
   separated by '---' delimiters.

2. Open the `final_new.py` file and modify the `evidence` variable within the functional testing
   to include the evidence you want to search for.
>>  if __name__ == "__main__":

        evidence = ["term1", "term2"]

   Also modify the 'EMAIL_DATA_DIR' with the path of the dataset (email text files).

3. Run the script:

    ```
    python final_new.py
    ```

4. View the output, which includes frequently used terms and top senders (along with
   their counts).
   
   Example of an output is given below:

   Frequently used terms: [('animal', 2412), ('bat', 2241), ('cat', 1867), ('dog', 1772), ('elephant', 1608)]
   Top senders: [('sender1@example.com', 14), ('sender2@example.com', 7)]

## Usage - additional notes - final_new_unittest.py
1. Ensure that the main python program, and the name of the coordinating agent, is referenced correctly.
   In the current file, it references "final_new" and "CoordinatorAgent" (line 2).
>> from final_new import CoordinatorAgent


## References

Cohen, W. (2015) Enron Email Dataset. Available from: https://www.cs.cmu.edu/~enron/ [Accessed 28 February 2024].

Malakhov, A. (2016). Composable Multi-Threading for Python Libraries. 15th Python in Science Conference (SciPy 2016) 15-19. Available from: http://dx.doi.org/10.25080/Majora-629e541a-002 [Accessed 15 April 2024].

Mielke, S.J. et al. (2021). Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP. arXiv:2112.10508 [cs]. Available from: https://arxiv.org/abs/2112.10508 [Accessed 15 April 2024].

Open AI ChatGPT-3.5 (2024) ChatGPT response to Roshni Kasturi, 15 April.

Python Software Foundation (2024). threading - Thread-based parallelism. Available from: https://docs.python.org/3/library/threading.html#module-threading [Accessed 29 February 2024].

Python Software Foundation (2024). os - Miscellaneous operating system interfaces. Available from: https://docs.python.org/3/library/os.html [Accessed 29 February 2024].

Python Software Foundation (2024). unittest - Unit testing framework. Available from: https://docs.python.org/3/library/unittest.html [Accessed 29 February 2024].