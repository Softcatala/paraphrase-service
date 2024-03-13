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

from flask import Flask
from flask_cors import CORS
import logging
import logging.handlers
import os
from inference import Inference

app = Flask(__name__)
CORS(app)


def init_logging():
    LOGDIR = os.environ.get("LOGDIR", "")
    LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
    logger = logging.getLogger()
    logfile = os.path.join(LOGDIR, "paraphrase-service.log")
    hdlr = logging.handlers.RotatingFileHandler(
        logfile, maxBytes=1024 * 1024, backupCount=1
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(LOGLEVEL)

    console = logging.StreamHandler()
    console.setLevel(LOGLEVEL)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)


def do_inference(sentence):
    model_name = decoding_params["model_name"]

    models_paths = os.environ.get("PARAPHRASE_MODELS", "/srv/models")
    model_path = os.path.join(models_paths, "outputs.exp209/")

    temperature = 1
    paraphrases, _ = Inference().get_paraphrases(model_path, sentence, temperature)
    return paraphrases


def json_answer(data, status=200):
    json_data = json.dumps(data, indent=4, separators=(",", ": "))
    resp = Response(json_data, mimetype="application/json", status=status)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


def _inference():
    text = values["text"]
    logging.debug(f"input text: '{text}'")
    paraphrases = do_inference(sentence)

    entries = []
    for paraphrase in paraphrases:
        entry = {}
        entry["type"] = "paraphrase"
        entry["proposal"] = paraphrase
        entries.append(entry)

    return json_answer(entries)


@app.route("/check", methods=["POST"])
def punctuation_api_post():
    return _inference(request.form)


@app.route("/check", methods=["GET"])
def punctuation_api_get():
    return _inference(request.args)


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello"


def init():
    init_logging()


if __name__ == "__main__":
    app.debug = True
    init()
    app.run()
else:
    init()
