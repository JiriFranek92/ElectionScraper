import sys
import re
from string import whitespace
import csv

from bs4 import BeautifulSoup
from requests import get


def get_soup(url):
    return BeautifulSoup(get(url).text, "html.parser")


def zadan(count):
    if count == 1:
        return f"zadán {count}"
    elif count == 3:
        return f"zadány {count}"
    else:
        return f"zadáno {count}"


def check_args():
    # zkontroluje správný počet vstupních argumentů, v případě špatného počtu
    # vrátí chybovou hlášku
    args = len(sys.argv) - 1
    if args != 2:
        msg = f"CHYBA! Program potřebuje 2 vstupní argumenty, {zadan(args)}."
    else:
        msg = None

    return msg


def check_url(url):
    # zkontroluje jestli je na vstupu zadané url platné, pokud není vrátí
    # chybovou hlášku (pokud možno řekne která část není platná).
    valid_regions = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    valid_nuts = (1100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109,
                  2110, 2111, 2112, 3101, 3102, 3103, 3104, 3105, 3106, 3107,
                  3201, 3202, 3203, 3204, 3205, 3206, 3207, 4101, 4102, 4103,
                  4201, 4202, 4203, 4204, 4205, 4206, 4207, 5101, 5102, 5103,
                  5104, 5201, 5202, 5203, 5204, 5205, 5301, 5302, 5303, 5304,
                  6101, 6102, 6103, 6104, 6105, 6201, 6202, 6203, 6204, 6205,
                  6206, 6207, 7101, 7102, 7103, 7104, 7105, 7201, 7202, 7203,
                  7204, 8101, 8102, 8103, 8104, 8105, 8106)

    match = re.match(
        r"https://volby.cz/pls/ps2017nss/ps32\?xjazyk=CZ&xkraj=(\d*)&xnumnuts=(\d*)$",
        url)
    if not match:
        return f"CHYBA! '{url}' není platné url."
    elif not int(match[1]) in valid_regions:
        return f"CHYBA! '{match[1]}' není platný kód kraje."
    elif not int(match[2]) in valid_nuts:
        return f"CHYBA! '{match[2]}' není platný kód NUTS."
    else:
        return None


def get_links(soup, url):
    # získá odkazy na jednotlivé obce
    i = 1
    link_list = []
    while True:
        table_links = [url + cell["href"] for cell in
                       soup.select(f'td[headers="t{i}sa1 t{i}sb1"] > a')]
        if not table_links:
            break
        else:
            link_list += table_links
            i += 1
    return link_list


def muni_code(url):
    # vrátí kód obce
    match = re.search(r"xobec=(\d*)", url)
    if match:
        return match[1]
    else:
        return ""


def scrape_name(soup, pattern):
    # najde reg. výraz v nadpisech h3 na stránce
    for header in soup.find_all("h3"):
        mat = re.match(pattern, header.text.strip(whitespace))
        if mat:
            return mat[1]
    else:
        return ""


def muni_name(soup):
    return scrape_name(soup, "Obec: (.*)")


def county_name(soup):
    return scrape_name(soup, "Okres: (.*)")


def vote_data(soup):
    # vrátí počet voličů, vydaných obálek a platných hlasů
    data = []
    for header in ["sa2", "sa3", "sa6"]:
        txt = soup.select_one(f'td[headers={header}]').text
        txt = txt.replace(u"\xa0", "")
        data.append(txt)
    return data


def party_data(soup):
    # vrátí počet hlasů pro jednotlivé strany
    data = []
    for i in [1, 2]:
        data += [cell.text.replace(u"\xa0", "")
                 for cell in soup.select(f'td[headers="t{i}sa2 t{i}sb3"]')
                 if cell.text != "-"]
    return data


def scrape_data(url):
    # stáhne volební výsledky obce a vrátí je jako list pro zápis do csv
    line = [muni_code(url)]

    soup = get_soup(url)
    line.append(muni_name(soup))
    line += vote_data(soup)
    line += party_data(soup)
    return line


def obce(count):
    if count < 5:
        return f"{count} obce"
    else:
        return f"{count} obcí"


def progress_bar(i, total, length=50):
    # vypíše postup pro i-tou položku z total
    filled_length = total if total < length else int(length * i / total)
    bar = filled_length * "#" + (length - filled_length) * "-"
    print(f"\r|{bar}| {i} z {total}", end="\r")
    if i == total:
        print()


headers = ['Kód obce', 'Název obce', 'Voliči', 'Vydané obálky', 'Platné hlasy',
           'Občanská demokratická strana', 'Řád národa - Vlastenecká unie',
           'CESTA ODPOVĚDNÉ SPOLEČNOSTI', 'Česká str.sociálně demokrat.',
           'Radostné Česko', 'STAROSTOVÉ A NEZÁVISLÍ',
           'Komunistická str.Čech a Moravy',
           'Strana zelených', 'ROZUMNÍ-stop migraci diktát.EU',
           'Strana svobodných občanů',
           'Blok proti islam.-Obran.domova',
           'Občanská demokratická aliance',
           'Česká pirátská strana', 'Unie H.A.V.E.L.',
           'Referendum o Evropské unii',
           'TOP 09', 'ANO 2011', 'Dobrá volba 2016',
           'SPR-Republ.str.Čsl. M.Sládka',
           'Křesť.demokr.unie-Čs.str.lid.',
           'Česká strana národně sociální',
           'REALISTÉ', 'SPORTOVCI', 'Dělnic.str.sociální spravedl.',
           'Svob.a př.dem.-T.Okamura (SPD)', 'Strana Práv Občanů']

base_url = "https://volby.cz/pls/ps2017nss/"


# noinspection PyUnboundLocalVariable
def main():
    # zkontroluj vstupní argumenty
    err_msg = check_args()
    if err_msg:
        exit(err_msg)
    else:
        url_for_scraping = sys.argv[1]
        filename = sys.argv[2]

    # zkontroluj url
    err_msg = check_url(url_for_scraping)
    if err_msg:
        exit(err_msg)
    else:
        soup = get_soup(url_for_scraping)
        print(f"Stahuji volební výsledky pro okres: {county_name(soup)}")

    # získej odkazy na obce
    links = get_links(soup, base_url)
    if len(links) == 0:
        exit("Chyba! Nenalezen žádný odkaz na obci.")
    else:
        print(f"Nalezeno: {obce(len(links))}.")

    # otevři csv soubor pro zápis, zapiš hlavičku,
    # stáhni data pro jednotlivé obce a vypiš do souboru
    print(f"Stahuji data do souboru '{filename}'.")
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for i, link in enumerate(links):
            writer.writerow(scrape_data(link))
            progress_bar(i + 1, len(links))

    print("Stahování úspěšně dokončeno.")


if __name__ == "__main__":
    main()
