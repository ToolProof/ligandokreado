'''
Dummy
'''
from flask import Flask, request, jsonify
from src import addition, multiplication

app = Flask(__name__)

@app.route('/addition', methods=['GET', 'POST'])
def addition_endpoint():
    '''
    Dummy
    '''
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        try:
            # Extract arguments from JSON payload
            number_A = data.get('number_A')
            number_B = data.get('number_B')
            
            # Log the extracted values
            print(f'Number A: {number_A}, Number B: {number_B}')

            # Call the workflow from basic_docking
            result = addition.add(number_A, number_B)
            return jsonify({'message': 'Addition completed successfully', 'result': result}, 200)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Addition endpoint'})


@app.route('/multiplication', methods=['GET', 'POST'])
def multiplication_endpoint():
    '''
    Dummy
    '''
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        try:
            # Extract arguments from JSON payload
            number_A = data.get('number_A')
            number_B = data.get('number_B')
            
            # Log the extracted values
            print(f'Number A: {number_A}, Number B: {number_B}')

            # Call the workflow from basic_docking
            result = multiplication.multiply(number_A, number_B)
            return jsonify({'message': 'Multiplication completed successfully', 'result': result}, 200)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Multiplication endpoint'})


if __name__ == '__main__':
    # Expose the app on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)