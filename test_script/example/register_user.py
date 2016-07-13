form wtforms import Form, TextField, BooleanField, validators

class RegistUserForm(Form):
	firstname = TextField('firstname', [validators.Length(min=2, max=25)])
	lastname = TextField('lastname'), [validators.Length(min=2, max=35)])
	nickname = TextField('nickname'), [validators.Length(min=3, max=50)])
	email = TextField('emailaddr'), [validators.Length(min=6, max=50)])
	accept_rules = BooleanField(''), [validators.Required()]

@app.route('/test_wtforms', methods = ['GET', 'POST'])
def RegistUser():
	form = RegistUserForm(request.POST)
	if request.method == 'POST' and form.validate():
        return redirect(url_for('show_entries'))

    return render_response('test_wtforms.html', form=form)
