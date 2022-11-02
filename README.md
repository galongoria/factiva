SETUP INSTRUCTIONS PERTAIN TO UT STUDENTS

Setup:

1. Go to https://chromedriver.chromium.org/downloads and install the chromedriver that supports your version of Chrome

2. In the root directory, or otherwise C:/Users/usr/, create a new directory and store 'chromedriver.exe' that was downloaded in step 1

3. Open the terminal and copy and paste: cd C:\Program Files (x86)\Google\Chrome\Application

4. Copy and paste: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\usr\directory\localhost"
(A Chrome browser should immediately open upon entering this command)

5. I'm going to add a requirements.txt soon, but for now here's what you'll need to install yourself to run the notebook:

  pandas
  python-dotenv
  selenium
  regex
  bs4

** Optional ** – Only necessary if you want to contribute
6. Create a .env file containing your eid password

Usage:

1. Open the the notebook scrape.ipynb

2. Replace all the variables at the top with names relevant to you

3. Run the whole notebook

Side notes:

This scraper will automatically search and store data in your repo. If you stop the scraper or it stops because of an error, it will pick up where it left off. However, it will only pick up after the last full year completed.


**** ONCE THE PROGRAM HAS RUN ONCE, DO NOT DELETE 'searches.pickle' UNTIL THE LIST HAS BEEN EXHAUSTED ****

If you delete 'searches.pickle', you will lose where you left off and will need to start the scraping process from the first search.


Next steps:

1. When the program runs for a long time, the user is signed out and the scraper stops working. I'm trying to determine where this happens and fix the issue.
2. In step4_scraper, the articles save in a list of lists for some reason. If someone sees where/why the code does this point it out and I'll change it because this isn't good
2. I'm still fixing bugs as they appear

If you are a UT student and would like to contribute, email me at george.longoria@utexas.edu
