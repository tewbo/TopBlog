import os
import io

from flask import Flask, render_template, request, Response, send_from_directory
from file_processor import process

os.environ["YC_FOLDER_ID"] = "b1gm0h08vu8cjto5c7sa"
os.environ["YC_IAM"] = "t1.9euelZrOnZyNyYmSnJPPlMaWypKPxu3rnpWax5SSmYyQlIqSy8jKz46cy5jl8_d7Yw1R-e9TEB4j_N3z9zsSC1H571MQHiP8zef1656Vmo2bnoucy56YxpiXy8-axomd7_zF656Vmo2bnoucy56YxpiXy8-axomd.37xTAMhoxpkLWOzUmzfglTKIUcwvQfDWSy4Omc4HeR3MrGWjfA_ROxEr5yCOnyOQe3jstnkEc71urCMRnJA-BQ"

app = Flask(__name__)


# Определение маршрута для главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Получаем загруженный файл из формы
        uploaded_file = request.files['file']
        selected_option = request.form['option']  # Получаем выбранный вариант

        if uploaded_file.filename != '':
            # Обрабатываем файл как вам нужно
            # Например, просто читаем содержимое файла и возвращаем его
            table_name = process(uploaded_file, selected_option)
            # result = uploaded_file.read().decode('utf-8')
            # result = f"Выбранный вариант: {selected_option}\n\nПолученное значение: {parsed}\n"
            output = io.BytesIO()
            with open(table_name, "rb") as table:
                output.write(table.read())
            output.seek(0)

            # Возвращаем файл для скачивания
            return Response(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment;filename={table_name}"}
            )

    return render_template('index.html', result=result)


@app.route('/css/style.css')
def css():
    return send_from_directory('css', 'style.css')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
