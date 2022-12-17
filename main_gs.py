# %% Libraries
from flask import Flask, render_template, request
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup

# %%
main_gs = Flask(__name__)


# Route to display the home page
@main_gs.route('/',
            methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")


# route to show the review comments in a web UI
@main_gs.route('/review',
            methods=['POST',
                     'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            SEARCH_STRING = request.form['content'].replace(" ", "")

            SITE = r'https://scholar.google.com/scholar'
            HEADERS = { 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
            PARAMS = {'q': SEARCH_STRING,  # search query
                      'hl': 'en'  # language of the search
                      }

            PAGE_HTML = requests.get(SITE, headers=HEADERS, params=PARAMS).text
            PAGE_SOUP = BeautifulSoup(PAGE_HTML, 'lxml')
            ARTICLES = PAGE_SOUP.select('.gs_r.gs_or.gs_scl')

            ARTICLES_DATA = []
            for ARTICLE in ARTICLES:

                try:
                    TITLE = ARTICLE.select_one('.gs_rt').text
                except:
                    TITLE = 'NA'

                try:
                    PUBLICATION_INFO = ARTICLE.select_one('.gs_a').text
                except:
                    PUBLICATION_INFO = 'NA'

                try:
                    AUTHOR = PUBLICATION_INFO.split('-')[0].split('\xa0')[0]
                except:
                    AUTHOR = 'NA'

                try:
                    JOURNAL = PUBLICATION_INFO.split('-')[1].split('\xa0')[0]
                except:
                    JOURNAL = 'NA'

                try:
                    PUBLICATION_YEAR = PUBLICATION_INFO.split('-')[1].split()[-1]
                except:
                    PUBLICATION_YEAR = 'NA'

                try:
                    HOST = PUBLICATION_INFO.split('-')[-1]
                except:
                    HOST = 'NA'

                try:
                    HOST_URL = ARTICLE.select_one('.gs_rt a')['href']
                except:
                    HOST_URL = 'NA'

                try:
                    ABSTRACT = ARTICLE.select_one('.gs_rs').text
                except:
                    ABSTRACT = 'NA'

                try:
                    CITE_INFO = ARTICLE.select_one('a:contains("Cited by")').text if ARTICLE.select_one('a:contains("Cited by")') is not None else 'No citation count'
                except:
                    CITE_INFO = 'NA'

                try:
                    CITATIONS = CITE_INFO.split(sep=" ")[-1]
                except:
                    CITATIONS = 'NA'

                try:
                    PDF_LINK = ARTICLE.select_one('.gs_or_ggsm a:nth-child(1)')['href']
                except:
                    PDF_LINK = 'NA'

                ARTICLE_DATA = {'TITLE': TITLE,
                                'AUTHOR': AUTHOR,
                                'PUBLICATION_YEAR': PUBLICATION_YEAR,
                                'JOURNAL': JOURNAL,
                                'HOST': HOST,
                                'HOST_URL': HOST_URL,
                                'ABSTRACT': ABSTRACT,
                                'CITATIONS': CITATIONS,
                                "PDF_LINK": PDF_LINK,
                                }

                ARTICLES_DATA.append(ARTICLE_DATA)

            """
            filename = SEARCH_STRING + ".csv"
            fw = open(filename, "w")
            SCHEMA = "TITLE, AUTHOR, PUBLICATION_YEAR, JOURNAL, HOST, HOST_URL, ABSTRACT, CITATIONS, PDF_LINK \n"
            fw.write(SCHEMA)
            """

            return render_template('results.html', ARTICLES_DATA=ARTICLES_DATA)

        except Exception as e:
            print('The Exception message is: ', e)
            return 'Oops Something went wrong :('

    else:
        return render_template('index.html')

if __name__ == "__main__":
    main_gs.run(host='127.0.0.1', port=5001, debug=False)
