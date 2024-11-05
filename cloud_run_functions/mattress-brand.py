from flask import jsonify

def ask_mattress_brand(request):
    brands = ['Beautyrest', 'Delta', 'Nectar', 'Sealy', 'Serta', 'Sleepy', 'Tulo', 'DreamCloud', 'Tempur-Pedic', 'Zinus', 'Purple', 'Stearns and Foster']

    response = {
        'message': 'What brand are you looking for?',
        'options': brands
    }
    
    return jsonify(response), 200