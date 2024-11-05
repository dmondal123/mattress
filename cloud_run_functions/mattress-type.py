from flask import jsonify

def ask_mattress_type(request):
    mattress_types = ['memory foam', 'innerspring', 'hybrid', "foam"]
    
    response = {
        'message': 'What type of mattress are you looking for?',
        'options': mattress_types
    }
    
    return jsonify(response), 200