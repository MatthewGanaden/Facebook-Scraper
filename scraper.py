import csv
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd
#import browser_cookie3


def search_fb(username, password, keywords, time_interval, csv_file):
    # Get the current time
    current_time = datetime.datetime.now()

    # Format and print the current time as a string
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Code started running at: " + formatted_time)

    # Set up Chrome options
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Adding argument to disable the AutomationControlled flag
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Exclude the collection of enable-automation switches
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    chrome_options.add_experimental_option("useAutomationExtension", False)
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    #chrome_options.add_argument('--headless')  # Run Chrome in headless mode


    driver = webdriver.Chrome(options=chrome_options)

    # Initializing a list with two Useragents
    useragentarray = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]

    for i in range(len(useragentarray)):
        # Setting user agent iteratively as Chrome 108 and 107
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[i]})
        print(driver.execute_script("return navigator.userAgent;"))

    driver.get("https://www.facebook.com/")

    # Find the email input field by its name attribute
    email_input = driver.find_element("name", "email")
    # Check if the element is found
    if email_input:
        # Clear any existing text in the input field
        email_input.clear()

        # Enter a new email address
        email_input.send_keys(username)

    password_input = driver.find_element("name", "pass")
    if password_input:
        password_input.clear()
        password_input.send_keys(password)
        password_input.submit()
        time.sleep(4)

    # Check if the file is empty or the first row is already populated
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        first_row = next(reader, None)

    if first_row is None:
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Post Owner', 'Text', 'Date Scraped', 'Shares', 'Comments', 'Reaction', 'Link'])

    # Open the browser and navigate to the Facebook search page
    for keyword in keywords:
        print(keyword)
        driver.get(f'https://www.facebook.com/search/posts?q={keyword}&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D')
        time.sleep(4)

        while True:
            # Store the number of div elements before scrolling
            prev_element_count = len(driver.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z'))

            # Scroll to the bottom of the page
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Wait for a short interval to allow the page to load new content
            time.sleep(time_interval)

            # Get the current number of div elements after scrolling
            curr_element_count = len(driver.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z'))

            # Check if the page has reached the bottom (no new elements loaded)
            if curr_element_count == prev_element_count:
                break
            else:
                # Locate all div elements with the specified class
                div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')

                for div_element in div_elements:
                    owner = ""
                    text = ""
                    number_of_shares = "0"
                    number_of_comments = "0"
                    number_of_reactions = "0"
                    link = ""

                    try:
                        element_href = div_element.find_element(By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h')
                        
                        get_link = div_element.find_element(By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xi81zsa')
                        link = get_link.get_attribute('href')

                        # If the href contains "#," simulate a hover action
                        # if "#" in href:
                        action = ActionChains(driver)
                        action.move_to_element(get_link).perform()
                            # Wait for a short interval to allow the page to load new content
                        time.sleep(4)

                            # Start fix from here
                            # Wait for the target element to appear
                        #date_finder = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div')
                        get_date = driver.find_element(By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1nxh6w3.x1sibtaa.xo1l8bm.xzsf02u')

                        # Extract the text from the target element
                        date = get_date.text

                        check_see_more = div_element.find_elements(By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xzsf02u.x1s688f')

                        for check in check_see_more:
                            element_text = check.text
                            if "See more" in element_text:
                                action = ActionChains(driver)
                                action.move_to_element(check).click().perform()

                        # Extract the text from the <span> element within the <a> element
                        get_owner = div_element.find_element(By.CSS_SELECTOR, 'strong span')
                        owner = get_owner.text

                        # Select the desired element
                        get_text = div_element.find_element(By.CSS_SELECTOR, 'div[dir="auto"]')
                        text = get_text.text

                        comments_shares_section = div_element.find_element(By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1qughib.x1qjc9v5.xozqiw3.x1q0g3np.xykv574.xbmpl8g.x4cne27.xifccgj')
                        get_comments_shares = comments_shares_section.find_elements(By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')
                        "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"
                        for element in get_comments_shares:
                            text_content = element.text
                            # Check if the text contains the word "comment"
                            if "comment" in text_content.lower():
                                # You've found the element with "comment," you can do further operations on it
                                number_of_comments = text_content.split()[0]
                            else:
                                # If it doesn't contain "comment," it's likely the number of shares
                                number_of_shares = text_content.split()[0]

                        element_reaction = div_element.find_element(By.CSS_SELECTOR, 'span.x1e558r4')
                        number_of_reactions = element_reaction.text

                        # Get the current time
                        date = datetime.datetime.now().isoformat()[:19].replace('T', ' ')

                        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow(
                                [owner, text, date, number_of_shares, number_of_comments, number_of_reactions, link])

                    except Exception as e:
                        # print(f"An error occurred: {e}")
                        print(f"")

    # Close the browser
    driver.quit()

    df = pd.read_csv(csv_file)
    # After collecting data, you can drop duplicates and save to the CSV file
    if 'Text' in df.columns:
        df.drop_duplicates(subset=['Text'], keep='first', inplace=True)
    df.to_csv(csv_file, index=False)

    # Get the current time
    current_time = datetime.datetime.now().isoformat()[:19].replace('T', ' ')
    print(f"Code done running at: " + current_time)