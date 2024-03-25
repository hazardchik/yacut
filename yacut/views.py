from flask import flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_URL
from .exceptions import ShortGenerateException
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            url=url_for(
                REDIRECT_URL,
                short=URLMap.create(
                    form.original_link.data, form.custom_id.data,
                ).short,
                _external=True
            )
        )
    except (ValueError, ShortGenerateException) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
