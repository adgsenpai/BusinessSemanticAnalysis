from flask import Flask,render_template,send_from_directory,request
import search.searchengine as se
import engine.analysis as analysis
import pandas as pd

app = Flask(__name__,template_folder='./pages')


# allows for files to be refreshed in server
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/api/search',methods=['POST'])
def search():
    if request.method == 'POST':
        # get data from request as json
        data = request.get_json()
        # get the query from the json
        query = data['query']
        # call the search function
        results = se.search(query)
        # return name and slug
        try:
            return {'names': [result['name'] for result in results],'slugs': [result['slug'] for result in results]}
        except:
            return {'names': [],'slugs': []}

@app.route('/search/<queryterm>')
def searchterm(queryterm):
    results = se.search(queryterm)
    try:
        query = {'results': {'names':[result['name'] for result in results],'slugs': [result['slug'] for result in results]}}
    except:
        query =  {'results': []}
    return render_template('searchoptions.html',query=query)
 
@app.route('/viewsemanticanalysis/<encodedname>/<slug>')
def viewsemanticanalysis(encodedname,slug):
    try:
        df = analysis.GetReviews(slug,5)
        newdf , score, avg_review_rating = analysis.Analyze(df)     
        avg_review_rating = round(avg_review_rating,2)  
        # from the newdf only get the columns we need
        newdf = newdf[['review_title','review_content','review_rating','sentiment','neg','neu','pos']] 
        htmlcode = newdf.to_html()
        # set id to table
        htmlcode = htmlcode.replace('<table border="1" class="dataframe">','<table id="data" border="1" class="dataframe">')

        # get positive count from df
        positive_count = newdf[newdf['sentiment'] == 'positive'].count()['sentiment']
        # get negative count from df
        negative_count = newdf[newdf['sentiment'] == 'negative'].count()['sentiment']
        # get neutral count from df
        neutral_count = newdf[newdf['sentiment'] == 'neutral'].count()['sentiment']


        data = analysis.FetchStats(slug)
        industryLogo = 'https://www.hellopeter.com/'+data['industryLogo']
        trustIndex = data['trustIndex']
        keywords = data['businessDetails']['keywords']
        #remove any keywords that contains hello or peter
        keywords = [x for x in keywords if 'hello' not in x]
        keywords = [x for x in keywords if 'peter' not in x]
        businessDetails = data['businessDetails']
    except:
        score = 0
        avg_review_rating = 0
        htmlcode = ''
        industryLogo = ''
        trustIndex = 0
        keywords = []
        businessDetails = {}
        positive_count = 0
        negative_count = 0
        neutral_count = 0
    return render_template('semanticanalysis.html',slug=slug,encodedname=encodedname,score=score,avg_review_rating=avg_review_rating,htmlcode=htmlcode,industryLogo=industryLogo,keywords=keywords,trustIndex=trustIndex,positive_count=positive_count,negative_count=negative_count,neutral_count=neutral_count,businessDetails=businessDetails)
#running server on port 8000 - you can change the values here
if __name__ == "__main__":
  app.run(host="0.0.0.0",port=8000,debug=True)


