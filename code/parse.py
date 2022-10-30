from bs4 import BeautifulSoup
import regex as re


def get_page_info(soup, counter, total, article_links):

    map_dict = {
        "January": "1",
        "February": "1",
        "March": "1",
        "April": "2",
        "May": "2",
        "June": "2",
        "July": "3",
        "August": "3",
        "September": "3",
        "October": "4",
        "November": "4",
        "December": "4",
    }
    headlines = soup.find_all("tr", {"class": "headline"})
    total += len(headlines)

    if total == 1:
        headline = headlines[0]
        article_links.append(headline.find("a").get("href"))
        sub_list = sum(
            [
                subtitle.split(" ")
                for subtitle in headline.find("div").text.split(",")
                if len(re.findall("[0-9]+", subtitle)) > 0
            ],
            [],
        )
        month = "".join(set(sub_list) & set(map_dict.keys()))
        counter[map_dict[month]] += 1

        return counter, total, article_links

    for i, headline in enumerate(headlines):

        if (headline.text.split(".")[0] == headlines[i - 1].text.split(".")[0]) and (
            total == 2
        ):

            headline = headlines[0]
            article_links.append(headline.find("a").get("href"))
            sub_list = sum(
                [
                    subtitle.split(" ")
                    for subtitle in headline.find("div").text.split(",")
                    if len(re.findall("[0-9]+", subtitle)) > 0
                ],
                [],
            )
            month = "".join(set(sub_list) & set(map_dict.keys()))
            counter[map_dict[month]] += 1

            return counter, total, article_links

        elif headline.text.split(".")[0] == headlines[i - 1].text.split(".")[0]:

            continue

        else:

            article_links.append(headline.find("a").get("href"))
            sub_list = sum(
                [
                    subtitle.split(" ")
                    for subtitle in headline.find("div").text.split(",")
                    if len(re.findall("[0-9]+", subtitle)) > 0
                ],
                [],
            )
            month = "".join(set(sub_list) & set(map_dict.keys()))
            counter[map_dict[month]] += 1

    return counter, total, article_links


def get_duplicates(soup):

    return int(soup.find("span", {"id": "dedupSummary"}).text.split(":")[1].strip())
