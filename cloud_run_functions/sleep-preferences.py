from flask import jsonify

def ask_sleep_preferences(request):
    sleep_preferences = ['side', 'back', 'stomach', 'pain', 'bed partner', 'temperature', 'all', 'toss and turn']

    response = {
        'message': 'What sleep preferences do you have?',
        'options': sleep_preferences
    }
    
    return jsonify(response), 200