from flask import Flask,render_template,send_from_directory,request
import search.searchengine as se

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
 


#running server on port 8000 - you can change the values here
if __name__ == "__main__":
  app.run(host="0.0.0.0",port=8000,debug=True)