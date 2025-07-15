'''
Dummy
'''
from flask import Flask, request, jsonify
from src import creation

app = Flask(__name__)

@app.route('/creation', methods=['GET', 'POST'])
def creation_endpoint():
    '''
    Dummy
    '''
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        try:
            # Extract arguments from JSON payload
            anchor = data.get('anchor')
            target = data.get('target')
            dirname = data.get('outputDir')
            
            # Log the extracted values
            # print(f'Anchor: {anchor}, Target: {target}')

            # Call the workflow from basic_docking
            result = creation.create(anchor, target, dirname)
            return jsonify({'message': 'Creation completed successfully', 'result': result}, 200)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Creation endpoint'})


if __name__ == '__main__':
    # Expose the app on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)