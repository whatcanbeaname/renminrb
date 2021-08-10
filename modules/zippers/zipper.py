import os
import zipfile

def zip_file(target_dir):
    if os.path.exists(target_dir) and os.listdir(target_dir) != []:
        output = target_dir + '.zip'
        z = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_name, file_names in os.walk(target_dir):
            f_path = dir_path.replace(target_dir, '')
            f_path = f_path and f_path + os.sep or ''
            for filename in file_names:
                z.write(os.path.join(dir_path, filename), f_path + filename)
        z.close()
