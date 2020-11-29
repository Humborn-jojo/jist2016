import os,json

from urllib.request import unquote

def scan_folder(directory, prefix=None, postfix=None):

    files_list = []

    #os.chdir(os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))) #进入上一级目录
    for root, sub_dirs, files in os.walk(directory):

        for special_file in files:

            if postfix:

                if special_file.endswith(postfix):

                    files_list.append(os.path.join(root, special_file))

            elif prefix:

                if special_file.startswith(prefix):

                    files_list.append(os.path.join(root, special_file))

            else:

                files_list.append(os.path.join(root, special_file))

    return files_list

def merge_synonym(synonym_folder,out_dir):

    f = open(out_dir, 'a', encoding='utf8')

    for file in scan_folder(synonym_folder):

        f_temp = open(file, 'r', encoding='utf8')

        data = f_temp.readline()

        f.write(data)

        while data:

            data = f_temp.readline()

            f.write(data)

        f_temp.close()

    f.close()

def build_conbined_file(baidubaike_synonym_path,baidubaike_entity_path,baidubaike_entity_synonym_file_savepath):
    # 读取同义词文件
    baidubaike_synonym_file = open(baidubaike_synonym_path, 'r', encoding='utf8')

    synonym_counter = 0

    baidubaike_synonym = []

    for line in baidubaike_synonym_file.readlines():
        synonym_counter += 1

        dict = {}

        line = line.strip('\n')

        split = line.split('> <')

        dict['entity'] = split[0]

        dict['synonym'] = split[1]

        baidubaike_synonym.append(dict)

    # 合并
    baidubaike_entity_synonym_file = open(baidubaike_entity_synonym_file_savepath, 'w', encoding='utf8')


    #输入路径为文件路径
    try:
        baidubaike_entity_file=open(baidubaike_entity_path, 'r', encoding='utf8')

        entity_list = json.load(baidubaike_entity_file)

        baidubaike_entity_file.close()

        for entity in entity_list:

            synonym = ''

            for d in baidubaike_synonym:

                if entity == d['entity']:
                    synonym = d['synonym']

                    break

            entity_synonym = '<' + unquote(entity) + '> <' + synonym + '>\n'

            baidubaike_entity_synonym_file.write(entity_synonym)

        baidubaike_entity_synonym_file.close()


    #输入路径为文件夹路径
    except:

        for file in scan_folder(baidubaike_entity_path):

            baidubaike_entity_file = open(file, 'r', encoding='utf8')

            entity_list = json.load(baidubaike_entity_file)

            baidubaike_entity_file.close()

            for entity in entity_list:

                synonym = ''

                for d in baidubaike_synonym:

                    if entity == d['entity']:
                        synonym = d['synonym']

                        break

                entity_synonym = '<' + unquote(entity) + '> <' + synonym + '>\n'

                baidubaike_entity_synonym_file.write(entity_synonym)

        baidubaike_entity_synonym_file.close()

if __name__ == "__main__":

    # step1 merge_synonym(synonym_folder,out_dir)
    # synonym_folder=''
    # out_dir=''

    # step2  build_conbined_file(baidubaike_synonym_path,baidubaike_entity_path,baidubaike_entity_synonym_file_savepath)
    # baidubaike_synonym_path=''
    # baidubaike_entity_path=''
    # baidubaike_entity_synonym_file_savepath=''



