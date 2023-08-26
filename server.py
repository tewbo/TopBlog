import os
import sys
import cgi
from http.server import HTTPServer, SimpleHTTPRequestHandler

from PIL import Image

import dzen
from utils import error

# from database.database import create_table, insert_record, fetch_records


HOST_NAME = "localhost"
PORT = 8080

def read_html_template(path):
    """function to read HTML file"""
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

# def show_records(self):
#     """function to show records in template"""
#     file = read_html_template(self.path)
#     # fetch records from database
#     table_data = fetch_records()
#     table_row = ""
#     for data in table_data:
#         table_row += "<tr>"
#         for item in data:
#             table_row += "<td>"
#             table_row += item
#             table_row += "</td>"
#         table_row += "</tr>"
#     # replace {{user_records}} in template by table_row
#     file = file.replace("{{user_records}}", table_row)
#     self.send_response(200, "OK")
#     self.end_headers()
#     self.wfile.write(bytes(file, "utf-8"))

class PythonServer(SimpleHTTPRequestHandler):
    """Python HTTP Server that handles GET and POST requests"""
    def do_GET(self):
        if self.path == '/':
            self.path = './form.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

    def do_POST(self):
        if self.path == '/':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'})

            self.send_response(200)
            self.end_headers()

            saved_fns = ""

            # try:
            files = form['files']
            files = files if isinstance(files, list) else [ files ]
            files2 = []
            imgs = []
            for f in files:
                try:
                    imgs.append(Image.open(f.file))
                    files2.append(f)
                except:
                    pass
            files = files2
            result = dzen.process(imgs, folder_id, iam)
            answer = list(zip(map(str, result), map(lambda x: x.filename, files)))
            answer_string = "\n".join(map(" ".join, answer))
            self.wfile.write(answer_string.encode())
                # return (True, "File(s) '%s' upload success!" % saved_fns)
            # except IOError:
            #     pass
                # return (False, "Can't create file to write, do you have permission to write?")


if __name__ == "__main__":
    folder_id = os.getenv('YC_FOLDER_ID')
    if not folder_id:
        error("YC_FOLDER_ID variable must be set")

    iam = os.getenv('YC_IAM')
    if not iam:
        error("YC_IAM variable must be set")

    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Server started http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)