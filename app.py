from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Needed to use sessions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gs.html')
def get_started():
    # It still looks inside the 'templates' folder for the actual file
    return render_template('gs.html')

@app.route('/api/select-path', methods=['POST'])
def select_path():
    data = request.get_json()
    
    # Extract the data
    grade = data.get('grade')
    subject = data.get('subject')
    module = data.get('module')

    # Store in session so you can use it on the next page
    session['user_selection'] = {
        'grade': grade,
        'subject': subject,
        'module': module
    }

    print(f"Flask received: Grade {grade}, Subject {subject}, Module {module}")

    # for now redirect back to home; later this can point to /lesson or another page
    return jsonify({"status": "success", "redirect": "/"}), 200

if __name__ == '__main__':
    app.run(debug=True)