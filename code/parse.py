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

    if len(set(headline.text.split(".")[0] for headline in headlines)) == 1:

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

        if headline.text.split(".")[0] == headlines[i - 1].text.split(".")[0]:

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


def get_years(soup):

    years = []
    text = soup.find('div', {'class': 'cd_div_expand'}).find('script', {'type': 'text/javascript'}).text.split('"categories":')[1].split(',"seriesData":')[0]
    for year in range(1995,2021):
        if str(year) in text:
            years.append(year)
    return years


def check_frequency_chart(soup):

    if soup.find('tr', {'class': 'headline'}) == None:

        return None

    else:

        return get_years(soup)
    
def get_article_info(page_source, dict_,):
    
    soup = BeautifulSoup(page_source, 'html.parser')
    for tr in soup.find('div', {'class': 'article'}).tbody:
        try:
            tds = tr.find_all('td')
            index = tds[0].text.strip()
            text = tds[1].text.strip()
        except AttributeError:
            pass
        dict_[index] = text
    return dict_