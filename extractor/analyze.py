from aifc import Error
from statistics import median
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from heapq import nlargest
import re
from summarizer import Summarizer, TransformerSummarizer
from transformers import pipeline 

class Analyzer:
    def __init__(self, doc) -> None:     
        self.doc = doc
        self.nlp = spacy.load('en_core_web_sm')
        self.descriptions = self.doc['Job Description']
        # self.tokens = [token.text for token in self.description]
        self.word_frequencies = {}
        self.location_frequencies = {}
        self.work_type_frequencies = {"hybrid": 0, "remote":0, "other": 0}
        self.keyword = []
        self.avg_salary = None
        self.freq_word = None
        self.stopwords = list(STOP_WORDS)
        self.bert_model = Summarizer()
        self.qa_pipeline = pipeline('document-question-answering')
        self.prompt = "How do they work: remote, hybrid, or other?"
        self.summary = []
        self.demand = 0

    def analyze(self):
        # self.summerize()
        # self.skill_trend()
        self.location_trend()
        self.work_type_trend()
        self.experience_trend()
        self.education_trend()
        self.find_salary()
        self.salary_median_trend()

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
        """

        """
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
        """
        Count the number of each location of job posts
        """
        try: 
            for location in self.doc['Location']:
                if location.text not in self.location_frequencies.keys():
                    self.location_frequencies[location.text] = 1
                else:
                    self.location_frequencies[location.text] += 1
        except Error as e:
            print("Error at location_trend: ", e)
            pass
    
    def work_type_trend(self):
        """
        Count each appearance of how they work: remote, hybrid, in person
        """
        try:
            for description in self.descriptions:
                result = self.qa_pipeline({'context': f'''{description.text}''', 'question': self.prompt})
                self.work_type_frequencies[result['answer']] += 1
        except Error as e: 
            print("Error at work type trend: ", e)
            pass

    def experience_trend(self):
        """
        Find the required expereince trend: how many years of work experience or...
        """
        try:
            pass
        except Error as e:
            print("Error at salary trend: ", e)
            pass

    def education_trend(self):
        """
        Find the required education trend: bachelor, master, phd, etc
        """
        try:
            pass
        except Error as e:
            print("Error at salary trend: ", e)
            pass
    
    def demand_trend(self):
        """
        Calculate the new job posting out of fixed number. (maybe extract 100 and divide the number of new post from the last extraction by 100)
        """
        try:
            self.demand = len(self.doc['Job Title'])
        except Error as e:
            print("Error at demand_trend: ", e)
            pass

    def find_salary(self):
        """
        Extract salary range out of the job description, and store them into a new column. 
        """
        try: 
            salary_regex = r"\$\d+(,\d{3})*(\.\d{2})?"
            for description in self.descriptions:
                salary_match = re.search(salary_regex, description.text)
                if salary_match:
                    self.doc['Salary'] = float(salary_match.group())
                else: 
                    pass
        except Error as e:
            print("Error at salary_trend: ", e)
            pass
    
    def salary_median_trend(self):
        "Find a median salary"
        try:
            salaries = [self.doc['Salary']]
            return median(salaries) 
        except (ValueError, KeyError):
            print('Error calculatin average salary. Check data format.')
            return None
    


