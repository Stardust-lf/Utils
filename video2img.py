import os
from PIL import Image
import numpy as np


def cut_image(path,cut_path,size):
    '''
    剪切图片
    :param path: 输入图片路径
    :param cut_path: 剪切图片后的输出路径
    :param size: 要剪切的图片大小
    :return:
    '''
    for (root,dirs,files) in os.walk(path):
        temp = root.replace(path,cut_path)
        if not os.path.exists(temp):
            os.makedirs(temp)
        for file in files:
            image,flag = cut(Image.open(os.path.join(root,file)))
            if not flag: Image.fromarray(image).convert('L').resize((size[1],size[0])).save(os.path.join(temp,file))

    pass
def cut(image):
    '''
    以重心为中心合成GEI
    通过找到人的最小最大高度与宽度把人的轮廓分割出来，、
    因为原始轮廓图为二值图，因此头顶为将二值图像列相加后，形成一列后第一个像素值不为0的索引。
    同理脚底为形成一列后最后一个像素值不为0的索引。
    人的宽度也同理。
    :param image: 需要裁剪的图片 N*M的矩阵
    :return: temp:裁剪后的图片 size*size的矩阵。flag：是否是符合要求的图片
    '''
    image = np.array(image)
    # 找到人的最小最大高度与宽度
    height_min = (image.sum(axis=1)!=0).argmax()
    height_max = ((image.sum(axis=1)!=0).cumsum()).argmax()
    width_min = (image.sum(axis=0)!=0).argmax()
    width_max = ((image.sum(axis=0)!=0).cumsum()).argmax()
    head_top = image[height_min,:].argmax()
    # 设置切割后图片的大小，为size*size，因为人的高一般都会大于宽
    size=height_max-height_min
    temp = np.zeros((size,size))
    #计算质心
    N = np.sum(image!=0)
    Xy = 0
    for i in range(image.shape[0]):
        Xy += np.sum(image[i,:]!=0)*i
    Xy = Xy//N
    Xc = 0
    for i in range(image.shape[1]):
        Xc += np.sum(image[:, i] != 0) * i
    Xc = Xc // N
    centroid = (Xc,Xy)
    l1 = Xc-int(size*11/16/2)
    r1 = Xc+int(size*11/16/2)
    # 若宽大于高，或头的左侧或右侧身子比要生成图片的一般要大。则此图片为不符合要求的图片
    flag = False
    if l1>width_min or l1<0 or r1<width_max or r1>image.shape[1]:
        flag = True
        return temp,flag
    # centroid = np.array([(width_max+width_min)/2,(height_max+height_min)/2],dtype='int')
    #temp[:,(size//2-l1):(size//2+r1)] = image[height_min:height_max,width_min:width_max ]
    temp = image[height_min:height_max,l1:r1]
    #print((r1-l1)/size,temp.shape[1]/temp.shape[0],11/16)
    #若图片像素值过少，则图片也不合格
    print(image.sum())
    if image.sum()<5000:
        flag = False
    return temp,flag

def GEI(cut_path,data_path,size,batch=None,strides=None):
    '''
    生成步态能量图，若batch或strides为None则将整个序列合成一GEI
    :param cut_path: 剪切后的图片路径
    :param data_path: 生成图片的路径
    :param size: 生成能量图大小
    :param batch: 多少张图片合成一张步态能量图
    :param strides: 合成GEI的步长
    :return:
    '''
    for (root,dirs,files) in os.walk(cut_path):
        temp = root.replace(cut_path,data_path)
        if not os.path.exists(temp):
            os.makedirs(temp)
        if batch==None or strides==None:
            batch_ = len(files)
            strides_ = len(files)
        else:
            batch_ = batch
            strides_ = strides
        #图片多余10张才生成GEI
        if len(files)>10:
            print(len(files))
            files.sort()
            k = len(os.listdir(temp))
            for i in range(0,len(files),strides_):
                if i+batch_>len(files):
                    break
                GEI = np.zeros(size)
                for file in files[i:i+batch_]:
                    GEI += Image.open(os.path.join(root, file)).convert('L')
                GEI /= batch_
                Image.fromarray(GEI).convert('L').save(os.path.join(temp, str(k)+'.png'))
                k += 1
    pass

cut_image(r'C:\Users\StarDust\Desktop\cutImage\GaitDatasetA-silh\fyc\00_1',r'C:\Users\StarDust\Desktop\movedImage',(240,352))
GEI(r'C:\Users\StarDust\Desktop\movedImage',r'C:\Users\StarDust\Desktop\energyImage\energy1.jpg',(240,352))