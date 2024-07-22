from aifc import Error
import pandas as pd
import string
import re

class Cleaner: 
    def __init__(self) -> None:
        pass

    def clean(self, csv_path):

        output_file = "cleaned_descriptions.txt"

        doc = pd.read_csv(csv_path)
        
        doc = doc.drop_duplicates(subset=['Job Title', 'Job Description', 'Company Name', 'Location'], keep='first')
        
        doc['Job Description'] = doc['Job Description'].apply(self.process_preprocess)
        
        self.save_to_file(doc['Job Description'], output_file )

        return doc, output_file
    
    def process_preprocess(self,x):
        x = self.convert_lower(x)
        # x = self.remove_punctuation(x)
        return x

    def save_to_file(self, dataframe, filename):
        """
        Saves a DataFrame to a text file.

        Args:
            dataframe (pandas.DataFrame): The DataFrame to save.
            filename (str): The name of the output file.
        """

        try:
            with open(filename, 'w') as file:
                file.write(dataframe.to_string())
            print(f"DataFrame saved to {filename}")
        except IOError as e:
            print(f"Error saving data to file: {e}")

    def convert_lower(self, x):
        try:
            return x.lower()
        except Error as e:
            print("Error is detected at convert_lower: ", e)
            pass

    def remove_punctuation(self, x):
        try:
            no_punc = [words for words in x if words not in string.punctuation]
            words_no_punct = ''.join(no_punc)
            return words_no_punct
        except Error as e:
            print("Error is detected at remove_punctuation: ", e)
            pass




