import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api('swagger.yml')

@app.route('/')
def home():
    return "hello there"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)