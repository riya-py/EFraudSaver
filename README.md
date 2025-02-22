# EFraudSaver: Fraud Detection System

EFraudSaver is a machine learning-powered System that detects potential fraud in credit card and online payment transactions.

## Features

- Credit Card Fraud Detection
- Online Payment Fraud Detection
- Real-time Fraud Probability Calculation
- Responsive Web Interface

## Installation

1. Clone the repository:

```bash
Copygit clone https://github.com/yourusername/efraudsaver.git
cd efraudsaver
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

## Project Structure 
```
project_root/
│   ├── models/             # ML model related code
│       ├── credit_card_model.pkl
│       └── online_payment_model.pkl

├── static/                 # Static files
│   ├── css/
│   │   ├── cdFrdDtc_style.css
|   |   ├── indexStyle.css
|   |   ├── OnlpymntFrdDtcn.css
│   │   └── result.css
│   ├── images/                
│
├── templates/             # HTML templates
│   ├── crdDrdDtcn.html         
│   ├── index.html
|   ├── OnlPymntFrdDtcn.html
│   └── result.html
|
│ # Jupyter notebooks for analysis
|── credit_card_fraud_detection.ipynb 
|── online_payment_fraud_detection.ipynb 
│
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```


## Model Training
Run Jupyter Notebooks:

credit_card_fraud_detection.ipynb
online_payment_detection.ipynb

## Notebooks will generate:

#### models
credit_card_model.pkl
online_payment_model.pkl

#### and
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
This project is licensed under the MIT License - see the [MIT LICENSE](https://github.com/riya-py/EFraudSaver/blob/main/LICENSE) file for details.

## Contact

X- [@riya_pyy](https://twitter.com/riya_pyy)
gmail- riya.rk006@gmail.com

Project Link: [https://github.com/riya-py/EFraudSaver](https://github.com/riya-py/EFraudSaver)
