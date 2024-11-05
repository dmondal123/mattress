from flask import jsonify

def ask_budget(request):
    # Define the budget ranges
    budget_ranges = [
        '0-500',
        '500-1000',
        '1000-1500',
        '1500-2000',
        '2000-2500',
        '2500-3000',
        '3000-3500',
        '3500-4000',
        '4000-4500',
        '4500-5000',
        '5000-5500',
        '5500-6000',
        '6000-6500'
    ]
    
    response = {
        'message': 'What is your budget range for a mattress?',
        'options': budget_ranges
    }
    
    return jsonify(response), 200