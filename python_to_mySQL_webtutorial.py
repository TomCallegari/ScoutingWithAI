from requests import get
import mysql.connector
from bs4 import BeautifulSoup

# Database credentials
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='TCisc00l#',
    database='tommy'
    )
cursor = cnx.cursor()

# Url
url = 'https://howpcrules.com/sample-page-for-web-scraping/'

# Html data
response = get(url)

# Convert html data into a bs4 object
soup = BeautifulSoup(response.text, 'html.parser')

name_of_class = soup.h3.text.strip()
print(name_of_class)

# Get all data associated with name_of_class
basic_data_table = soup.find('table', {'summary': 'Basic data for the event'})

# Get all cells in the basic_data_table
basic_data_cells = basic_data_table.find_all('td')

# Print each element of basic_data_cells
for i in basic_data_cells:
    print(i)

# Get each element of basic_data_cells
type_of_course = basic_data_cells[0].text.strip()
lecturer = basic_data_cells[1].text.strip()
number = basic_data_cells[2].text.strip()
short_text = basic_data_cells[3].text.strip()
choice_term = basic_data_cells[4].text.strip()
hours_per_week = basic_data_cells[5].text.strip()
expected_num_of_participants = basic_data_cells[6].text.strip()
maximum_participants = basic_data_cells[7].text.strip()
assignment = basic_data_cells[8].text.strip()
lecture_id = basic_data_cells[9].text.strip()
credit_points = basic_data_cells[10].text.strip()
hyperlink = basic_data_cells[11].text.strip()
language = basic_data_cells[12].text.strip()

# Insert statement for database
sql = 'INSERT INTO classes(name_of_class, type_of_course, lecturer, number, short_text, choice_term, hours_per_week, expected_num_of_participants, assignment, lecture_id, credit_points, hyperlink, language)'

cursor.execute(sql)
cnx.commit()

print(' - '*20)

# Get the group dates tables 
dates_tables = soup.find_all('table', {'summary': 'Overview of all event dates'})

# Print each date table in dates_tables
for i in dates_tables:
    print(i)

# Iterate through each table
for table in data_tables:
    # Iterate through each row
    for row in table.select('tr'):
        # Get each cell inside the rows
        cells = row.find_all('td')
        # Check if there is at least one td tag in the row
        if (len(cells) > 0):
            # Duration cell
            duration = cells[0].text.split('to')
            start_date = duration[0].strip()
            end_date = duration[1].strip()
            # Day
            day = cells[1].text.strip()
            # Time
            time = cells[2].text.split('to')
            start_time = time[0].strip()
            end_time = time[1].strip()
            # Frequency
            frequency = cells[3].text.strip()
            # Room
            room = cells[4].text.strip()
            # Lecturer_for_date
            lecturer_for_date = cells[5].text.strip()
            # Status
            status = cells[6].text.strip()
            # Remarks
            remarks = cells[7].text.strip()
            # Cancelled
            cancelled = cells[8].text.strip()
            # Max participants
            max_participants = cells[9].text.strip()
            sql = 'INSERT INTO events(class_id, start_date, end_date, day, start_time, end_time, frequency, room, lecturer_for_date, status, remarks, cancelled, max_participants)'

