import scraper as fs 

keywords = ["Baguio Fire"] 
time = 4 
csv_file = "Sample.csv" 
username = ""
password = ""
fs.search_fb(username, password, keywords, time, csv_file)
