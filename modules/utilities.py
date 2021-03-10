import hashlib
import sys

def print_status(text):
    """Function to print and update text on jupyter notebook
        Args: 
            text: str
        Returns: 
    """
    sys.stdout.write("{}\r".format(text))
    sys.stdout.flush()

def calculate_md5(file_name):
    return hashlib.md5(open(file_name,'rb').read()).hexdigest()