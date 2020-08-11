import pprint

import requests
from bs4 import BeautifulSoup


def get_html(url: str, params: dict) -> str:
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r
    except (requests.RequestException, ValueError) as e:
        print(repr(e))
        return False


def parse_habr_html(html: requests.models.Response) -> list:
    if html:
        soup = BeautifulSoup(html.text, "lxml")
        vacancies = soup.find_all(
            name="div",
            attrs={"class": "vacancy-card__info"}
        )
        vs_list = []
        for vacancy in vacancies:
            vs_list.append(
                {
                    "link": f"https://career.habr.com{vacancy.a['href']}",
                    "title": vacancy.a.text,
                    "salary": vacancy.find("div", {"class": "basic-salary"}).text,
                    "skills": [skill.text for skill in vacancy.find(
                        "div", {"class": "vacancy-card__skills"}).find_all(
                            "a", {"class": "link-comp link-comp--appearance-dark"})],
                    "meta": [skill.text for skill in vacancy.find(
                        "div", {"class": "vacancy-card__meta"}).find_all(
                            "a", {"class": "link-comp link-comp--appearance-dark"})],
                    "employment_type": [skill.text for skill in vacancy.find(
                        "div", {"class": "vacancy-card__meta"}).find_all(
                            "span", {"class": "preserve-line"})][2:]
                }
            )
        return vs_list


def parse_hh_html(html: requests.models.Response) -> list:
    if html:
        vacancies = html.json()["items"]
        pprint.pprint(html.json()["alternate_url"])
        vs_list = []
        for vacancy in vacancies:
            vs_list.append(
                {
                    "link": vacancy["alternate_url"],
                    "title": vacancy["name"],
                    "salary": vacancy["salary"]["from"] if vacancy["salary"] else None,
                    "skills": vacancy["snippet"]["requirement"] if vacancy["snippet"] else None,
                    "meta": [
                        vacancy["employer"]["name"],
                        vacancy["address"]["city"] if vacancy["address"] else vacancy["area"]["name"]
                    ],
                    "employment_type": vacancy["schedule"]["name"]
                }
            )
        return vs_list


if __name__ == "__main__":
    pass
