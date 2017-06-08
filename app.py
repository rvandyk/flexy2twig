from flask import Flask, render_template, request
from twigparse import parse
import sys
import os
from tqdm import tqdm

if(len(sys.argv) == 4):
    if(sys.argv[1] == '-c'):
        topdir = sys.argv[2]
        exten = '.tpl'
        for dirpath, dirnames, files in os.walk(topdir):
            print("Folder found : " + dirpath)
            for name in tqdm(files):
                if name.lower().endswith(exten):
                    f_in = open(os.path.join(dirpath, name),'r')

                    if(not os.path.exists(sys.argv[3] +'/' + dirpath)):
                        os.makedirs(sys.argv[3] +'/' + dirpath)

                    f_out = open(sys.argv[3] +'/' + dirpath +'/'+name,'w')


                    f_out.write(parse(f_in.read()))
                    f_in.close()
                    f_out.close()

elif(len(sys.argv) == 2 and sys.argv[1] == '-s'):

    app = Flask(__name__)



    @app.route('/data', methods=["POST"])
    def data():
        flexy = str(request.form.get('flexycode'))
        print(flexy)

        parsed = parse(flexy)
        return render_template('cp.html', res=parsed, flex=flexy)


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/cp')
    def cp():
        return render_template('cp.html')


    if __name__ == '__main__':
        app.run(host='127.0.0.1',debug = True,port=80)
else:
    print('ERROR : incorrect arguments')
    print('-s                           : server mode')
    print('-c [in_folder] [out_folder]  : recursive console mode')
