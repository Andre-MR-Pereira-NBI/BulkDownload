import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import shutil

dir = './DocsExtracted/'
zipped_dir = './ZipDocsExtracted'

class FileUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            doc_name = self.headers.get('Name', 'temp')
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            file_path = os.path.join(os.getcwd(), dir + doc_name)
            with open(file_path, 'wb') as f:
                decoded_data = base64.b64decode(post_data)
                f.write(decoded_data)
            self.send_response(201)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'filePath': file_path}), 'utf8'))
        except:
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'filePath': file_path}), 'utf8'))
    def do_GET(self):
        try:
            shutil.make_archive(zipped_dir, 'zip', dir)
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'filePath': zipped_dir}), 'utf8'))
        except:
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'filePath': zipped_dir}), 'utf8'))

if __name__ == '__main__':
    with HTTPServer(('', 3000), FileUploadHandler) as server:
      print('Starting HTTP server...')
      server.serve_forever()