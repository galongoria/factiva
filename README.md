SETUP INSTRUCTIONS PERTAIN TO THOSE LOGGING IN THROUGH THE UT STUDENT PORTAL

Setup:

1. Go to https://chromedriver.chromium.org/downloads and install the chromedriver that supports your version of Chrome

2. In the root directory, or otherwise C:/Users/usr/, create a directory and store the chromedriver.exe file you downloaded in step 1

3. Open the terminal and cd to the directory you just created (e.g. C:\Users\usr\directory\localhost)

4. Copy and paste: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\usr\directory\localhost"
(A Chrome browser should immediately open upon entering this command)

5. Create a .env file containing the following:

'eid_password' = YOUR_UT_EID_PASSWORD

6. Clone the repo and create a directory called `data`. Within `data`, create two directories called `article_soup` and `clean`


Usage:

1. Open the the notebook scrape.ipynb

2. At the bottom of the notebook, you will see: get_all_frequencies(some_ut_eid, os.get.env('eid_password'), "C://Users/usr/directory/chromedriver.exe")

3. Change `some_ut_eid` to your UT eid

4. Change "C://Users/usr/directory/chromedriver.exe" to the path of wherever you put 'chromedriver.exe' in the setup

5. Run the whole notebook


Side notes:

This scraper will automatically search and store data in your repo. If you stop the scraper, it will only pick up after the last full year completed.


**** DO NOT DELETE 'search_list.pickle' UNTIL THE LIST HAS BEEN EXHAUSTED ****

