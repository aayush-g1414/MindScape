# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def index():
    return jsonify({
        "message": "hello!"
    })
