import pprint

import requests
from bs4 import BeautifulSoup

import config as c


def get_html(url: str, params: dict) -> str:
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.text
    except (requests.RequestException, ValueError) as e:
        print(repr(e))
        return False


def parse_habr_html(html: str) -> list:
    if html:
        soup = BeautifulSoup(html, "lxml")
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
                    "calary": vacancy.find("div", {"class": "basic-salary"}).text,
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


def parse_hh_html(html: str) -> list:
    pass


if __name__ == "__main__":
    # print(get_html(
    #     url=c.HABR_BASE,
    #     headers=c.HABR_HEADERS
    # )
    # )
    html = get_html(
        url=c.HH_BASE,
        params=c.HH_HEADERS
    )
    # parse_habr_html(html=html)
