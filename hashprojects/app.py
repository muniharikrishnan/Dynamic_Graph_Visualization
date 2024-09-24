from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Adjust origin as needed

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456srikrishna$@localhost/hashagiles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the UserFiles model
class UserFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_content = db.Column(db.Text, nullable=False)
 
    def __repr__(self):
        return f'<UserFiles {self.file_name}>'

# Create the database and tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/save_csv', methods=['POST'])
def save_csv():
    data = request.get_json()
    if not data or 'file_name' not in data or 'file_content' not in data:
        return jsonify({'message': 'Invalid data provided.'}), 400

    file_name = data['file_name']
    file_content = data['file_content']
    
    new_file = UserFiles(file_name=file_name, file_content=file_content)
    db.session.add(new_file)
    db.session.commit()
    
    return jsonify({'message': 'File saved successfully!'}), 200

@app.route('/files', methods=['GET'])
def get_files():
    files = UserFiles.query.all()
    return jsonify([{'id': file.id, 'file_name': file.file_name} for file in files]), 200

@app.route('/files/<int:file_id>', methods=['GET'])
def get_file_content(file_id):
    file = UserFiles.query.get(file_id)
    if file:
        return jsonify({'file_name': file.file_name, 'file_content': file.file_content}), 200
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ensure the port matches your setup
 

