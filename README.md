SETUP INSTRUCTIONS PERTAIN TO THOSE LOGGING IN THROUGH THE UT STUDENT PORTAL

Setup:

1. Go to https://chromedriver.chromium.org/downloads and install the chromedriver that supports your version of Chrome

2. In the root directory, or otherwise C:/Users/usr/, create a new directory and store 'chromedriver.exe' that was downloaded in step 1

3. Open the terminal and cd to the directory you just created (e.g. cd C:\Users\usr\directory\)

4. Copy and paste: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\usr\directory\localhost"
(A Chrome browser should immediately open upon entering this command)

5. Create a .env file containing the following:

'eid_password' = REPLACE_WITH_EID_PASSWORD

6. Clone this repo locally and create a directory called `data`. Within `data`, create two directories called `article_soup` and `clean`

7. I'm going to add a requirements.txt soon, but for now here's what you'll need to install yourself to run the notebook:

  pandas
  dotenv
  selenium
  regex
  bs4


Usage:

1. Open the the notebook scrape.ipynb

2. At the bottom of the notebook, you will see: get_all_frequencies(some_ut_eid, os.get.env('eid_password'), "C://Users/usr/directory/chromedriver.exe")

3. Change `some_ut_eid` to your UT eid

4. Change "C://Users/usr/directory/chromedriver.exe" to the path of wherever you put 'chromedriver.exe' in setup

5. If `search_list.pickle` exists, delete the file from factiva/code

5. Run the whole notebook


Side notes:

This scraper will automatically search and store data in your repo. If you stop the scraper or it stops because of an error, it will pick up where it left off. However, it will only pick up after the last full year completed.


**** ONCE THE PROGRAM HAS RUN ONCE, DO NOT DELETE 'search_list.pickle' UNTIL THE LIST HAS BEEN EXHAUSTED ****


Next steps:

1. I would like to create a method that searches all years initially, so as to disclude the years without any articles. I think we could use the html in the frequency graph shown in the top left of the results page.

2. I'm still fixing bugs as they appear

If you'd like to contribute, email me at george.longoria@utexas.edu
