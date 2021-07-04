# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, abort
import base64
import tempfile
from PIL import Image
import io
import numpy as np
import cv2

app = Flask(__name__)


def kuwahara(pic, r=5, resize=False, rate=0.5):
    h, w, _ = pic.shape
    if resize:
        pic = cv2.resize(pic, (int(w*rate), int(h*rate)))
        h, w, _ = pic.shape
    pic = np.pad(pic, ((r, r), (r, r), (0, 0)), "edge")
    ave, var = cv2.integral2(pic)
    ave = (ave[:-r-1, :-r-1]+ave[r+1:, r+1:]-ave[r+1:, :-r-1] -
           ave[:-r-1, r+1:])/(r+1)**2
    var = ((var[:-r-1, :-r-1]+var[r+1:, r+1:]-var[r+1:, :-r-1] -
           var[:-r-1, r+1:])/(r+1)**2-ave**2).sum(axis=2)

    def filt(i, j):
        return np.array([ave[i, j], ave[i+r, j], ave[i, j+r], ave[i+r, j+r]])[(np.array([var[i, j], var[i+r, j], var[i, j+r], var[i+r, j+r]]).argmin(axis=0).flatten(), j.flatten(), i.flatten())].reshape(w, h, _).transpose(1, 0, 2)
    filtered_pic = filt(
        *np.meshgrid(np.arange(h), np.arange(w))).astype(pic.dtype)  # 色の決定
    return filtered_pic


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":

        f = request.files["file"]
        filepath = tempfile.mkdtemp()+"/a.png"

        f.save(filepath)
        image = Image.open(filepath)

        image = np.asarray(image)
        filtered = kuwahara(image, r=7)
        filtered = Image.fromarray(filtered)

        buffer = io.BytesIO()
        filtered.save(buffer, format="PNG")
        img_string = base64.b64encode(
            buffer.getvalue()).decode().replace("'", "")

        result = "image size {}×{}".format(len(image[0]), len(image))
        return render_template("index.html", filepath=filepath, result=result, img_data=img_string)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
