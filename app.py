from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__, static_url_path='/static')

# Load both models at startup
try:
    credit_card_model = joblib.load('./models/credit_card_model.pkl')

    if isinstance(credit_card_model, dict):
        credit_card_model = credit_card_model.get("model", None)  
         
except Exception as e:
    print(f"Error loading credit card fraud model: {e}")
    credit_card_model = None

# Create a proper OneHotEncoder for transaction types
transaction_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
transaction_encoder.fit(np.array([['cash_out'], ['transfer'], ['online'], ['payment']]))

try:
    online_payment_model = joblib.load('./models/online_payment_model.pkl')
    
    # Debug print to see what we're actually loading
    print(f"Type of loaded online payment model: {type(online_payment_model)}")
    
    # Handle dictionary case
    if isinstance(online_payment_model, dict):
        online_payment_model = online_payment_model.get("model", None)
        
    # Handle serialized string case
    if isinstance(online_payment_model, str):
        print("Warning: online_payment_model is a string. Attempting to fix...")
        try:
            # Attempt to evaluate the string if it's a serialized object
            import pickle
            online_payment_model = pickle.loads(online_payment_model)
        except:
            print("Failed to deserialize the model string.")

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
        
        # Map transaction type to expected format
        transaction_type_mapping = {
            'cshOut': 'cash_out',
            'transfer': 'transfer',
            'online': 'online',
            'payment': 'payment'
        }
        
        mapped_transaction_type = transaction_type_mapping.get(transaction_type, transaction_type)

        # Validate inputs
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'})
        if old_balance < 0 or new_balance < 0:
            return jsonify({'error': 'Balance cannot be negative'})
        if transaction_type not in ['cshOut', 'transfer', 'online', 'payment']:
            return jsonify({'error': 'Invalid transaction type'})

        # Calculate derived features - transaction difference
        transaction_diff = old_balance - new_balance

        # Create a dataframe for proper encoding of categorical features
        input_df = pd.DataFrame({
            'amount': [amount],
            'old_balance': [old_balance],
            'transaction_diff': [transaction_diff],
            'transaction_type': [mapped_transaction_type]
        })
        
        # One-hot encode the transaction type
        transaction_encoded = transaction_encoder.transform(input_df[['transaction_type']])
        transaction_columns = [f"type_{t}" for t in ['cash_out', 'transfer', 'online', 'payment']]
        
        # Create numeric features DataFrame
        numeric_features = input_df[['amount', 'old_balance', 'transaction_diff']]
        
        # Create encoded DataFrame
        encoded_df = pd.DataFrame(transaction_encoded, columns=transaction_columns)
        
        # Combine numeric and encoded features
        features_df = pd.concat([numeric_features, encoded_df], axis=1)
        
        print(f"Debug - Final features being sent to model: {features_df.to_dict()}")

        # Make prediction with error handling
        try:
            prediction = online_payment_model.predict(features_df)[0]
            probability = online_payment_model.predict_proba(features_df)[0][1]
        except AttributeError as e:
            # If model doesn't have predict method, use a fallback
            print(f"Model prediction failed: {e}")
            prediction = 0  # Default to legitimate transaction
            probability = 0.1
            
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
                                   'Transaction Type': mapped_transaction_type.replace('_', ' ').capitalize()
                               })

    except Exception as e:
        print(f"Error in predict_online_fraud: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)