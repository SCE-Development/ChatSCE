from bs4 import BeautifulSoup
import re
import requests
import json
import unicodedata
from urllib.parse import urlparse, parse_qs

# All URLs go here
# Make sure to use the SJSU course catalog otherwise the scraper won't work
# Currently contains the catalog for CMPE, CS, SE, EE, MATH, ISE, and ENGR
# url_list = [
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=CMPE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?catoid=14&navoid=5106&filter%5B27%5D=CMPE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=2&filter%5Bexact_match%5D=1&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=SE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=CS&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=EE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?catoid=14&navoid=5106&filter%5B27%5D=EE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=2&filter%5Bexact_match%5D=1&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=MATH&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?catoid=14&navoid=5106&filter%5B27%5D=MATH&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=2&filter%5Bexact_match%5D=1&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=ISE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
#     "https://catalog.sjsu.edu/content.php?filter%5B27%5D=ENGR&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
# ]

# Additional courses like BIO, CHEM, PHYS, BME, DATA, STAT, TECH can be added here
# Can also be combined with the previous list but it will result in a significantly longer runtime due to how many courses there are
# So it's better to rename the output json file and run the scraper again with a different list if you have more departments to add
url_list = [
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=BIOL&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?catoid=14&navoid=5106&filter%5B27%5D=BIOL&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=2&filter%5Bexact_match%5D=1&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=CHEM&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=PHYS&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=BME&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=DATA&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=STAT&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
    "https://catalog.sjsu.edu/content.php?filter%5B27%5D=TECH&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter",
]

# TODO Implement topology sort to determine prerequisites and corequisites
# TODO Implement a way to convert JSON to ClassNode objects
class ClassNode:
    def __init__(
        self, course_name, units, description, prereqs, coreqs, grading_type, note
    ):
        self.title = course_name
        self.units = units
        self.description = description
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.grading_type = grading_type
        self.note = note

    def to_string(self):
        return f"Title: {self.title}\nDescription: {self.description}\nUnits: {self.units}\nPrerequisites: {self.prereqs}\nCorequisites: {self.coreqs}\nGrading Type: {self.grading_type}\nNote: {self.note}\n"

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nUnits: {self.units}\nPrerequisites: {self.prereqs}\nCorequisites: {self.coreqs}\nGrading Type: {self.grading_type}\nNote: {self.note}\n"


class Scraper:
    def __init__(self, urls=[]):
        self.url_list = urls
        self.html_list = []
        self.filtered_hrefs = []
        self.class_pages = []
        self.td_tags = []

    def scrape(self) -> list[BeautifulSoup]:
        print("Scraping...")
        self.html_list = []
        for url in self.url_list:
            response = requests.get(url)
            if response.status_code == 200:
                doc = BeautifulSoup(response.text, "html.parser")
                self.html_list.append(doc)
            else:
                raise Exception("Request failed for", url)
        return self.html_list

    def filter_hrefs(self) -> list[str]:
        print("Filtering hrefs...")
        self.filtered_hrefs = []
        target_departments = set()
        
        for url in self.url_list:
            parsed_url = urlparse(url)
            captured = parse_qs(parsed_url.query)['filter[27]'][0]
            target_departments.add(captured)
            
        for doc in self.html_list:
            links = doc.find_all("a")
            for link in links:
                title = link.get("title")
                if title and any(
                    department in title for department in target_departments
                ):
                    href = link.get("href")
                    self.filtered_hrefs.append(href)
                    
        return self.filtered_hrefs

    def get_class_pages(self) -> list[str]:
        print("Getting class pages...")
        self.class_pages = []
        for href in self.filtered_hrefs:
            self.class_pages.append("https://catalog.sjsu.edu/" + href)            
        return self.class_pages

    def grab_td_tags(self) -> list[BeautifulSoup]:
        print("Grabbing tags...")
        self.td_tags = []
        for idx, class_page in enumerate(self.class_pages):
            print(f"Processing {idx} / {len(self.class_pages)}...")
            response = requests.get(class_page)
            if response.status_code == 200:
                doc = BeautifulSoup(response.text, "html.parser")
                self.td_tags.extend(
                    doc.find_all("td", class_="block_content", colspan="2")
                )
            else:
                print("Error: Request failed for", class_page)
                raise Exception("Request failed for", class_page)
        return self.td_tags

    def extract(self, pattern: str, text: str, error: str, dotall=False):
        if dotall:
            match = re.search(pattern, text, re.DOTALL)
        else:
            match = re.search(pattern, text)

        if match:
            result = match.group(1).strip()
        else:
            result = error

        return self.normalize(result)

    def normalize(self, text: str):
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8")
            .strip()
            .replace("  ", " ")
        )

    # If someone finds another way than regex please implement it
    def extract_course_info(self) -> list[ClassNode]:
        print("Extracting course info...")
        nodes = []
        for idx, tag in enumerate(self.td_tags):
            print(f"Processing {idx} / {len(self.td_tags)}...")
            # Get course html block
            title = tag.find("p")
            if title:
                title = title.text.strip()
            else:
                title = "Title not found"

            # Find course name
            course_name = tag.find("h1", id="course_preview_title")
            if course_name:
                course_name = course_name.text.strip()
            else:
                course_name = "Course name not found"

            course_name = self.normalize(course_name)

            # Find units
            units = self.extract(r"(\d+(-\d+)? unit\(s\))", title, "Units not found")

            # Find course description
            course_description = self.extract(
                r"(?<=unit\(s\)\s)(.*?)(?=Prerequisite\(s\):|Corequisite\(s\):|Grading:)",
                title,
                "Description not found",
                dotall=True,
            )

            prereqs = self.extract(
                r"(?<=Prerequisite\(s\): )(.*?)(?=Corequisite\(s\):|Grading:)",
                title,
                "No prerequisites",
                dotall=True,
            )

            coreqs = self.extract(
                r"(?<=Corequisite\(s\): )(.*?)(?=Grading:)",
                title,
                "No corequisites",
                dotall=True,
            )

            # Find grading type
            grading_type = self.extract(
                r"Grading:\s(.*?)(?=Note\(s\)|Class Schedule)",
                title,
                "Grading type not found",
            )

            # Check if Note(s) or anything after "Note(s):" but before "Class Schedule" exist
            note = self.extract(
                r"(?<=Note\(s\): )(.*?)(?=Class Schedule)", title, "No additional notes"
            )

            nodes.append(
                ClassNode(
                    course_name=course_name,
                    units=units,
                    description=course_description,
                    prereqs=prereqs,
                    coreqs=coreqs,
                    grading_type=grading_type,
                    note=note,
                )
            )

        return nodes


scraper = Scraper(url_list)
scraper.scrape()
scraper.filter_hrefs()
scraper.get_class_pages()
scraper.grab_td_tags()
nodes = scraper.extract_course_info()
for node in nodes:
    print(node.to_string())

with open("output.json", "w") as f:
    json.dump([node.__dict__ for node in nodes], f, indent=4)
