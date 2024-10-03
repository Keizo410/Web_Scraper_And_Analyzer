from extractor.analyze import Analyzer
from extractor.clean import Cleaner
from extractor.collect import JobDescriptionCollector



def main():
   
    url = "https://www.glassdoor.ca/Job/vancouver-c-developer-jobs-SRCH_IL.0,9_IC2278756_KO10,21.htm"
    output_csv = 'job_data'

    collector = JobDescriptionCollector(num_jobs=3, file_name = output_csv)
    cleaner = Cleaner()

    collector.extract(url, verbose = True)

    doc, output_file_path = cleaner.clean(f"/output/{output_csv}.csv")
    
    # analyzer = Analyzer(doc)

    # analyzer.analyze()


if __name__ == "__main__":
    main()