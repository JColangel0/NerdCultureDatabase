from tkinter import *
from bs4 import BeautifulSoup
import requests

def web_scrape(searchData, space_key, link, class_name, list):
    if " " in searchData:
        searchData = searchData.replace(" ", space_key)
    response = requests.get(link+searchData.lower())
    soup = BeautifulSoup(response.content, "html.parser")
    page = soup.find("div", {"class": class_name}) if not list else soup.find_all(
        "div", {"class": class_name})
    return page


def search(searchData):
    try:
        page = web_scrape(
            searchData, "-", "https://www.dccomics.com/characters/", "field-item even", True)
        for i in page:
            if i.get("property") == "schema:about content:encoded":
                textSection = i.find_all("p")
        returnValue = ""
        for i in textSection:
            returnValue += i.text + "\n"
        return returnValue
    except:
        try:
            page = web_scrape(
                searchData, "+", "https://www.fandom.com/?s=", "post grid-block small-12 mediawiki-article", False)
            results = page.find_all("a")
            finalResponse = requests.get(results[0]["href"])
            finalSoup = BeautifulSoup(finalResponse.content, "html.parser")
            information = finalSoup.find("div", {"class": "mw-parser-output"})
            textSection = information.find_all("p", recursive=False)
            return textSection[1].text
        except:
            return "No Data Found"

def main():
    root = Tk()
    root.title("Database")
    root.geometry("+300+300")

    v = StringVar()
    searchBar = Entry(root, bd=5, font=(
        "Arial 60"), textvariable=v).pack(padx=20, pady=20)

    information = Text(root, bd=5, wrap=WORD)


    def EnterController(e):
        results = search(v.get())
        results += "\n\n"
        global information
        information.insert(INSERT, results)
        information.pack(padx=20, pady=20)
        v.set("")


    root.bind('<Return>', EnterController)

    root.mainloop()

if __name__ == "__main__":
    main()
