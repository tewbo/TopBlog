import os
import io

from flask import Flask, render_template, request, Response, send_from_directory
from file_processor import process

os.environ["YC_FOLDER_ID"] = "b1g4ju1c9nnua4cubmtg"
os.environ[
    "YC_IAM"] = "t1.9euelZrIyZ6YyciJi5WWypeRxouene3rnpWak5THipCNy56enpaWj5XNkcjl8_d3RFRY-e9vTB1M_t3z9zdzUVj5729MHUz-zef1656Vmo-Qlp2ZnZ2em8_Im4-alprG7_zF656Vmo-Qlp2ZnZ2em8_Im4-alprG.iFdSknvGFBhltPdSQlE2jjTS7MslWUyAWsylg8v_yAgNFE8h6i-DvKoDKdtQbbCIVBDCwo3Fju_KVwz3Z-WZDg"

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
    app.run(debug=True)
