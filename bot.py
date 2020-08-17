import telebot

import config as c
import parser

bot = telebot.TeleBot(token=c.BOT_TOKEN)


def generate_message(source: str) -> str:
    if source == "habr":
        html = parser.get_html(
            url=c.HABR_BASE,
            params=c.HABR_PARAMS
        )
        vacancies = parser.parse_habr_html(html=html)
    elif source == "hh":
        html = parser.get_html(
            url=c.HH_BASE,
            params=c.HH_PARAMS
        )
        vacancies = parser.parse_hh_html(html=html)

    text = ""
    for vacancy in vacancies:
        # тип требуемых навыков может быть str или None
        try:
            skills = ', '.join(vacancy['skills']) if isinstance(
                vacancy['skills'], list) else vacancy['skills'].replace(
                    '<highlighttext>', '').replace('</highlighttext>', '')
        except AttributeError:
            skills = "Требуемые навыки не указаны"

        employment_type = ', '.join(vacancy['employment_type']) if isinstance(
            vacancy['employment_type'], list) else vacancy['employment_type']

        salary = vacancy['salary'] if vacancy['salary'] else "не указана"

        text += f"[{vacancy['title']}]({vacancy['link']})\nЗП: {salary}\n\
{skills}\n{', '.join(vacancy['meta'])}\n{employment_type}\n\n"

    return text


def send_jobs():
    resources = ["hh", "habr"]
    for source in resources:
        text = generate_message(source=source)
        text = text if text else "Вакансий нет."
        bot.send_message(
            chat_id=c.CHANNEL_ID,
            text=f"*Источник вакансий: {source}*\n\n{text}",
            parse_mode="markdown",
            disable_web_page_preview=True
        )


if __name__ == "__main__":
    send_jobs()
