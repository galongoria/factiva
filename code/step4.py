from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import pickle, json, os
import pandas as pd
import regex as re
from parse import (
    get_page_info,
    get_duplicates,
    get_years,
    check_frequency_chart,
    find_next_button,
)
from bot import open_page, enter_search, next_page, login, set_driver


### Directories ###
RAW_DIR = os.path.join(r"../data", "raw")
CLEAN_DIR = os.path.join(r"../data", "clean")
ARTICLE_DIR = os.path.join(r"../data", "article_hrefs")

### Input files ###
SOURCE_PATH = os.path.join(RAW_DIR, "source_codes.csv")


### Make directories ###
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs("pickles", exist_ok=True)
os.makedirs(ARTICLE_DIR, exist_ok=True)

def delete_old_pickle(input_company_file):

    """Takes in the input file name and deletes any pickles that do not contain the input string. """

    for file in os.listdir("pickles"):
        if file == ".ipynb_checkpoints":
            continue
        elif file != f"{input_company_file}_searches.pickle":
            os.remove(os.path.join("pickles", file))


def read_input_file(input_company_file):

    """Takes the input file string and uses it to read in either a csv or xlsx"""

    try:
        df = pd.read_csv(os.path.join(RAW_DIR, f"{input_company_file}.csv"))
        return df
    except FileNotFoundError:
        pass
    try:
        df = pd.read_excel(os.path.join(RAW_DIR, f"{input_company_file}.xlsx"))
        return df
    except FileNotFoundError:
        pass


def gen_output_name(input_company_file, last_name):

    """Takes in the input string and last name variables to generate an output file name.
    """
    
    output_name = "STEP4_Company_Frequency_"
    try:
        company_range = re.findall('No\d*_\d*',input_company_file)[0]
    except IndexError:
        print("Make suret the input file name includes a range of values, eg: No5301_5350")
    return f"{output_name}{company_range}_{last_name}"


def save_progress(searches_pickle, articles, df, output_file_name, PICKLE_OUTPATH):

    """Writes new lines in the csv, saves article json, and creates a new pickle to save progress."""


    CSV_OUTPATH = os.path.join(CLEAN_DIR, f"{output_file_name}.csv")
    ARTICLE_DIR = os.path.join("..\\data", "article_hrefs", output_file_name)
    searches_pickle.pop(0)
    for name, article_list in articles.items():
        if len(article_list) == 0:
            continue
        else:
            with open(os.path.join(ARTICLE_DIR, f"{name}.json"), "w+") as file:
                file.write("\n")
                json.dump(article_list, file)
                file.write("\n")
    df.to_csv(CSV_OUTPATH, mode="a", header=not os.path.exists(CSV_OUTPATH))
    with open(PICKLE_OUTPATH, "wb") as file:
        pickle.dump(searches_pickle, file)


def gen_searches(input_company_file, PICKLE_OUTPATH):

    """Generates searches from either a pickle if it exists or the input csv files."""

    delete_old_pickle(input_company_file)

    try:
        with open(PICKLE_OUTPATH, "rb") as file:
            searches = pickle.load(file)
            if not searches:
                return "You have completed this assignment. Please change the input file before running the program."
    except FileNotFoundError:
        co_df = read_input_file(input_company_file)
        companies = [
            str(code).lower()
            for code in co_df[~co_df["factiva_company_code"].isnull()][
                "factiva_company_code"
            ].values
        ]
        df = pd.read_csv(SOURCE_PATH)
        codes = df["Newspaper_code"].values
        commands = df["search command"].values
        searches = [
            f"{command}{company},{codes[i]},{company}"
            for company in companies
            for i, command in enumerate(commands)
        ]
    return searches


def all_none_dataframe(co_code, pub_code):

    """Creates dataframe with no frequencies for the year range 1995-2020."""

    for year in range(1995, 2021):
        if year == 1995:
            info_dict = {
                "year": [1995, 1995, 1995, 1995],
                "quarter": [1, 2, 3, 4],
            }

        elif year < 2020:
            info_dict["year"] += [year, year, year, year]
            info_dict["quarter"] += [1, 2, 3, 4]

        elif year == 2020:
            info_dict["year"] += [2020, 2020]
            info_dict["quarter"] += [1, 2]
    df = pd.DataFrame.from_dict(info_dict)
    df["count"] = 0
    df["company_code"] = co_code
    df["pub_code"] = pub_code

    return df


def year_none_dataframe(co_code, pub_code, year):

    """Creates a dataframe with no frequencies for a single year."""

    if year < 2020:
        info_dict = {
            "year": [year, year, year, year],
            "quarter": [1, 2, 3, 4],
        }

    else:
        info_dict = {
            "year": [year, year],
            "quarter": [1, 2],
        }
    df = pd.DataFrame.from_dict(info_dict)
    df["count"] = 0
    df["company_code"] = co_code
    df["pub_code"] = pub_code

    return df


def get_year_info(driver, wait, eid_username, eid_password):

    """Gets information from every page in a given search year including duplicates, article json, and article frequencies."""

    duplicates = 0
    counter = {"1": 0, "2": 0, "3": 0, "4": 0}
    total = 0
    article_links = []

    while driver:

        next_button = find_next_button(driver.page_source)
        if next_button != None:
            counter, total, article_links = get_page_info(
                driver.page_source, counter, total, article_links
            )
            duplicates += get_duplicates(driver.page_source)
            next_page(driver, wait)

        elif next_button == None:
            counter, total, article_links = get_page_info(
                driver.page_source, counter, total, article_links
            )
            duplicates += get_duplicates(driver.page_source)
            counter_total = sum(list(counter.values()))

            if (total - duplicates) != counter_total:
                return "Did not count duplicates properly; increase sleep time if necessary"
            else:
                open_page(driver, wait, eid_username, eid_password)
                return counter, article_links


def get_all_frequencies(
    eid_username, eid_password, last_name, input_company_file,
):
    """This is the main function that iterates through every search and scrapes all information from Factiva, while saving progess after each search"""

    output_file_name = gen_output_name(input_company_file, last_name)
    PICKLE_OUTPATH = os.path.join("pickles", f"{input_company_file}_searches.pickle")
    searches = gen_searches(input_company_file, PICKLE_OUTPATH)
    searches_pickle = searches.copy()
    driver, wait = set_driver()
    open_page(driver, wait, eid_username, eid_password)

    print(
        f"\nStarting at: {datetime.now()}\nFirst search term is {searches[0]}\nLength of the current list is {len(searches)}\n"
    )

    for i, text in enumerate(searches):

        search, pub_code, co_code = text.split(",")
        articles = {
            f'{co_code}_{"".join(pub_code)}_{year}': [] for year in range(1995, 2021)
        }
        date_dict = {
            "frm": "01",
            "frd": "01",
            "fry": 1995,
            "tom": "06",
            "tod": "30",
            "toy": 2020,
        }
        enter_search(driver, wait, date_dict, search, eid_username, eid_password)
        results = check_frequency_chart(driver.page_source)

        if results == None:
            df = all_none_dataframe(co_code, pub_code)
            try:
                save_progress(searches_pickle, articles,df, output_file_name, PICKLE_OUTPATH)
            except:
                print("Error when saving")
                return None

        else:

            df = pd.DataFrame()
            for year in range(1995, 2021):
                if year in results:
                    if year < 2020:
                        date_dict = {
                            "frm": "01",
                            "frd": "01",
                            "fry": year,
                            "tom": "12",
                            "tod": "31",
                            "toy": year,
                        }
                    else:
                        date_dict = {
                            "frm": "01",
                            "frd": "01",
                            "fry": year,
                            "tom": "06",
                            "tod": "30",
                            "toy": year,
                        }
                    enter_search(
                        driver, wait, date_dict, search, eid_username, eid_password
                    )
                    counter, article_links = get_year_info(driver, wait, eid_username, eid_password)
                    df = pd.concat(
                        [
                            df,
                            pd.DataFrame.from_dict(
                                {
                                    "year": [year, year, year, year],
                                    "quarter": list(counter.keys()),
                                    "count": list(counter.values()),
                                    "company_code": [
                                        co_code,
                                        co_code,
                                        co_code,
                                        co_code,
                                    ],
                                    "pub_code": [
                                        pub_code,
                                        pub_code,
                                        pub_code,
                                        pub_code,
                                    ],
                                }
                            ),
                        ]
                    )
                    articles[f"{co_code}_{pub_code}_{year}"].append(article_links)
                else:
                    df = pd.concat([df, year_none_dataframe(co_code, pub_code, year)])

            try:
                save_progress(searches_pickle, articles,df, output_file_name, PICKLE_OUTPATH)
            except:
                print('Error when saving')
                return None

