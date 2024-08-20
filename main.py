from extractor.analyze import Analyzer
from extractor.clean import Cleaner
from extractor.collect import JobDescriptionCollector



def main():
    # url = "https://www.glassdoor.ca/Job/data-engineer-jobs-SRCH_KO0,13.htm"
    # url="https://www.glassdoor.ca/Job/data-analyst-jobs-SRCH_KO0,12.htm"
    # url = "https://www.glassdoor.ca/Job/vancouver-entry-level-software-developer-jobs-SRCH_IL.0,9_IC2278756_KO10,40.htm"
    url = "https://www.glassdoor.ca/Job/vancouver-bc-data-analyst-jobs-SRCH_IL.0,12_IC2278756_KO13,25.htm"
    output_csv = 'job_data'

    collector = JobDescriptionCollector(num_jobs=3, file_name = output_csv)
    cleaner = Cleaner()

    collector.extract(url, verbose = True)

    doc, output_file_path = cleaner.clean(f"/output/{output_csv}.csv")
    
    # analyzer = Analyzer(doc)

    # analyzer.analyze()


if __name__ == "__main__":
    main()