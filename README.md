# FraudSaver: Fraud Detection System

FraudSaver is a machine learning-powered System that detects potential fraud in credit card and online payment transactions.

## Features

- Credit Card Fraud Detection
- Online Payment Fraud Detection
- Real-time Fraud Probability Calculation
- Responsive Web Interface

## Installation

1. Clone the repository:

```bash
Copygit clone https://github.com/yourusername/fraudsaver.git
cd fraudsaver
```

2. Create a virtual environment:

``` bash
Copypython -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
Copypip install -r requirements.txt
```

The application will be available at `http://localhost:5000`


creditcard.csv for Credit Card Fraud
onlinepayment.csv for Online Payment Fraud

## Model Training
Run Jupyter Notebooks:

credit_card_fraud_detection.ipynb
online_payment_detection.ipynb

## Notebooks will generate:

credit_card_model.pkl
online_payment_model.pkl

Running the Application
bash Copy python app.py

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JS
- **Machine Learning**: scikit-learn, SMOTE
- **Data Processing**: pandas, numpy
- **NLP**: NLTK, TfidfVectorizer


## Model Performance

1. Accuracy: 95%+ for both models
2. Uses SMOTE for handling class imbalance
3. Supports multiple ML algorithms

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
[MIT LICENSE](https://github.com/riya-py/EFraudSaver/blob/main/LICENSE)

## Contact

twitter- [@riya_pyy](https://twitter.com/riya_pyy)
gmail- riya.rk006@gmail.com

Project Link: [https://github.com/riya-py/Fraudsaver](https://github.com/riya-py/Fraudsaver)
