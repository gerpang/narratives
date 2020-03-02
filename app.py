
from flask import Flask, request, jsonify, render_template
import pickle
import implicit
from markupsafe import Markup
import pandas as pd

app = Flask(__name__)

 # Put model and lookup stuff in it's own library TODO

NUM_TO_RETURN = 20

def get_meta(work_id):
    
    # Lookup matrix index for fanwork ID
    work_indice = indices['work_id'][str(work_id)]
    # Find similar items
    related_BPR = model.similar_items(work_indice)

    for work in related_BPR:
        # Find fanwork ID from matrix indices
        suggested_id = inverted_indices['work_id'][work[0]]
        meta = df_meta.loc[df_meta['work_id'] == int(suggested_id)]
        title = meta['title'].values[0]
        rating = meta['rating'].values[0]
        yield suggested_id, title, rating

def validate(request):
    try:
        fanwork_id = [int(x) for x in request.form.values()][0]
    except:
        raise ValueError("Enter a number as fanwork ID")
        return
    if (df_meta['work_id'] == fanwork_id).any() :
        return fanwork_id
    else:
        raise ValueError('FanWork ID not in current recommendation system')

@app.before_first_request
def load__model():
    global model
    global indices
    global inverted_indices
    global df_meta

    model = pickle.load(open('models/bpr270220.pkl', 'rb'))
    indices = pickle.load(open('models/indices270220.pkl', 'rb'))
    inverted_indices = {'work_id':{}, 'user':{}}
    inverted_indices['work_id'] = {v: k for k, v in indices['work_id'].items()}
    inverted_indices['user'] = {v: k for k, v in indices['user'].items()}
    df_meta = pd.read_csv('models/fanfics_metadata.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            fanwork_id = validate(request)
        except Exception as e:
            errormsg = f"{str(e)}"
            return render_template('index.html', prediction_text=errormsg) 

        suggestions = get_meta(fanwork_id)
        response = f"Suggested works for <a href='http://ao3.org/works/{fanwork_id}'>{next(suggestions)[1]}</a>:<br><br>"
        next(suggestions)
        count = 1
        #for count, meta in enumerate(suggestions):
        for suggested_id, title, rating in suggestions:
        #for count in range(NUM_TO_RETURN):
            if count > NUM_TO_RETURN: 
                print(f"breaking out at count value: {count}")
                break
            #boop = next(suggestions)
            #suggested_id, title, rating = meta[0], meta[1], meta[2]
            #suggested_id, title, rating = boop[0], boop[1], boop[2]
            link = f"<a href ='http://ao3.org/works/{suggested_id}'>{count}-{title}-{rating}</a><br>"
            response = response + link
            count += 1
        return render_template('index.html', prediction_text = Markup(response))

@app.route('/<work_id>', methods=['POST'])
def predict_again(work_id):
    #make generator pickup where it left off at
    return return_template('index.html', work_id=work_id)

if __name__ == "__main__":
    app.run(debug=True)