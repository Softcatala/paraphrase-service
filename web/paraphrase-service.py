#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2024 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from flask import Flask, request, Response
from flask_cors import CORS
import json
import os
import time
import logging
import logging.handlers


app = Flask(__name__)
CORS(app)
@app.route('/check', methods=['GET'])
def punctuation_api_get():
    return _punctuation_api(request.args)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"
  
def init():
    init_logging()



if __name__ == '__main__':
    app.debug = True
    init()
    app.run()
else:
    init()
