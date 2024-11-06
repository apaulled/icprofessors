import bs4
import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return str(e)


html_content = get_html('https://www.ithaca.edu/academics/school-humanities-and-sciences/faculty-staff-directory#a38528')

soup = BeautifulSoup(html_content, 'lxml')

a_tags = soup.find_all('a', href=True)
a_tags = [tag for tag in a_tags if 'https://staff.ithaca.edu/aodowd/' in str(tag) or 'https://www.ithaca.edu/staff' in str(tag) or 'https://faculty.ithaca.edu' in str(tag)]
links = [tag['href'] for tag in a_tags]

facs = []
tracker = []
for link in links:
    fac = {}
    faculty_html = get_html(link)
    faculty_soup = BeautifulSoup(faculty_html, 'lxml')
    profile_intros = faculty_soup.find_all('div', class_='profile-intro')
    if len(profile_intros) == 0:
        continue  # Could not get any information

    profile_intro = profile_intros[0]

    # Get Name
    headings = profile_intro.find_all('h2', class_='person-intro__heading')
    if len(headings) == 0:
        continue  # Could not find a name
    name = headings[0].get_text().strip()
    if name in tracker:
        continue
    fac['name'] = name
    print('Found Name:', name)
    tracker.append(name)

    # Get Department
    subheadings = profile_intro.find_all('div', class_='person-intro__subheading')
    if len(subheadings) != 0:
        subheading = subheadings[0].get_text()
        subheading_parts = subheading.split(',')
        if len(subheading_parts) < 2:
            print('BAD SUBHEADING')
        else:
            fac['role'] = subheading_parts[0].strip()
            fac['department'] = subheading_parts[-1].strip()

    # Get Image
    images = profile_intro.find_all('img')
    if len(images) > 0:
        if images[0]['src'] is not None:
            fac['image_url'] = 'https://www.ithaca.edu' + images[0]['src']

    # Get General Information
    content = profile_intro.find_all('div', class_='profile-intro__content')
    if len(content) > 0:
        divs = content[0].find_all('div')
        for div in divs:
            strongs = div.find_all('strong')
            if len(strongs) > 0 and ':' in strongs[0].get_text():
                key = strongs[0].get_text().replace(':', '').strip()
                value = None

                # Check for a link
                links = strongs[0].find_all('a')
                if len(links) > 0:
                    value = links[0].get_text().strip()
                else:  # Content is not a link, can safely get the text
                    value = div.get_text().split(':')[-1].strip()

                    # Check for a list
                    value_parts = value.split(',')
                    # Office locations are comma-separated, but should not be treated as lists
                    if len(value_parts) > 1 and 'Office' not in key:
                        value = [part.strip() for part in value_parts]

                fac[key.lower()] = value

    # Get Paragraph Information from Under the Contact Details

    paragraph_texts = faculty_soup.find_all('div', class_='paragraph__text')
    if len(paragraph_texts) > 0:
        body_texts = paragraph_texts[0].find_all('div', class_='body-text')
        if len(body_texts) > 0:
            inner_div = body_texts[0].find('div')
            if inner_div is not None:
                bio = {}
                key = 'generic'  # Default key if there is no clear header
                value = []
                children = inner_div.children
                for child in children:
                    if isinstance(child, bs4.element.Tag):
                        text = child.get_text()

                        if child.name == 'p':
                            # A trailing colon is assumed to be an indicator of a section heading
                            if len(text.strip()) > 0 and text.strip()[-1] == ':':
                                if len(value) > 0:
                                    bio[key.lower().replace(' ', '_').replace(':', '')] = value
                                value = []
                                key = text.strip().lower()
                                continue

                            # Newlines are assumed to be separators
                            text_parts = text.split('\n')
                            if len(text_parts) > 1:
                                value.extend([part.strip() for part in text_parts])
                            else:
                                value_text = text.strip()
                                if value_text != '':
                                    value.append(value_text)

                        elif child.name == 'ol' or child.name == 'ul':
                            list_children = child.children
                            for list_child in list_children:
                                child_text = list_child.get_text().strip()
                                if child_text != '':
                                    value.append(child_text)

                bio[key.lower().replace(' ', '_').replace(':', '')] = value
                if len(bio) > 0:
                    fac['bio'] = bio

    facs.append(fac)
    # You should just be able to run some kind of insert method here to put the
    # fac object right into the database.


with open('faculty.json', 'w') as f:
    f.write(json.dumps(facs, indent=4))
