import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


def download(pmc_id, filename, pmid):
    url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/' + str(pmc) + "/"
    ua = UserAgent()
    headers = {'User-Agent': ua.firefox}
    request = requests.get(url, headers=headers)
    bs = BeautifulSoup(request.content, 'lxml')
    download_url = bs.find_all(attrs={'class': "usa-link display-flex usa-tooltip"})
    download_link = download_url[1].get('href')
    print(download_link)
    download_url = "https://pmc.ncbi.nlm.nih.gov/articles" + "/" + pmc + "/" + download_link
    print(filename)
    print(download_url)
    r = requests.get(download_url, headers=headers)
    with open("The Path You Want to Store These/Papers/"+filename+"_"+ str(pmid) + ".pdf", 'wb') as f:
        f.write(r.content)


# Read the excel file containing the list of papers
df = pd.read_excel('The Path Where Your Paper List is Located/Demo_Paper_List.xlsx', header=None)
df.columns = ['Title', 'PMCNum', "PMID"]

# Drop rows with missing values
PMC = df.dropna(axis=0, how='any')
print(PMC)
PMCNum = PMC['PMCNum']
TitleO = list(PMC['Title'])
PMID = list(PMC['PMID'])

# Remove special characters from the title
Title = []
for i in TitleO:
    table = i.maketrans(':"/', '   ')
    Title.append(i.translate(table))

# Download the papers
failed_titles = []
for m, pmc in enumerate(PMCNum):
    file = Title[m]
    pmid = PMID[m]
    try:
        download(filename=file, pmc_id=pmc, pmid=pmid)
    except Exception as e:
        print(f"Error downloading {pmc} for title '{Title[m]}': {e}")
        failed_titles.append(Title[m])
        continue

# Print the titles that failed to download
if failed_titles:
    print("Failed to download the following titles:")
    for title in failed_titles:
        print(title)
