"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from .forms import PropertyForm
from app.models import Property


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/properties')
def properties():
    """Render page for displaying list of all properties."""
    # results = Property.query.all()
    results = db.session.query(Property).all()

    properties = [{
        "id": r.id,
        "title": r.prop_title,
        "desc": r.prop_desc,
        "room_count": r.prop_room_count,
        "bathroom_count": r.prop_bathroom_count,
        "price": r.prop_price,
        "type": r.prop_type,
        "location": r.prop_location,
        "photo": r.prop_photo,
    } for r in results]

    return render_template('properties.html', properties=properties)


@app.route('/uploads/<string:filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'][0:]), filename)


@app.route('/properties/create', methods=["GET", "POST"])
def create_property():
    """Render form for adding a new property."""
    form = PropertyForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            prop_photo = form.photo.data
            photo_filename = secure_filename(prop_photo.filename)
            prop_photo.save(os.path.join(
                os.environ.get('UPLOAD_FOLDER'), photo_filename
            ))

            prop = Property(
                prop_title=form.title.data,
                prop_desc=form.desc.data,
                prop_room_count=form.room_count.data,
                prop_bathroom_count=form.bathroom_count.data,
                prop_price=form.price.data,
                prop_type=form.type.data,
                prop_location=form.location.data,
                prop_photo=photo_filename
            )
            db.session.add(prop)
            db.session.commit()

            flash('New property added successfully', 'success')
            return redirect(url_for('properties'))

    return render_template('create_property.html', form=form)


@ app.route('/properties/<propertyid>')
def property(propertyid):
    """Render page for displaying a single property."""
    #prop = Property.query.get(int(propertyid))
    prop = db.session.query(Property).get(int(propertyid))

    return render_template('property.html', prop=prop)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@ app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@ app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@ app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
