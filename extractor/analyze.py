from aifc import Error
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from heapq import nlargest
import re
from summarizer import Summarizer, TransformerSummarizer

class Analyzer:
    def __init__(self, doc) -> None:     
        self.doc = doc
        self.nlp = spacy.load('en_core_web_sm')
        self.descriptions = self.doc['Job Description']
        # self.tokens = [token.text for token in self.description]
        self.word_frequencies = {}
        self.location_frequencies = {}
        self.keyword = []
        self.avg_salary = None
        self.freq_word = None
        self.stopwords = list(STOP_WORDS)
        self.bert_model = Summarizer()
        self.summary = []
        self.demand = 0

    def analyze(self):
        # self.summerize()
        self.skill_trend()

    def summarize(self):
        """Summarize the job description. The puncutation is needed to processs the text by BERT model..."""
        try:
            for description in self.descriptions:
                if(description):
                    self.summary.append(''.join(self.bert_model(f'''{description}''', min_length=60)))
                else: 
                    print("none description")
        except Error as e:
            print("Error at summarize: ", e)
            pass
    
    
    def word_count(self):
        try: 
            pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
            for token in self.descriptions:
                if(token.text in self.stopwords or token.text):
                    continue
                if(token.pos_ in pos_tag):
                    self.keyword.append(token.text)
            self.freq_word = Counter(self.keyword)
        except Error as e:
            print("Error at word_count: ", e)
            pass

    def skill_trend(self):
        """Extracts job requirements from job descriptions."""
        try: 
            requirement_regex = r"(?:requires|needs|must have|experience in|skilled in) (.*?)(?: skills|experience|\b)"  # Improved regex
            job_requirements = []  # List to store all extracted requirements

            for description in self.descriptions:
                for requirement_match in re.finditer(requirement_regex, description):  # Iterate through all matches
                    extracted_requirement = requirement_match.group(1).strip()  # Extract and clean text
                    job_requirements.append(extracted_requirement)
            print(job_requirements)
            # if job_requirements:
            #     self.doc['Job Requirements'] = job_requirements  # Store as list
            # else: 
            #     print("No job requirements detected")
        except Error as e: 
            print("Error at skill_trend: ", e)
            pass

    def location_trend(self):
        try: 
            for location in self.doc['Location']:
                if location.text not in self.location_frequencies.keys():
                    self.location_frequencies[location.text] = 1
                else:
                    self.location_frequencies[location.text] += 1
        except Error as e:
            print("Error at location_trend: ", e)
            pass

    def experience_trend(self):
        pass

    def education_trend(self):
        pass

    def certification_trend(self):
        pass
    
    def demand_trend(self):
        try:
            self.demand = len(self.doc['Job Title'])
        except Error as e:
            print("Error at demand_trend: ", e)
            pass

    def salary_trend(self):
        try: 
            salary_regex = r"\$\d+(,\d{3})*(\.\d{2})?"
            for description in self.descriptions:

                if not hasattr(description, 'text'):
                    print(f"Error: Job description object missing 'text' attribute.")
                    continue

                salary_match = re.search(salary_regex, description.text)

                if salary_match:
                    self.doc['Salary'] = float(salary_match.group())
                else: 
                    pass
        except Error as e:
            print("Error at salary_trend: ", e)
            pass
        
        try:
            salaries = [self.doc['Salary']]
            return sum(salaries) /len(salaries)
        except (ValueError, KeyError):
            print('Error calculatin average salary. Check data format.')
            return None
    


