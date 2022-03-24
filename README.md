# Web Scraping and Elastic Search
 Lab1 of 2022 NCU Web Intelligence and Message Understanding
## Prior Requirement
* Elasticsearch 7.11.0 : https://www.elastic.co/downloads/past-releases/elasticsearch-7-11-0
* Java version >8 : https://jdk.java.net/java-se-ri/8-MR3
* Python 3 and essential package used in the code
## Start Running
1. Type `Python Exam.py` to run the program in command line and we will get the court's judgment we crawl from the website.
2. Run Elasticsearch.bat in another command line windows.
3. Type `Python import2es.py` in command line to import the data to elasticsearch.
4. Type `Python query_es.py` in command line so the user can input the key word，如輸入詐欺，則會印出與詐欺相關的裁判字號、裁判日期、摘要。輸入exit即可離開query system.
