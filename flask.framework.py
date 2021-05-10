from flask import Flask,render_template #render template .html uzantılı anasayfayı proje içinden response edebilmek için çagırıldı

app = Flask(__name__)

@app.route("/")#tırnak içinde / bırakırsak anasayfa
def anasayfa():
    on=10
    yirmi=20
    sozluk= {"TL":"Türkiye","Dolar":"ABD","Euro":"AB"}

    return render_template("anasayfa.html",number=on,number2=yirmi,sozluk=sozluk)
    #number adıyla html sayfasında 10'u kullanıcaz


@app.route("/hakkimizda")
def hakkimizda():
    return render_template("hakkimizda.html")

@app.route("/inheritence")#miras aldı
def inheritence():
    return render_template("inheritence.html")  


if __name__=="__main__":
    app.run(debug=True)
    
