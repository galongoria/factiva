## Installing the code

Install this entire repository by either:

1. Opening the terminal and entering the command:
 
```
git clone https://github.com/galongoria/factiva.git
```

2. Downloading it from the project repository at Factiva_project/Factiva_guide/STEP4/STEP4_Austin_new_code.
  __DOWNLOAD THE ENTIRE PROJECT FOLDER, NOT JUST THE CODE FOLDER.__


## Setup – Windows Users

1. Go to https://chromedriver.chromium.org/downloads and install the chromedriver that supports your version of Chrome

2. In the root directory, or otherwise `C:/Users/usr/`, create a new folder and store 'chromedriver.exe' that was downloaded in step 1.

For the instructions refer to this folder as `step1_directory`

If my profile on Windows was called factiva_user, the path to chromedrive would be: `C:/Users/factiva_user/step1_directory/chromedriver.exe`

3. The next step is dependent on where your Chrome data is stored. 

First, try the following command in your terminal:

```
cd C:\Program Files (x86)\Google\Chrome\Application
```

If there is not error message, continue to step 4.

If you receive an error message saying, "The system cannot find the path specified.": , then try the following command:
                
```
cd C:\Program Files\Google\Chrome\Application
```

4. Enter the following command in your terminal:

```
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\usr\step1_directory\localhost"

```

(A Chrome browser should immediately open upon entering this command)

* Note that you will need to perform this step again if you close this Chrome window. You can expedite this process by copying and pasting either:

```
cd C:\Program Files (x86)\Google\Chrome\Application
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\usr\step1_directory\localhost"
```

or

```
cd C:\Program Files\Google\Chrome\Application
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\galon\step1_directory\localhost"
```


## Setup – Mac Users

## Dependencies

1. Install the necessary packages by either moving into the repository and installing the requirements.txt, or by simply opening the terminal and typing:

```
pip3 install pandas python-dotenv selenium regex bs4
```

__Optional – only necessary if you want to contribute__

2. Create a .env file containing your eid password. If you need help with this and are a UT student, please contact me using the email at the bottom of the instructions.

## Usage:

1. Open the the notebook scrape.ipynb

2. Replace all the variables at the top with names relevant to you. The notebook has detailed instructions in the first cell.

3. Run the whole notebook

## Side notes:

This scraper will automatically search and store data in your repo. If you stop the scraper or it stops because of an error, it will pick up where it left off. However, it will only pick up after the last full year completed.


### __ONCE THE PROGRAM HAS RUN ONCE, DO NOT DELETE 'searches.pickle' UNTIL THE LIST HAS BEEN EXHAUSTED__ ###

If you delete 'searches.pickle', you will lose where you left off and will need to start the scraping process from the first search.


Next steps:

1. When the program runs for a long time, the user is signed out and the scraper stops working. I'm trying to determine where this happens and fix the issue.
2. In step4_scraper, the articles save in a list of lists for some reason. If someone sees where/why the code does this point it out and I'll change it because this isn't good
2. I'm still fixing bugs as they appear

If you are a UT student and would like to contribute, email me at george.longoria@utexas.edu
