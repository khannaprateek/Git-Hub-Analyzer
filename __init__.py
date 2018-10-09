from flask import Flask, render_template, session, redirect, url_for ,request, flash
from forms import LoginForm
from flask_login import login_required, LoginManager
import requests
login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = '7dd8816386bd78dabf1ef0715308c002'



userUrl = 'https://api.github.com/user'
repoUrl = 'https://api.github.com/repos'

@app.route('/login',methods=['GET','POST'])
def login():
    login = LoginForm()
    
    if request.method=='POST':
        
        session['username'] = login.username.data
        session['password'] = login.password.data
        
        session['user'] = requests.get(userUrl, auth=(session['username'], session['password'])).json()
        
        repoInfo=requests.get(session['user']['repos_url'], auth=(session['username'], session['password'])).json()
        no = []
        repoName = []
        repoForks = []
        repoClones = []
        repoViews = []
        user={}
        count=0
        for data in repoInfo:
            no.append(count)
            repoName.append(data['name'])
            repoForks.append(data['forks'])
            a=requests.get(repoUrl+'/'+session['user']['login']+'/'+ data['name'] + '/traffic/clones',auth=(session['username'], session['password'])).json()
            repoClones.append(a)
            a=requests.get(repoUrl+'/'+session['user']['login']+'/'+ data['name'] + '/traffic/views',auth=(session['username'], session['password'])).json()
            repoViews.append(a)
            count+=1
        user['no']=no
        user['name']=repoName
        user['forks']=repoForks
        user['clones']=repoClones
        user['clones']=repoClones
        user['view']=repoViews            
        session['log']=True 
        session['u']= user
        flash('You are loged in')
        
#        next = request.args.get('next')
#            
#        if next == None or not next[0]=='/':
#            next = url_for('status')
        return redirect(url_for('status'))
    return render_template('login.html', form=login)

#Pass our app to login manager
login_manager.init_app(app)

#Tell the user which view to go when they need to login 
login_manager.login_view= 'login'

@app.route('/status')
def status():
    return render_template('status.html')
@app.route('/plot')
def plot():
#    next = request.args.get('next')
#    if next == None or not next[0]=='/':
#        next = url_for('plot')
#        return redirect(next)
    return render_template('plot.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout user')
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)