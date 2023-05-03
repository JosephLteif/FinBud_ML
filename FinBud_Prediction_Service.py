import pickle

from flask import Flask, jsonify, request

# creating a Flask app
app = Flask(__name__)
loaded_model = None


@app.route('/', methods=['GET', 'POST'])
def home():
    return "API Running"


@app.route('/Predict_Expenses', methods=['POST'])
def predict_expenses():
    data = request.get_json()
    number_of_people = data.get('NumberOfPeople', '')
    employment_status = data.get('Employment status', '')
    employment_status_dict = {'Employed': 0, 'Self-Employed': 2, 'Not Employed': 1}
    employment_status = employment_status_dict[employment_status]
    income = data.get('Income', '')
    income_dict = {'Between $1200 and $1500': 0, 'Between $1000 and $1200': 1, 'Between $0 and $300': 2,
                   'More than $1500': 3, 'Between $800 and $1000': 4, 'Between $500 and $800': 5,
                   'Between $300 and $500': 6}
    income = income_dict[income]
    marital_status = data.get('Marital Status', '')
    marital_status_dict = {'Single': 0, 'Widowed': 1, 'Divorced': 2, 'Married': 3}
    marital_status = marital_status_dict[marital_status]
    industry = data.get('Industry', '')
    industry_dict = {'Computer and information technology': 0, 'Other': 1, 'Food and hospitality': 2, 'Retail': 3,
                     'Advertising and marketing': 4, 'Architecture': 5, 'Health care': 6, 'Education': 7,
                     'Arts and entertainment': 8}
    industry = industry_dict[industry]
    data = loaded_model.predict([[number_of_people, employment_status, income, marital_status, industry]])
    prediction_dict = {'Between $1000 and $1200': 0, 'Between $300 and $500': 1,
                       'Between $0 and $300': 2, 'More than $1500': 3, 'Between $800 and $1000': 4,
                       'Between $500 and $800': 5, 'Between $1200 and $1500': 6}
    data = [key for key, value in prediction_dict.items() if value == round(data.flatten()[0])]
    return jsonify({'Predicted Expenses': str(data[0])})


# driver function
if __name__ == '__main__':
    filename = 'finalized_model.sav'
    # Load the model
    loaded_model = pickle.load(open(filename, 'rb'))
    app.run(debug=True)
