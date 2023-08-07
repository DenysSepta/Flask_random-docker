from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import names
import random

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql_random.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Randoms (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable =False)
    random_num = db.Column(db.String(200),default= str(random.randint(0,9999999)))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/', methods=['POST','GET'])
def index():
     

    if request.method == 'POST':
        
        num_content  = request.form['content']
        
        new_number = Randoms(content=num_content,random_num=str(random.randint(0,9999999)))

        try:
            db.session.add(new_number)
            db.session.commit()
            
            return redirect('/')
        except:
            return 'There was an issue during update of DB'
        

    else:
        
        num_content  = names.get_full_name()
        new_number = Randoms(content=num_content,random_num=str(random.randint(0,9999999)))

        try:
            db.session.add(new_number)
            db.session.commit()
            
        except:
            return 'There was an issue during update of DB'
        
        numbers= Randoms.query. order_by(desc(Randoms.date_created)).all()
        top_num = Randoms.query. order_by(desc(Randoms.date_created)).first()
        return render_template('index.html', numbers=numbers, top_num = top_num)
        


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="0.0.0.0" , port=5000)
