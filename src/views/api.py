#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint

bp_api = Blueprint('api', __name__, url_prefix='/api/')
