#---------------------------------------------#
#   运行前一定要修改classes
#   如果生成的2007_train.txt里面没有目标信息
#   那么就是因为classes没有设定正确
#---------------------------------------------#
import xml.etree.ElementTree as ET
from os import getcwd

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
#-----------------------------------------------------#
#   这里设定的classes顺序要和model_data里的txt一样
#-----------------------------------------------------#
classes = ["吊纬", "毛斑", "扎洞", "normal", "边白印", "边缺纬", "边扎洞", "边针眼", "擦洞", "擦毛", "擦伤", "粗纱", "吊弓", "吊经", "耳朵", "弓纱", "厚薄段", "黄渍", "回边", "剪洞","结洞","紧纱","经粗纱","经跳花","楞断","毛斑","毛洞","毛粒","破边","破洞","嵌结","缺经","缺纬","跳花","纬粗纱","污渍","线印","修印","油渍","扎洞","扎纱","扎梳","蒸呢印","织入","织稀","边缺经","明嵌线","厚段"]

def convert_annotation(year, image_id, list_file):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id), encoding='utf-8')
    tree=ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        difficult = 0 
        if obj.find('difficult') == None:
            cls_id=3
            list_file.write(" "+"11,3,2560,1912,"+str(cls_id))
            continue
        if obj.find('difficult')!=None:
            difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set), encoding='utf-8').read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w', encoding='utf-8')
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(wd, year, image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()
