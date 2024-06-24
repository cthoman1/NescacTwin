import requests
from bs4 import BeautifulSoup
import re

us_state_abbreviations = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
# This is just an index of abbreviations for each US state.


def initialize_schools_by_state_table():
    url = requests.get('https://en.wikipedia.org/wiki/New_England_Small_College_Athletic_Conference')
    soup = BeautifulSoup(url.content, 'html.parser')
    table_header_span = soup.find('span', class_='mw-headline', string='Current members')
    member_table = table_header_span.find_next('table')
    schools_by_state = []
    rows = member_table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        school_full = columns[0].text.strip() if len(columns) > 1 else ''
        school = re.sub(r'\b(college|university)\b', '', school_full, flags=re.IGNORECASE).strip()
        location = columns[1].text.strip() if len(columns) > 1 else ''
        state = re.sub(r'^.*?,', '', location).strip()
        state_abbreviation = us_state_abbreviations.get(state, None)
        if school and state_abbreviation:
            schools_by_state.append((school, state_abbreviation))
    return schools_by_state
# This returns a list of NESCAC schools and the abbreviation of the state to which each belongs, from Wikipedia.


