from flask import jsonify

def ask_mattress_features(request):
    features = {
        'firmness': ['medium', 'firm', 'extra firm', 'plush'],
        'cooling_technology': ['yes', 'no'],
        'motion_separation': ['yes', 'no'],
        'pressure_relief': ['yes', 'no'],
        'support': ['yes', 'no'],
        'adjustable_base_friendly': ['yes', 'no'],
        'breathable': ['yes', 'no'],
        'mattress_in_a_box': ['yes', 'no']
    }
    
    response = {
        'message': 'What features do you want in the mattress?',
        'options': features
    }
    
    return jsonify(response), 200