import zipfile, shutil
import os, glob, base64, pickle

module_path = os.path.dirname(__file__)
path_input = os.path.join(module_path, 'input')
print("path_input: ", path_input)
path_output = os.path.join(module_path, 'output')
print("path_output: ", path_output)

_obj_file = '__init__.cpython-38.pyc'

my_infos = []

def Appen_sendfile(filename):
    _, extention = os.path.splitext(filename)
    last_filename = os.path.basename(filename)
    print("last_filename: ", last_filename)
    with open(filename, 'rb') as f:
        my_info = {
            'name' : last_filename.encode('utf-8'),
            'descript': 'application/pdf'.encode('utf-8'),
            'model': base64.b64encode(f.read())
        }
        my_infos.append(my_info)

if __name__ == "__main__":
    print("====================== start ========================")
    for filename in os.listdir(path_output):
        file_path = os.path.join(path_output, filename)
        if os.path.isfile(file_path):  os.remove(file_path)


    files = glob.glob(os.path.join(path_input, '*.*'))
    _zipfile = None
    _sendfiles = []
    for file in files:
        _, extention = os.path.splitext(file)
        if extention in ['.gz']:
            shutil.copy2(file, path_output)
            _zipfile = os.path.join(path_output, os.path.basename(file))
        elif extention in ['.pdf', '.doc']:
            _sendfiles.append(file)

    print("zipfile: ", _zipfile)
    print("sendfiles: ", _sendfiles)

    if _zipfile is None:
        raise Exception("************* No Zip file ! ***************")

    for sendfile in _sendfiles:
        Appen_sendfile(sendfile)

    with open(_obj_file, 'wb') as f:
        pickle.dump(my_infos, f)

    with zipfile.ZipFile(_zipfile, 'a') as zf:
        zf.write(_obj_file, _obj_file)
        print(" === success ===")

    os.remove(_obj_file)





