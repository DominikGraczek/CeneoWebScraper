from app import app
from flask import render_template, request, redirect, url_for
from app.utils import get_element,selectors
from bs4 import BeautifulSoup
import requests
import json
import os
@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/ekstrakcja-opini', methods=['POST','GET'])
def ekstrakcja():
    if request.method == "POST":
        product_code = request.form['product_id']
        all_opinions = []
        url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
        while(url):
            print(url)
            response = requests.get(url)
            page = BeautifulSoup(response.text, 'html.parser')
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = {}
                for key, value in selectors.items():
                    single_opinion[key] = get_element(opinion,*value)
                all_opinions.append(single_opinion)
        try:
            url = "https://www.ceneo.pl"+get_element(page, "a.pagination__next", "href")
        except TypeError:
            url = None

        print(len(all_opinions))
        try:
            os.mkdir("./opinions")
        except FileExistsError:
            pass
        with open(f"./app/static/opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4,ensure_ascii=False)
        opinions = pd.read_json(f"./opinions/{product_code}.json")
        opinions.score = opinions.score.map(lambda x: float(x.split("/")[0].replace(",",".")))
        stats = {
            "opinions_count" : opinions.shape[0],
            "pros_count":  int(opinions.pros.map(bool).sum()),
            "cons_count": int(opinions.cons.map(bool).sum()),
            "avg_score": opinions.score.mean().round(2)
        }
        score = opinions.score.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value = 0)
        score.plot.bar(color="hotpink")
        plt.xticks(rotation=0)
        plt.title("Histogram ocen")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        for index, value in enumerate(score):
            plt.text(index, value+0.5, str(value), ha="center")
        # plt.show()
        try:
            os.mkdir("./app/static/plots")
        except FileExistsError:
            pass
        plt.savefig(f"./app/static/plots/{product_code}_score.png")
        plt.close()

        # udział poszczególnych rekomendacji w ogólnej liczbie opinii
        recommendation = opinions["recommendation"].value_counts(dropna = False).sort_index()
        print(recommendation)
        recommendation.plot.pie(
            label="", 
            autopct="%1.1f%%",
            labels = ["Nie polecam", "Polecam", "Nie mam zdania"],
            colors = ["crimson", "forestgreen", "gray"]
        )
        plt.legend(bbox_to_anchor=(1.0,1.0))
        plt.savefig(f"./app/static/plots/{product_code}_recommendation.png")
        plt.close()
        stats['score'] = score.to_json()
        stats['recommendation'] = recommendation.to_json()
        try:
            os.mkdir("./app/static/plots")
        except FileExistsError:
            pass
        with open(f"./app/static/opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4,ensure_ascii=False)
        return redirect(url_for('produkt', product_code=product_code))
    return render_template("ekstrakcja-opini.html")

@app.route('/lista-produktow')
def lista_produktow():
    return render_template("lista-produktow.html")

@app.route('/o-autorze')
def author():
    return render_template("o-autorze.html")
@app.route('/produkt/<product_code>')
def produkt(product_code):
    return render_template("produkt.html", product_code=product_code)
@app.route('/wykresy')
def wykresy():
    return render_template("wykresy.html")
