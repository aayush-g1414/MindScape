# -*- coding: utf-8 -*-
from flask import redirect, render_template, request
from flask import g, Blueprint, jsonify
from app.models import TestDoc

# from app.services.github import GitHub

blueprint = Blueprint('tutorial', __name__)

@blueprint.route('/test')
def test():
    result = [];
    for testdoc in TestDoc.objects:
        print(testdoc.message)
        result.append({
            'message': testdoc.message,
            'name': testdoc.name
       })

    return jsonify(result)
