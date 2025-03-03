from flask import Flask, request, jsonify

app = Flask(__name__)

dictionary = {}

@app.route('/api/words', methods=['GET'])
def get_words():
    return jsonify(dictionary)

@app.route('/api/words', methods=['POST'])
def add_word():
    word = request.json.get('word')
    definition = request.json.get('definition')
    dictionary[word] = definition
    return jsonify({word: definition}), 201

@app.route('/api/words/<word>', methods=['GET'])
def get_word(word):
    definition = dictionary.get(word)
    if definition:
        return jsonify({word: definition})
    else:
        return jsonify({"error": "Word not found"}), 404

@app.route('/api/words/<word>', methods=['PUT'])
def update_word(word):
    definition = request.json.get('definition')
    if word in dictionary:
        dictionary[word] = definition
        return jsonify({word: definition})
    else:
        return jsonify({"error": "Word not found"}), 404

@app.route('/api/words/<word>', methods=['DELETE'])
def delete_word(word):
    if word in dictionary:
        del dictionary[word]
        return jsonify({"message": "Word deleted"})
    else:
        return jsonify({"error": "Word not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
