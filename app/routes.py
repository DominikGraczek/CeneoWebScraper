from app import app

@app.route('/')
@app.route('/index')
def index():
    # return "Hello, Dominik Graczek!"
    return render_template("home.html")
# @app.route('/name/',defaults={'name':"Anonim"})
# @app.route('/name/<name>')
# def name(name = None):
#     return f"Hello, {name}!"

@app.route('/ekstrakcja-opini')
def ekstrakcja():
    return render_template("ekstrakcja-opini.html")

@app.route('/lista-produktow')
def lista_produktow():
    return render_template("lista-produktow.html")

@app.route('/o-autorze')
def author():
    return render_template("o-autorze.html")
@app.route('/ekstrakcja-opini')
def ekstrakcja():
    return render_template("ekstrakcja-opini.html")
@app.route('/produkt')
def produkt():
    return render_template("produkt.html")
@app.route('/wykresy')
def wykresy():
    return render_template("wykresy.html")
