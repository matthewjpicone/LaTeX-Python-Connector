#!/usr/bin/env python3
"""
    24/5/2023 9:25 pm
    Author: matthewpicone

    Project: Latex - Word Processing
    main.py  - This code is a GUI application that allows the user to write
    LaTeX documents. It can also behave as anb output engine for other
    applications and can output PDF and HTML documents using customised
    templates either in python or LaTex. The application automatically updates
    the user's parameters on run and handles document compilation and
    bibliography management.

    See readme.md for details.

    """

# MIT License
#
# Copyright (c) 2023 Matthew Picone
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#


import subprocess
import sys
import logging
import os
import tkinter as tk
from tkinter import messagebox

ENABLE_TERMINAL_LOGGING = True  # Set this flag based on your requirements
ROOT_DIR = os.path.abspath(__file__)
LOG_DIR = os.path.join(ROOT_DIR, 'log')
LOG_FILE = 'error.log'


def initialize_logging(log_dir, log_file, terminal_logging=True):
    """
    Initializes logging configuration.

    Creates the log directory if it doesn't exist and sets up the log file.
    If enable_terminal_logging is True and a terminal is available, logs will also be shown in the terminal.

    :param log_dir: A string specifying the directory path for the log file.
    :param log_file: A string specifying the log file name.
    :param terminal_logging: A boolean indicating whether to enable logging in the terminal. Default is True.
    """
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_path = os.path.join(log_dir, log_file)

        if not os.path.exists(log_path):
            with open(log_path, 'w'):
                pass

        if terminal_logging and sys.stdout.isatty():
            logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s',
                                filename=log_path)
        else:
            logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    except OSError as e:
        logging.error(f"Error occurred while initializing logging: {str(e)}")
    except Exception as e:
        logging.error(f"Error occurred while initializing logging: {str(e)}")


def show_error_message(message):
    """
    Displays an error message to the user either in a message box or through logging, depending on the availability
    of the terminal.

    :param message: The error message to display.
    """
    if ENABLE_TERMINAL_LOGGING and sys.stdout.isatty():
        # Terminal is available, log the error
        logging.error(message)
    else:
        # Terminal is not available, show a message box
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", message)

def get_word_count(tex_file: str) -> dict:
    """
    Runs the texcount executable and returns a dictionary of word counts.

    Calls the texcount executable via the subprocess module and strips the
    output into key value pairs. Removes any unnecessary strings before
    returning the dictionary.

    :param tex_file: A string containing the path to the file of interest.
    :return: A dictionary containing the returned data.
    """
    try:
        command = ['texcount', '-sum=1', '-total', tex_file]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
        temp_dict = {}
        output = output.split('\n')
        for item in output:
            temp_item = item.split(': ')
            if len(temp_item) == 2:
                temp_dict[temp_item[0]] = temp_item[1]
        return temp_dict
    except subprocess.CalledProcessError as error:
        # Handle CalledProcessError
        show_error_message(f"Error while performing a word count on {tex_file}: Command failed. Return code: {error.returncode}")
        return None
    except subprocess.TimeoutExpired as error:
        # Handle TimeoutExpired
        show_error_message(f"Error while performing a word count on {tex_file}: Command timed out: {error}")
        return None
    except OSError as error:
        # Handle OSError
        show_error_message(f"Error while performing a word count on {tex_file}: OS error occurred: {error}")
        return None
    except ValueError as error:
        # Handle ValueError
        show_error_message(f"Error while performing a word count on {tex_file}: Invalid value: {error}")
        return None
    except PermissionError as error:
        # Handle PermissionError
        show_error_message(f"Error while performing a word count on {tex_file}: Permission denied: {error}")
        return None
    except (IndexError, KeyError) as error:
        # Handle IndexError and KeyError
        show_error_message(f"Error while performing a word count on {tex_file}: Index or Key error occurred: {error}")
        return None
    except Exception as error:
        # Handle other exceptions
        show_error_message(f"Error while performing a word count on {tex_file}: Caught Exception: {str(error)}")
        return None



# import os
# import subprocess
# import yaml
# from datetime import date, datetime
# os.environ['TERM'] = 'xterm'




# # Compile LaTeX document and update bibliography using latexmk
# def compile_latex(tex_file, output_dir):
#     command = [ 'latexmk', '-lualatex' , '-f','-interaction=nonstopmode',f'--output-directory={output_dir}', tex_file]
#     command2 = ['biber', f'--output-directory={output_dir}', tex_file]
#     subprocess.run(command)
#     subprocess.run(command2)
#     subprocess.run(command)
#
# # # Compile LaTeX document and update bibliography using latexmk
# # def compile_latex(tex_file):
# #     command = ['latexmk', '-lualatex', '-bibtex', '-interaction=nonstopmode', tex_file]
# #     subprocess.run(command)
#
# # Generate LaTeX file with document details
# def generate_document_details_file(details_file, word_count, te_page):
#     # Read details from YAML file
#     with open(details_file, 'r') as f:
#         details = yaml.safe_load(f)
#
#     # Extract document details
#     university_name = details['document']['universityName']
#     trimester_num = details['document']['trimesterNum']
#     subject_code = details['document']['subjectCode']
#     subject_name = details['document']['subjectName']
#     supervisor_coordinator = details['document']['supervisorCoordinator']
#     supervisor_coordinator_name = details['document']['supervisorCoordinatorName']
#     paper_title = details['document']['paperTitle']
#     due_date = details['document']['dueDate']
#     my_name = details['document']['myName']
#     student_id = details['document']['studentID']
#
#     # Get today's date
#     today = date.today().strftime("%d/%m/%Y")
#
#     # Generate LaTeX file with document details
#     with open(te_page, 'w') as f:
#         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#         f.write(f'%! Last updated: {now}\n')
#         f.write(f'\\newcommand{{\\wordCount}}{{{word_count}}}\n')
#         f.write(f'\\newcommand{{\\universityName}}{{{university_name}}}\n')
#         f.write(f'\\newcommand{{\\trimesterNum}}{{{trimester_num}}}\n')
#         f.write(f'\\newcommand{{\\subjectCode}}{{{subject_code}}}\n')
#         f.write(f'\\newcommand{{\\subjectName}}{{{subject_name}}}\n')
#         f.write(f'\\newcommand{{\\supervisorCoordinator}}{{{supervisor_coordinator}}}\n')
#         f.write(f'\\newcommand{{\\supervisorCoordinatorName}}{{{supervisor_coordinator_name}}}\n')
#         f.write(f'\\newcommand{{\\paperTitle}}{{{paper_title}}}\n')
#         f.write(f'\\newcommand{{\\dueDate}}{{{due_date}}}\n')
#         f.write(f'\\newcommand{{\\myName}}{{{my_name}}}\n')
#         f.write(f'\\newcommand{{\\studentID}}{{{student_id}}}\n')
#%! Author = matthewpicone
# %! Date = 23/5/2023
# %! % Variables specific to UNE Essay format requirements.
#
# \newcommand{\wordCount}{10 000 000 000} % Set the word count
# \newcommand{\universityName}{University of New England} % Set the name of your university
# \newcommand{\trimesterNum}{0} % Set the trimester number
# \newcommand{\subjectCode}{SUBJECT} % Set the subject code
# \newcommand{\subjectName}{SUBJECT NAME} % Set the subject name
# \newcommand{\supervisorCoordinator}{COORDINATOR TITLE} % Set the role of the academic
# \newcommand{\supervisorCoordinatorName}{UNIT COORDINATOR} % Set the name of the coordinator or supervisor
# \newcommand{\paperTitle}{ENTER TITLE HERE} % Set the paper title
# \newcommand{\dueDate}{DUE DATE} % Set the due date of the paper
# \newcommand{\myName}{Matthew Picone} % Set your name as the author
# \newcommand{\studentID}{220260510} % Set your student ID
#
#
# # Main function
# def main():
#     tex_file = 'main.tex'
#     title_page_settings_file = 'setup/title_page_settings.tex'
#     details_file = 'details.yaml'
#     output_dir = 'out/'
#
#
#
#
#
#     # Generate LaTeX file with document details
#     # generate_document_details_file(details_file, word_count, title_page_settings_file)
#
#     # Compile LaTeX document with document details
#     compile_latex(tex_file, output_dir)
#     # Perform word count
#     word_count = f'{perform_word_count(tex_file)} '
#     # Generate LaTeX file with document details
#     generate_document_details_file(details_file, word_count, title_page_settings_file)
#     # Compile LaTeX document with document details
#     compile_latex(tex_file, output_dir)
#     print('Word count:', word_count)
#
#
# if __name__ == '__main__':
#     main()
def main():
    pass


if __name__ == '__main__':
    main()