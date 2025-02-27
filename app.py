from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np


app = Flask(__name__, static_url_path='/static')

# Load both models at startup
try:
    credit_card_model = joblib.load('./models/credit_card_model.pkl')

    if isinstance(credit_card_model, dict):
        credit_card_model = credit_card_model.get("model", None)  
         
except Exception as e:
    print(f"Error loading credit card fraud model: {e}")
    credit_card_model = None

try:
    online_payment_model = joblib.load('./models/online_payment_model.pkl')

    if isinstance(online_payment_model, dict):
        online_payment_model = online_payment_model.get("model", None)  

except Exception as e:
    print(f"Error loading online payment fraud model: {e}")
    online_payment_model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crdtfrdtcn')
def credit_fraud():
    return render_template('crdFrdDtcn.html')

@app.route('/onlnpymntfrddtcn')
def online_fraud():
    return render_template('OnlPymntFrdDtctn.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/predict_credit_fraud', methods=['POST'])
def predict_credit_fraud():
    if credit_card_model is None:
        return jsonify({'error': 'Credit card fraud detection model not loaded properly'})

    try:
        # Get form data
        amount = float(request.form['TrnAmn'])
        zip_code = request.form['ZipCode']  # This matches our new form field name
        trans_hour = int(request.form['TrnHr'])
        age = int(request.form['Age'])

        # Validate inputs
        if not (0 <= trans_hour <= 23):
            return jsonify({'error': 'Transaction hour must be between 0 and 23'})
        
        # Validate ZIP/PIN code
        # Remove any whitespace and convert to string
        zip_code = str(zip_code).strip()
        # Check for either US ZIP (5 digits) or Indian PIN (6 digits)
        if not (len(zip_code) == 5 or len(zip_code) == 6) or not zip_code.isdigit():
            return jsonify({'error': 'Please enter a valid 5-digit US ZIP code or 6-digit Indian PIN code'})
        
        zip_code = int(zip_code)  # Convert to integer for model
        
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'})
        if not (18 <= age <= 100):
            return jsonify({'error': 'Age must be between 18 and 100'})

        # Prepare features for prediction
        features = np.array([[amount, zip_code, trans_hour, age]])

        # Make prediction
        prediction = credit_card_model.predict(features)[0]
        probability = credit_card_model.predict_proba(features)[0][1]

        # Prepare result
        result = {
            'prediction': 'Fraudulent' if prediction == 1 else 'Legitimate',
            'probability': float(probability),
            'confidence': 'High' if abs(probability - 0.5) > 0.3 else 'Low'
        }

        return render_template('result.html', 
                             result=result, 
                             transaction_type='Credit Card',
                             details={
                                 'Amount': f'${amount:,.2f}',
                                 'Postal Code': zip_code,
                                 'Transaction Hour': f'{trans_hour:02d}:00',
                                 'Age': age
                             })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predict_online_fraud', methods=['POST'])
def predict_online_fraud():
    if online_payment_model is None:
        return jsonify({'error': 'Online payment fraud detection model not loaded properly'})

    try:
        # Get form data
        amount = float(request.form['TrnAmn'])
        old_balance = float(request.form['oldBalance'])
        new_balance = float(request.form['newAccBalance'])
        transaction_type = request.form['inputType']

        # Validate inputs
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'})
        if old_balance < 0 or new_balance < 0:
            return jsonify({'error': 'Balance cannot be negative'})
        if transaction_type not in ['cshOut', 'transfer', 'online', 'payment']:
            return jsonify({'error': 'Invalid transaction type'})

        # Calculate derived features
        transaction_diff = old_balance - new_balance
        transaction_ratio = amount / old_balance if old_balance != 0 else 0

        # Prepare features for prediction
        features = np.array([[amount, old_balance, new_balance, transaction_diff]])

        # Make prediction
        prediction = online_payment_model.predict(features)[0]
        probability = online_payment_model.predict_proba(features)[0][1]

        # Prepare result
        result = {
            'prediction': 'Fraudulent' if prediction == 1 else 'Legitimate',
            'probability': float(probability),
            'confidence': 'High' if abs(probability - 0.5) > 0.3 else 'Low'
        }

        return render_template('result.html', 
                               result=result, 
                               transaction_type='Online Payment',
                               details={
                                   'Amount': f'${amount:,.2f}',
                                   'Old Balance': f'${old_balance:,.2f}',
                                   'New Balance': f'${new_balance:,.2f}',
                                   'Transaction Type': transaction_type.capitalize()
                               })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
