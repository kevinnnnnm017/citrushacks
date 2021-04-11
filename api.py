from flask import Flask, render_template, request, send_file
from createPDF import getPDF
from extractKeywords import extractWordsMethod
from keywordTest import getSummary
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/en.wikipedia.org/wiki/{name}')
def change():
    webbrowser.open('https://en.wikipedia.org/wiki/{name}')
    return redirect('/')


@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'POST':
        videoLink = request.form['videoURL']
        arr = extractWordsMethod(videoLink)
    else:
        print("ok")
        return redirect('/')
    sumArr = getSummary(videoLink)
    for i in sumArr:
        print("sum arr is " + i)
    pdff = getPDF(sumArr)
    send_file(pdff, attachment_filename=pdff)
    return render_template('keyTopic.html', new_array = arr, videoURL = videoLink)


# @app.route('/summary', methods=['POST'])
# def summary():
#     if request.method == 'POST':
#         print("video url is " + videoLink)
#         sumArr = getSummary(pyVideo)
#         getPDF(sumArr)
#         print("hi")
#     else:
#         return redirect('/')
#     return render_template('summary.html')

if __name__ == '__main__':
    app.run(debug=True)

