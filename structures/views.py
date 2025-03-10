from app import app
from flask import render_template
from models import get_all_buildings


@app.route('/')
def index():

    [buildings_head, buildings_body] = get_all_buildings()

    html = render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )

    return html