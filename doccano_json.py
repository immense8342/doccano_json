

def generate_json():
    '''将标注系统下载下来的文件转换为标准json格式'''
    f1 = open('out.jsonl', 'w', encoding='utf-8')
    f1.write("[")
    with open('project_last_dataset2.jsonl', 'r', encoding='utf-8')as f2:
        lines = f2.readlines()
        k = len(lines)
        i = 0
        while i < k-2:
            #strip() 去掉首位指定字符
            f1.write(lines[i].strip() + ',\n')
            i += 1
        f1.write(lines[i].strip() + '\n')
    f1.write(']')
    f1.close()

#generate_json()




import json

def tranfer2bio(method='BIO'):
    '''
    将json文件中的数据转录为BIO形式
    method 标记方法
    :return:
    '''
    f1 = open('./train.txt', 'w', encoding='utf-8')
    with open("./out.jsonl", 'r', encoding='utf-8') as inf:
        load = json.load(inf)
        if method == 'BIO':
            for i in range(len(load)):
                #一次处理一行数据
                labels = load[i]['labels']
                text = load[i]['text']
                #先将所有字符设为‘0’
                tags = ['O'] * len(text)
                # 处理每一个label
                for j in range(len(labels)):
                    label = labels[j]
                    #print(label)
                    tags[label[0]] = 'B-' + str(label[2])
                    k = label[0]+1
                    while k < label[1]:
                        tags[k] = 'I-' + str(label[2])
                        k += 1
                print(tags)
                for word, tag in zip(text, tags):
                    f1.write(word + '\t' + tag + '\n')
                f1.write("\n")
        elif method == 'BIOES':
            for i in range(len(load)):
                #一次处理一行数据
                labels = load[i]['labels']
                text = load[i]['text']
                #先将所有字符设为‘0’
                tags = ['O'] * len(text)
                #处理每一个label
                for j in range(len(labels)):
                    label = labels[j]
                    #print(label)
                    #检查label长度
                    if len(label[2]) == 1:
                        tags[label[0]] = 'S'
                    elif 1 < len(label[2]) <= 2:
                        tags[label[0]] = 'B-' + str(label[2])
                        tags[label[0]+1] = 'E-' + str(label[2])
                    elif len(label[2]) > 2:
                        tags[label[0]] = 'B-' + str(label[2])
                        k = label[0]+1
                        while k < label[1]-1:
                            tags[k] = 'I-' + str(label[2])
                            k += 1
                        tags[k] = 'E-' + str(label[2])
                print(tags)
                for word, tag in zip(text, tags):
                    f1.write(word + '\t' + tag + '\n')
                f1.write("\n")
        else:
            print('输入错误')


tranfer2bio(method = 'BIOES')