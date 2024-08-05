import scraper as fs 

keywords = ["Baguio Fire"] 
time = 4 
csv_file = "Sample.csv" 
username = "123happyjose321@gmail.com"
password = "HappyJose123"
fs.search_fb(username, password, keywords, time, csv_file)