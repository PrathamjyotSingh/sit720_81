# Housing Price Prediction – Jenkins DevOps Pipeline

## Project Overview

This project is a **Housing Price Prediction application** developed using Python and Machine Learning. The application predicts house prices based on user-provided inputs through an interactive **Streamlit** interface.

A **Jenkins CI/CD pipeline** has been implemented to automate the software delivery process, including building, testing, code quality analysis, security scanning, deployment preparation, release packaging, and monitoring.

## Technologies Used

- Python 3.13
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Streamlit
- Pytest
- Flake8
- pip-audit
- Jenkins
- GitHub

## Project Structure

```text
.
├── app.py
├── prediction.py
├── housing_price_model_final.pkl
├── requirements.txt
├── Jenkinsfile
├── tests/
│   ├── test_model.py
│   └── test_prediction.py
└── README.md
