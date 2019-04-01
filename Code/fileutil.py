import dill


class FileUtil(object):

    def __init__(self, dest_dir, setup_name, max_quant_length, model_size):
        self.folderName = "{0}/{1}_length={2}_size={3}".format(dest_dir, setup_name, max_quant_length,model_size)

    def dump_dill(self, data, filename):
        with open('{0}/{1}'.format(self.folderName, filename), 'wb') as file:
            dill.dump(data, file)

    def load_dill(self,filename):
        with open('{0}/{1}'.format(self.folderName, filename), 'rb') as file:
            return dill.load(file)

    def save_stringlist(self, data, filename):
        with open('{0}/{1}'.format(self.folderName, filename), 'w') as file:
            for item in data:
                file.write('{0}\n'.format(item))