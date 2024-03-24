from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time


class ProjectNode:
    # TODO: Figure out how to add languages/apis used from the images
    def __init__(self, project_name, project_type, project_desc, github_link):
        self.title = project_name
        self.project_type = project_type
        self.description = project_desc
        self.link = github_link

    def to_string(self):
        return f"Title: {self.title}\nType: {self.project_type}\nDescription: {self.description}\nGitHub Link: {self.link}"

    def __str__(self):
        return json.dumps(self.__dict__)


class Scraper:
    def __init__(self):
        self.project_titles = []
        self.project_types = []
        self.project_descs = []
        self.links = []

    def scrape_projects(self):
        # "Some elements are dynamically generated by scripts and won't appear on your bs4. You'll need to use a
        # different package like requests-html or selenium that can render these elements before parsing them."
        # https://stackoverflow.com/questions/59090591/beautifulsoup-how-to-show-the-inside-of-a-div-that-wont-show
        print("Scraping...")
        browser = webdriver.Firefox()
        url = 'https://sce.sjsu.edu/projects#'
        browser.get(url)
        time.sleep(20)
        html = browser.page_source

        self.doc = BeautifulSoup(html, "html.parser")

    def extract_project_info(self) -> list[ProjectNode]:
        print("Extracting project info...")

        html_project_titles = self.doc.find_all('h2',
                                                class_='mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white')
        for titles in html_project_titles:
            t = titles.find('a')
            self.project_titles.append(t.get_text())

        html_project_types = self.doc.find_all('span',
                                               class_='bg-primary-100 text-primary-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded dark:bg-primary-200 dark:text-primary-800')
        for project_type in html_project_types:
            self.project_types.append(project_type.get_text())

        html_project_descs = self.doc.find_all('p', class_='mb-5 font-light text-gray-500 dark:text-gray-400')
        for project_desc in html_project_descs:
            self.project_descs.append(project_desc.get_text())

        html_links = self.doc.find_all('a',
                                       class_='inline-flex items-center font-medium text-primary-600 dark:text-primary-500 hover:underline')
        for link in html_links:
            self.links.append(link.get('href'))

        nodes = []
        for title, proj_type, desc, link in zip(self.project_titles, self.project_types, self.project_descs, self.links):
            nodes.append(
                ProjectNode(
                    project_name=title,
                    project_type=proj_type,
                    project_desc=desc,
                    github_link=link,
                )
            )

        return nodes


scraper = Scraper()
scraper.scrape_projects()
nodes = scraper.extract_project_info()
for node in nodes:
    print(node.to_string())
with open("proj_output.json", "w") as f:
    json.dump([node.__dict__ for node in nodes], f, indent=4)