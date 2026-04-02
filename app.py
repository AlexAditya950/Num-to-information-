from flask import Flask, render_template, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form.get('number', '').strip()
        if not number:
            return render_template('index.html', error="Phone number daalo!")
        
        try:
            # Agar + nahi hai toh add kar do (India ke liye default)
            if not number.startswith('+'):
                number = '+91' + number if len(number) == 10 else '+' + number
            
            parsed_number = phonenumbers.parse(number)
            
            info = {
                'number': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'valid': phonenumbers.is_valid_number(parsed_number),
                'possible': phonenumbers.is_possible_number(parsed_number),
                'country': geocoder.description_for_number(parsed_number, 'en'),
                'carrier': carrier.name_for_number(parsed_number, 'en') or "Unknown",
                'timezone': timezone.time_zones_for_number(parsed_number),
                'country_code': parsed_number.country_code,
                'national_number': parsed_number.national_number
            }
            
            return render_template('index.html', info=info, number=number)
        
        except Exception as e:
            return render_template('index.html', error=f"Invalid number ya error: {str(e)}")
    
    return render_template('index.html')

@app.route('/api/lookup', methods=['POST'])
def api_lookup():
    data = request.get_json()
    number = data.get('number', '') if data else ''
    
    if not number:
        return jsonify({'error': 'Number required'}), 400
    
    try:
        if not number.startswith('+'):
            number = '+91' + number if len(number.replace('+','')) == 10 else '+' + number
        
        parsed = phonenumbers.parse(number)
        
        result = {
            'input': number,
            'formatted': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'valid': phonenumbers.is_valid_number(parsed),
            'country': geocoder.description_for_number(parsed, 'en'),
            'carrier': carrier.name_for_number(parsed, 'en') or "Unknown",
            'timezone': list(timezone.time_zones_for_number(parsed)),
            'country_code': parsed.country_code
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
