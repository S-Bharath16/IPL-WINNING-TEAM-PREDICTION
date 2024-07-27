from django.shortcuts import render
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# Load data
data = pd.read_csv("C:/Users/bhara/Final.csv")

# Extract features and target variable from the data
X = data[['batting_team', 'bowling_team', 'city', 'runs_left', 'balls_left', 'wickets_remaining', 'total_runs_x']]
y = data['result']

# Define a ColumnTransformer to encode categorical variables
column_transformer = ColumnTransformer(
    transformers=[
        ('encoder', OneHotEncoder(drop='first'), ['batting_team', 'bowling_team', 'city'])
    ],
    remainder='passthrough'
)

# Create a pipeline with the transformer and the RandomForest model
pipe = Pipeline(steps=[
    ('preprocessor', column_transformer),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipe.fit(X, y)


def home(request):
    return render(request, 'main.html')


def predict(request):
    if request.method == 'POST':
        batting_team = request.POST.get('batting_team')
        bowling_team = request.POST.get('bowling_team')
        city = request.POST.get('city')
        runs_left = int(request.POST.get('runs_left'))
        balls_left = int(request.POST.get('balls_left'))
        wickets_remaining = int(request.POST.get('wickets_remaining'))
        total_runs_x = int(request.POST.get('total_runs_x'))

        # Prepare input data
        input_data = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets_remaining': [wickets_remaining],
            'total_runs_x': [total_runs_x]
        })

        # Make prediction
        prediction = pipe.predict(input_data)
        win_probability = pipe.predict_proba(input_data)[0][1]

        return render(request, 'result.html', {
            'prediction': 'Win' if prediction == 1 else 'Lose',
            'win_probability': win_probability
        })

    return render(request, 'predict.html')
