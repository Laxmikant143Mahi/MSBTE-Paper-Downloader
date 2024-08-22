from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit-form", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    college = request.form.get("college")
    place = request.form.get("place")
    return render_template("index2.html", name=name, mobile=mobile, college=college, place=place)


@app.route("/download-paper", methods=["POST"])
def download_paper():
    paper_type = request.form.get("paperType")
    subject_code = request.form.get("subjectCode")
    year = request.form.get("year")

    year_code = year

    if paper_type == "question":
        url = f"https://msbte.org.in/portal/msbte_files/questionpaper_search/{year_code}/{subject_code}.pdf"
        file_name = f"{year_code}-{subject_code}-question_paper.pdf"
    elif paper_type == "answer":
        url = f"https://msbte.org.in/portal/model-answer-search/{year_code}/{subject_code}.pdf"
        file_name = f"{year_code}-{subject_code}-answer_paper.pdf"
    else:
        print("Invalid paper type entered")
        return

    # download the file and save it to the directory
    response = requests.get(url, stream=True)
    block_size = 1024
    file_path = os.path.join(download_dir, file_name)
    with open(file_path, 'wb') as f:
        for data in response.iter_content(block_size):
            f.write(data)

    # check if the downloaded file is empty
    if os.stat(file_path).st_size == 68:
        os.remove(file_path)
        return "<b><i><h1>Oops Sorry!!! Paper code for that year is not available</h1></i></b>"

    return "<b><i><h1>File downloaded successfully!</h1></i></b>"


if __name__ == "__main__":
    app.run(debug=True)
