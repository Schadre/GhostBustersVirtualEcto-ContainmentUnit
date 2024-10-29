from flask import render_template
from app import app 
from app.forms import LoginForm

@app.route('/')
@app.route('/VirtualEcto-ContainmenUnit')
def VirtualEctoContainmenUnit():
    return render_template('VirtualEcto-ContainmenUnit.html')

@app.route('/adminlogin')
def adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('VirtualEcto-ContainmenUnit.html')
    return render_template('login.html', form=form)

