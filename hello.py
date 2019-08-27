# coding: utf-8
from tornado.ioloop import IOLoop
from tornado import web
import shutil
import os
import json

import pwd


class FileUploadHandler(web.RequestHandler):
    def get(self):
        self.write('''
            <html>
              <head><title>Upload File</title></head>
              <body>
                <form action='/file' enctype="multipart/form-data" method='post'>
                <input type='file' name='file'/><br/>
                <input type='submit' value='submit'/>
                <a href='/static/biye.jpg'>biye</a>
                <a href='/static/haha.jpg'>haha</a>
                <a href='/static/single.jpeg'>single</a>
                </form>
              </body>
            </html>
            ''')

    def post(self):
        ret = {'result': 'OK'}
        upload_path = os.path.dirname(__file__) # 文件的暂存路径
        print("1 file"+__file__)
        print("2 upload_path"+upload_path)
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据

        if not file_metas:
            ret['result'] = 'Invalid Args'
        else:
            for meta in file_metas:
            	# print(meta)
                filename = meta['filename']
                file_path = os.path.join(upload_path, filename)
                print("3 file "+file_path)
                with open(file_path, 'wb') as up:
                    up.write(meta['body'])
                    # OR do other thing

        self.write(json.dumps(ret))

class DownloadHandler(web.RequestHandler):
    def get(self, filename):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
 
        path = os.path.join('./static', filename)
        print("4path"+path)
        with open( path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
 
        self.finish()

application = web.Application([
    (r'/file', FileUploadHandler),
    (r'/static/(.*)', DownloadHandler),
    ],autoreload = True)
application.listen(8888)
IOLoop.current().start()
