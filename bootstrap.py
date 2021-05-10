from flask import Flask, render_template,redirect,request,url_for,flash,session#redirect ve sonrakiler form işlemleri için gerekli    session giriş yapılıp yapılmadığının kontrolü
#cmd den pip3 install wtforms indirdik       flash için pip3 install ladık
import wtforms
from flask_mysqldb import MySQL #veri tabanı için
from passlib.hash import sha256_crypt #parolayı şifrelemek için






class RegisterForm(wtforms.Form): #formlar class la oluşturulur validators.DataRequired o kutucuga bişey girme zorunlulugu veriyor istersen .length ile de uzunluk falan ölçebilirsin

    name = wtforms.StringField("İsim",validators= [wtforms.validators.DataRequired()])#validators ler boşluk kısımlarının kuralarıdır

    username = wtforms.StringField("Kullanıcı Adı",validators=[wtforms.validators.DataRequired(),
                                    wtforms.validators.Length(min=5,max=25,message="Geçersiz Kullanıcı Adı")])#, ile ayırabliriz listeler validators.length belirttik min8 mx25 olsun kullanıcı adı diye

    email = wtforms.StringField("E-Mail",validators=[wtforms.validators.DataRequired(),wtforms.validators.Email(message="Lütfen Geçerli Bir E-mail adres girin")])# validators.Email girilenin e mail olup olmadıgını anlıyo

    password = wtforms.PasswordField("Parola", validators=[wtforms.validators.DataRequired(),#farklı olarak passwordfield verildi yazarken gözükmesin diye
                                    wtforms.validators.Length(min=8,max=25,message="parola 8-25 karakter uzunluğunda olmalıdır.")])                          




class LoginForm(wtforms.Form): #login kısmımızın girişleri
    username = wtforms.StringField("Kullanıcı Adı",validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Parola", validators=[wtforms.validators.DataRequired()])




class ArticleForm(wtforms.Form):
    title = wtforms.StringField("Makale Başlığı", validators=[wtforms.validators.DataRequired(),wtforms.validators.Length(min=5,max=150)])
    content = wtforms.TextAreaField("Makale", validators=[wtforms.validators.DataRequired(),wtforms.validators.Length(min=10,max=15000)])

#validatorslere girdigimiz message= ile istediğimiz uyarıyı verebiliriz koşul saglanmadıgında                         
app = Flask(__name__)
"""ÖNCE navbar html i includes altında açtık ve direk nası görünüyorsa öylece attık
sonra templates de layout attık ve css le script kodlarının nerlere konulacağına bootstrapten bakıp yerlerine koyduk
ve {% include "includes/navbar.html" %} i body içine yazarak navbarı layout'a çağırdık en sonunda da buradan
siteyi çalıştırdık."""

app.secret_key = "devkodblog"#flash mesajı için




mysql = MySQL(app)
app.config["MYSQL_HOST"] = "localhost"#hangi servera baglandıgımızı belirttik localdeyiz suan
app.config["MYSQL_USER"] = "root"#xampp le kurdugumuz serverin user adı root
app.config["MYSQL_PASSWORD"] = "" #password default boş gelir
app.config["MYSQL_DB"] = "devkodblog" # serverimiz içindeki oluşturdugumuz devkodblok data base'ini belirttik
app.config["MYSQL_CURSORCLASS"] = "DictCursor"









#-------------------------------------------- MAKALE EKLEME KISMI --------------------------------------------------------
@app.route("/addarticle", methods=["GET","POST"])
def addarticle():
    if session:
        form = ArticleForm(request.form)
        if request.method == "POST" and form.validate():
            title = form.title.data
            content = form.content.data


            cursor = mysql.connection.cursor()
            kayit = "INSERT INTO articles(title,author,content) VALUES(%s,%s,%s)"
            cursor.execute(kayit, (title,session["username"],content))
            mysql.connection.commit()
            cursor.close()
            flash("Makale Başarıyla Kaydedildi!","info")
            return redirect(url_for("dashboard"))
        else:
            return render_template("addarticle.html",form=form)


    else:
        flash("Makale Eklemek İçin Giriş Yapınız!","danger")
        return redirect(url_for("login"))
    







@app.route("/")
def deneme():
    return render_template("index.html")





@app.route("/index")
def index():
    on=10
    liste=[10,11,12,13,14]
    demet=(1,2,3,4,5)
    sozluk= [
        {"KaydedilmeTarihi":12,"Yazar":"Bilal","SonErişimTarihi":25},
        {"KaydedilmeTarihi":13,"Yazar":"Muhammet","SonErişimTarihi":26},       
        {"KaydedilmeTarihi":14,"Yazar":"Ahmet","SonErişimTarihi":28}
    ]

    return render_template("index.html",on=on,liste=liste,demet=demet,sozluk=sozluk)





@app.route("/about")
def about():
    return render_template("about.html")





@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()

    sorgu = "SELECT * FROM articles"

    cursor.execute(sorgu)

    articles = cursor.fetchall()

    return render_template("articles.html", articles=articles)
   





@app.route("/articles/<string:id>")#Dinamik url tanımlama
def articles_detail(id):#makalelerde / tan sonra kacıncı basılırsa basılsın not found almadan oraya gidilecek
    cursor = mysql.connection.cursor()#cursor oluşturmadan veritabanından id değerini çekemeyiz

    sorgu = "SELECT * FROM articles WHERE id=%s"

    result = cursor.execute(sorgu, (id,))

    if result >0:
        articles = cursor.fetchall() #fetchall ile articles ların hepsini alıyoruz
        
        return render_template("article_detail.html", articles = articles)

    else:
        flash("Aradığınız makale bulunamadı!","warning")
        return render_template("article_detail.html")
    return render_template("article_detail.html")

@app.route("/communicate")
def communicate():
    return render_template("communicate.html")







#----------------------------------KAYIT OL KISMI------------------------------
@app.route("/register", methods=["GET","POST"])#get request post request farklıdır
def register(): #post request bir bilgi iletmek istenildiğinde kullanılır (kayıt ol gibi)

    form = RegisterForm(request.form)

    
    if request.method=="POST" and form.validate():
        name = form.name.data #kayıt ol'un veri tabanına işlenmesi
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)#password veri tabanına şifrelenerek gidecek

        cursor = mysql.connection.cursor()
        kayit = "INSERT INTO users(name,username,email,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(kayit,(name,username,email,password))
        mysql.connection.commit() #mysql e veri vermek istediğimizi söyledik
        cursor.close()
        flash("Kayıt İşlemi Başarılı!","success")


        return redirect(url_for("deneme"))
    else:
        return render_template("register.html",form=form)






@app.route("/dashboard")#kontrol paneli giriş yapıldıgında cıkıyor
def dashboard():

    if session:
        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM articles WHERE author=%s"

        cursor.execute(sorgu,(session["username"],))

        articles = cursor.fetchall()

        return render_template("dashboard.html", articles=articles)
    else:
        flash("Kontrol Paneli sayfasına sadece üyeler erişebilr!","danger")
        return redirect(url_for("login"))
    



@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış Yapıldı","success")
    return redirect("index")





#------------------------------------GİRİŞ YAP KISMI---------------------------------------------------------------------
@app.route("/login",methods=["GET","POST"])
def login():

    form = LoginForm(request.form)  #en başta actıgımız loginformu aldık

    if request.method == "POST" and form.validate():
        username= form.username.data
        password_entered = form.password.data #username ve password_entered i data olarak belirttik

        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM users WHERE username = %s" #veritabanının ilgili kısmından username leri çekti
        result=cursor.execute(sorgu,(username,))#demetlerde ilk elemandan sonra virgül konulur yoksa python bunu demet olarak algılamaz

        if result>0:
            data = cursor.fetchone() #result 1 ise yani yazdıgımız kullanıcı adı veritabanında varsa buraya giriyor ve o satırdaki datalardan password'u real_password olarak kaydediyor
            real_password = data["password"]

            if sha256_crypt.verify(password_entered,real_password):#şifreler sha256 ile şifrelendi o yüzden denenen şifreyi de sha256 ile bakıp veritabanındakiyle aynı mı bakıyoruz
                session["logged_in"]= True
                session["username"]= username
                flash("Giriş Başarılı","success")
                return redirect(url_for("index"))
            else:
                flash("Parola Hatalı","danger")
                return redirect(url_for("login"))


        else:
            flash("Kullanıcı Adı Hatalı","danger")
            return redirect(url_for("login"))

    else:
        return render_template("login.html", form=form)

    return render_template("login.html",form=form)
    




@app.route("/delete/<string:id>")
def delete(id):
    if session:
        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM articles WHERE author=%s and id=%s"

        result = cursor.execute(sorgu,(session["username"], id))

        if result>0:
            sorgu2 = "DELETE FROM articles WHERE id=%s"

            cursor.execute(sorgu2,(id,))
            mysql.connection.commit()
            cursor.close()
            flash("Silme İşlemi Başarıyla Tamamlandı!","info")
            return redirect(url_for("dashboard"))
        else:
            flash("Yetkisiz İşlem!","danger")
            return redirect(url_for("index"))

    else:
        flash("Yetkisiz İşlem!","danger")
        return redirect(url_for("index"))


@app.route("/update/<string:id>", methods=["POST","GET"])
def update(id):
    if session:
        if request.method=="GET":

            cursor = mysql.connection.cursor()
            sorgu = "SELECT * FROM articles WHERE id=%s and author=%s"

            result = cursor.execute(sorgu,(id,session["username"]))

            if result>0:
                form = ArticleForm()

                article = cursor.fetchone()#bir tane makale düzenleyeceğimiz için fetchone yaptık
                form.title.data = article["title"]
                form.content.data = article["content"]

                return render_template("update.html",form=form)

            else:
                flash("Yetkisiz İşlem!","danger")
                return redirect(url_for("index"))
        else:
            form = ArticleForm((request.form))
            new_title = form.title.data
            new_content = form.content.data

            cursor = mysql.connection.cursor()

            update = "UPDATE articles SET title=%s, content=%s WHERE id=%s"

            cursor.execute(update, (new_title, new_content, id))

            mysql.connection.commit()

            cursor.close()

            flash("Makale Güncelleme İşlemi Başarılı!","info")
            return redirect(url_for("dashboard"))
            

    else:
        flash("Yetkisiz İşlem!","danger")
        return redirect(url_for("index"))





if __name__=="__main__":
    app.run(debug=True)