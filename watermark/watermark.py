''' 
批量给图片增加时间水印的Python脚本程序【目前测试为Mac OS X下的jpeg文件】。
遍历指定目录的照片文件，根据拍照时间给照片在右下角添加时间和地点的水印。


！该程序需要安装exifread，PIL，requests等模块，否则无法使用。
例如，Linux/Mac OS X下命令行安装该模块：sudo pip install exifread

！该程序需要加baidu api的secret_key（在getLocationBy_lat_lng函数中）；
！该程序可以手动调整字体大小（size），字体位置（d_width,d_height）和字体填充颜色（fillcolor）（在add_watermark函数中）。

获取拍照时间 From 'https://www.racksam.com/2014/05/14/python-script-to-change-pictures-filenames/'
拍照地点 参考 http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding-abroad
watermark 参考 https://blog.csdn.net/weixin_30561177/article/details/97609897 
orientation 参考 https://blog.csdn.net/mizhenpeng/article/details/82794112
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os
import stat
import time
import math
import exifread
from PIL import Image, ImageDraw, ImageFont, ExifTags
import requests
import json

'=================分割线==================='
# 创建文件夹
def mymkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

# 判断是否是支持的文件类型
SUFFIX_FILTER = ['.jpg','.png','.mpg','.mp4','.thm','.bmp','.jpeg','.avi','.mov'] # 仅测试了jpeg，jpg
def isTargetedFileType(filename):
    '根据文件扩展名，判断是否是需要处理的文件类型；仅支持x.x格式'
    filename_nopath = os.path.basename(filename)
    f,e = os.path.splitext(filename_nopath)
    if e.lower() in SUFFIX_FILTER:
        return True
    else:
        return False

# 新文件的名字
def get_new_filename(filename):
    f, e= filename.split('.')
    return "%s_watermark.%s" % (f, e)

'=================分割线==================='

'=================begin{得到照片的拍摄时间}==================='
def getPhotoTime(filename):
    '''得到照片的拍照时间（如果获取不到拍照时间，则使用文件的创建时间）
    '''
    try:
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
        else:
            raise "[%s] is not a file!\n" % filename
    except:
        raise "unopen file[%s]\n" % filename
        
    #默认用图像文件的创建日期作为拍摄日期（如果有照片的拍摄日期，则修改为拍摄日期
    state = os.stat(filename)
    dateStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(state[-2]))

    data = exifread.process_file( fd )
    if data: #取得照片的拍摄日期，改为拍摄日期
        try:
            t = data['EXIF DateTimeOriginal'] #转换成 yyyy-mm-dd_hh:mm:ss的格式
            dateStr = str(t).replace(":","-")[:10] + str(t)[10:]
        except:
            pass

    return dateStr
'=================end{得到照片的拍摄时间}==================='


'=================begin{得到照片的拍摄地点}==================='
def format_lat_lng(data):
    '将exif得到的经纬度转化成数值， 这个有点笨重'
    list_tmp=str(data).replace('[', '').replace(']', '').split(',')
    l= [ele.strip() for ele in list_tmp]
    data_sec = int(l[-1].split('/')[0]) /(int(l[-1].split('/')[1])*3600)# 秒的值
    data_minute = int(l[1])/60
    data_degree = int(l[0])
    result=data_degree + data_minute + data_sec
    return result

def getLocationBy_lat_lng(lat, lng):
    """
    使用Geocoding API把经纬度坐标转换为结构化地址。需要注册baidu map api的key
    """
    secret_key = 'XXXXX你得ak密钥'  # 请修改这里
    
    # 使用说明http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding-abroad
    baidu_map_api = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak={0}&output=json&coordtype=wgs84ll&location={1},{2}'.format(
        secret_key, lat, lng)
    response = requests.get(baidu_map_api)
    content = response.text
    baidu_map_address = json.loads(content)
    formatted_address = baidu_map_address["result"]["formatted_address"]
    return formatted_address

def getLocation(filename):
    '得到照片的拍照位置（如果获取不到，则为空字符串）'
    try:
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
        else:
            raise "[%s] is not a file!\n" % filename
    except:
        raise "unopen file[%s]\n" % filename
        
    # 图像文件的拍摄地址默认为空
    locationStr= ''
    
    data = exifread.process_file( fd )
    if data: #取得照片的拍摄位置
        try:
            lat= format_lat_lng(data['GPS GPSLatitude'])  # [34, 12, 9286743/200000] -> xx.xxxxx
            lng= format_lat_lng(data['GPS GPSLongitude']) # [108, 57, 56019287/1000000] -> xx.xxxx
            locationStr= getLocationBy_lat_lng(lat, lng)
        except:
            pass
        
    return locationStr

'=================end{得到照片的拍摄地点}==================='

def orientate(img):
    '''对于手机、相机等设备拍摄的照片，由于手持方向的不同，拍出来的照片可能是旋转0°、90°、180°和270°。即使在电脑上利用软件将其转正，他们的exif信息中还是会保留方位信息。
        在用PIL读取这些图像时，读取的是原始数据，也就是说，即使电脑屏幕上显示是正常的照片，用PIL读进来后，也可能是旋转的图像，并且图片的size也可能与屏幕上的不一样。
        对于这种情况，可以利用PIL读取exif中的orientation信息，然后根据这个信息将图片转正后，再进行后续操作，具体如下。
    '''
    try:
        orientation= None
        for i in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[i]=='Orientation' : # 肯定会找到orientation，所以不需要对None做处理
                orientation= i
                break 
        exif=dict(img._getexif().items())
        if   exif[orientation] == 3 : 
            img=img.rotate(180, expand = True)
        elif exif[orientation] == 6 : 
            img=img.rotate(270, expand = True)
        elif exif[orientation] == 8 : 
            img=img.rotate(90, expand = True)
    except:
        pass
    return img


def add_watermark(filename, text):
    '为照片文件添加水印，filename是照片文件名，text是水印时间和位置'
    # 创建输出文件夹
    outdir= 'watermark/'
    mymkdir(outdir) 

    # 创建绘画对象
    image= Image.open(filename)
    image= orientate(image) # 将图片转正
    draw= ImageDraw.Draw(image)
    width, height= image.size # 宽度，高度
    size= int(0.04*width)  # 字体大小(可以调整0.04)
    myfont= ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', size=size) # 80, 4032*3024
    #fillcolor= '#000000' # RGB黑色
    fillcolor= '#fbfafe'

    # 参数一：位置（x轴，y轴）；参数二：填写内容；参数三：字体；参数四：颜色    
    d_width, d_height=0.5*width, 0.92*height # 字体的相对位置（0.5, 0.92可以根据图片调整）
    draw.text((d_width, d_height), text, font=myfont, fill=fillcolor) # (-1200, -320)

    new_filename= get_new_filename(filename)
    image.save(outdir + new_filename)


def scandir(startdir):
    '遍历指定目录，对满足条件的文件进行改名或删除处理'
    os.chdir(startdir) # 改变当前工作目录
    for obj in os.listdir(os.curdir) :
        if os.path.isfile(obj):
            if isTargetedFileType(obj): # 对满足过滤条件的文件，加时间和地点水印
                photoTime = getPhotoTime(obj) # 获得照片的拍摄时间,当作水印的内容
                location= getLocation(obj) # 获得照片的拍摄位置,当作水印的内容

                print("%s    %s" % (obj, photoTime+' '+location))
                add_watermark(obj, location +'\n'+ photoTime) #加时间和地点水印


if __name__ == "__main__":
    path = "./fig" # 照片位置
    scandir(path)