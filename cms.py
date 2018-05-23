from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////run/media/yek/yek/mos/cms.db'
db = SQLAlchemy(app)



@app.route("/")
def index():

	return render_template('index.html')


@app.route("/musteribilgileri")
def musteriBilgileri():

    mus =  Musteri.query.all()

    return render_template("musteribilgileri.html",mus = mus)

@app.route("/delete/<string:id>")
def delete(id):
    veri = Musteri.query.filter_by(id=id).first()

    db.session.delete(veri)
    
    db.session.commit()

    return redirect(url_for('musteriBilgileri'))



@app.route("/stokdelete/<string:id>")
def stokdelete(id):
    veri = Stok.query.filter_by(id=id).first()

    db.session.delete(veri)
    
    db.session.commit()

    return redirect(url_for('stok'))

@app.route("/musteriekle")
def musteriekle():

    return render_template("musteriekle.html")

@app.route("/musteriduzenle/<string:id>")
def musteriduzenle(id):

    mus = Musteri.query.filter_by(id=id).first()


    return  render_template("musteriduzenle.html",mus = mus)

@app.route("/stokduzenle/<string:id>")
def stokduzenle(id):

    mus = Stok.query.filter_by(id=id).first()


    return  render_template("stokduzenle.html",mus = mus)

@app.route("/yenistok")
def yenistok():




    return  render_template("yenistok.html")




@app.route("/add",methods = ["POST"])
def addMusteri():


    musteri_ad = request.form.get("musteriisim")
    
    musteri_soyad = request.form.get("musterisoyisim")

    musteri_adres = request.form.get("musteriadres")
    
    musteri_no = request.form.get("musteritelefon")
    
    m_urun = request.form.get("musteriurun")
    
    musteri_mail = request.form.get("musteriemail")
    
    siparis_tarih = request.form.get("uruntarih")
     
    newMusteri = Musteri(musteri_ad = musteri_ad,musteri_soyad = musteri_soyad,musteri_no = musteri_no , musteri_adres = musteri_adres, m_urun = m_urun , musteri_mail = musteri_mail , siparis_tarih  = siparis_tarih)


    db.session.add(newMusteri)
                
    db.session.commit()

    return redirect(url_for('musteriBilgileri'))



@app.route("/edit",methods = ["POST"])
def edit():

    id = request.form.get("mid")

    item = Musteri.query.get(id)

    
    item.musteri_ad = request.form.get("musteriisim")
    
    item.musteri_soyad = request.form.get("musterisoyisim")

    item.musteri_adres = request.form.get("musteriadres")
    
    item.musteri_no = request.form.get("musteritelefon")
    
    item.m_urun = request.form.get("musteriurun")
    
    item.musteri_mail = request.form.get("musteriemail")
    
    item.siparis_tarih = request.form.get("uruntarih")

    db.session.commit()
    
    return redirect(url_for('musteriBilgileri'))

@app.route("/stokedit",methods = ["POST"])
def stokedit():

    id = request.form.get("mid")

    item = Stok.query.get(id)

    
    item.stok_adi = request.form.get("stok_adi")
    
    item.tedarikci_adi = request.form.get("tedarikci_adi")

    item.urun_adeti = request.form.get("urun_adeti")
    
    item.tedarik_tarihi = request.form.get("tedarik_tarihi")

    db.session.commit()
    
    return redirect(url_for('stok'))

@app.route("/stok")
def stok():


    stok =  Stok.query.all()

    return render_template("stokyonetimi.html",stok = stok)


@app.route("/stokadd",methods = ["POST"])
def addStok():


    stok_adi = request.form.get("stok_adi")
    
    tedarikci_adi = request.form.get("tedarikci_adi")

    tedarik_tarihi = request.form.get("tedarik_tarihi")
    
    urun_adeti = request.form.get("urun_adeti")
    
    newStok = Stok(stok_adi = stok_adi,tedarikci_adi = tedarikci_adi,tedarik_tarihi = tedarik_tarihi , urun_adeti = urun_adeti)


    db.session.add(newStok)
                
    db.session.commit()

    return redirect(url_for('stok'))




class Musteri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    musteri_ad = db.Column(db.String(50), nullable=False)
    musteri_soyad = db.Column(db.String(50), nullable=False)
    musteri_no = db.Column(db.String(11), nullable=False)
    musteri_adres = db.Column(db.String(250), nullable=False)

     #  stok_adi ile bağlantili
     
    m_urun = db.Column(db.String, db.ForeignKey('stok.stok_adi'),
        nullable=False)
    	#
    musteri_mail = db.Column(db.String(50), nullable=False)
    siparis_tarih = db.Column(db.String(10), nullable=False)



class Stok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stok_adi = db.Column(db.String(50), nullable=False)
    tedarikci_adi = db.Column(db.String(50), nullable=False)
    tedarik_tarihi = db.Column(db.String(50), nullable=False)
    urun_adeti = db.Column(db.Integer, nullable=False)
    stoklar = db.relationship('Musteri', backref='stok', lazy=True)



if __name__ == "__main__":
    app.run(debug=True)


