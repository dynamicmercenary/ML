import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import subprocess

def test_connection(recipients):
    msg = """The is a test for connection to your number. \n
            Script is now runnning. \n
            You'll be notified if a ticket is available"""

    for recipient in recipients:
        if not recipient:
            print("Recipient's phone number is not set")
            return
        else:
            applescript = f'''
            tell application "Messages"
                send "{msg}" to buddy "{recipient}" of (service 1 whose service type is iMessage)
            end tell
            '''
        subprocess.run(['osascript', '-e', applescript])

def check_availability(recipients):
    url = "https://secure.onreg.com/onreg2/bibexchange/?eventid=6087" 
    response = requests.get(url)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            #This string will be removed when a ticket is available
            unavailable_text = "Der er ikke nogen startnumre til salg i øjeblikket. Prøv igen lidt senere."

            if unavailable_text not in soup.text:
                with open('downloaded_html.html', 'w', encoding='utf-8') as f_out:
                    f_out.write(soup.prettify())
                send_notfication(recipients, url)
    except Exception as e:
        print(f"Code run into an error: {e}")
    

def send_notfication(recipients, url):
    subject = 'Ticket Available'
    body = f'Check the website: {url}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if soup.find('a', class_='btn button_cphmarathon'):
            
                # Find the <a> tag with the class "btn button_cphmarathon" not tested.
                a_tag = soup.find('a', class_='btn button_cphmarathon')

                # Extract the href attribute
                url_køb = a_tag['href']
                new_url = 'https://secure.onreg.com/onreg2/bibexchange/'
                full_url_køb = urljoin(new_url, url_køb)

                body_køb = f'Or clik here to add to shopping bag directly (might not work): {full_url_køb}'

                msg = f"{subject}\n\n{body} \n\n {body_køb}"

            else:

                msg = f"{subject}\n\n{body}"


    except Exception as e:
        print(f"Code run into an error: {e}")
    
    for recipient in recipients:
        if not recipient:
            print("Recipient's phone number is not set")
            return
        else:
            applescript = f'''
            tell application "Messages"
                send "{msg}" to buddy "{recipient}" of (service 1 whose service type is iMessage)
            end tell
            '''

        subprocess.run(['osascript', '-e', applescript])

if __name__ == "__main__":
    recipients = [] #Add you phone number here as a string

    print("Running script")

    test_connection(recipients)
    counter = 0
    while (True):
        if counter > 0:
            print(f"Running counter: {counter} times")
        counter += 1
        check_availability(recipients)
        time.sleep(60)  #wait before checking again
