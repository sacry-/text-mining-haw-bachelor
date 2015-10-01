
1. Continuous scraping

2. Normalizing the results 
  
  - html cleanup
  - timestamps
  - meta data
  - invalid results (charsets)

3. Continuous persistence
  
  - Using elasticsearch (date/article/id e.g. 20150707/article/a_title)
  - build a raw_data dump facility to save data

4. Preprocess data

  - tokenize + pos-tag
  - noun-phrases/ner-tags
  - persist using Elasticsearch (date/pre/id e.g. 20150707/pre/a_title)

5. Feature extraction (repeatable)

6. Clustering based on features 

    - Clustering strategies
    - Persist/cache clusters
    - feature extraction on clusters for meta categorization
      e.g. semantic modelling: Use Wordnet, Wikipedia or Google to connect points

7. Continuous clustering:
  
  - All above one day
  - All above two days
  - All above n days

8. Present results
  
  - Measure quality of a cluster
  - Measure overall subjective quality
  - Show what is good
  - Show generall weakness
  - Show how it can be improved
  - Explain limits
  - Explain how summarization would be integrated
