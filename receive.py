import zipfile
import os, glob, base64, pickle

module_path = os.path.dirname(__file__)
path_input = os.path.join(module_path, 'input')
path_output = os.path.join(module_path, 'output')
_obj_file = '__init__.cpython-38.pyc'


def ensure_directory(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print('Directory created successfully.')
        except OSError as e:
            print(f'Failed to create directory: {e}')

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
            _zipfile = file
    print("zipfile: ", _zipfile)

    if _zipfile is None:
        raise Exception("************* No Zip file ! ***************")

    with zipfile.ZipFile(_zipfile, 'r') as zf:
        a= zf.open(_obj_file)
        my_infos = pickle.load(a)
        for my_info in my_infos:
            my_info['descript'] = my_info['descript'].decode('utf-8')
            my_info['name'] = my_info['name'].decode('utf-8')
            my_info['model'] = base64.b64decode(my_info['model'])
            print("output:  ", my_info['name'])
            with open(os.path.join(path_output, my_info['name']), 'wb') as f:
                f.write(my_info['model'])

    print("====================== finished ========================")