from flask import jsonify

def ask_mattress_size(request):
    mattress_sizes = ['king', 'queen', 'full', 'full xl', 'twin','twin xl', 'cal king', 'split cal king', 'RV Short Queen', 'Narrow Twin']

    response = {
        'message': 'What size mattress do you need?',
        'options': mattress_sizes
    }
    
    return jsonify(response), 200