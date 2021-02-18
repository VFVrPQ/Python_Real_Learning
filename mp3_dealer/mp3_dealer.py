from pydub import  AudioSegment
import os
import numpy as np

def one(filePath):
    '''处理一个文件，129M的文件要1分钟左右
    '''
    song = AudioSegment.from_mp3(file=filePath)
    return song

def calc_dBFS(mydir):
    '''计算mydir目录下所有mp3的dBFS
    '''
    hasfile= {} # 处理过的文件集，使得可以中断后继续运行
    outfile = './dBFS.txt'
    if os.path.exists(outfile):
        with open(file=outfile, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            temp_list = line[:-1].split('\t')
            name, value = temp_list[0], float(temp_list[1])
            hasfile[name] = value
    
    #print(hasfile)
    for obj in os.listdir(mydir):  # 依次处理每个文件，并获得dBFS
        filePath = mydir + obj
        if not(obj in hasfile):
            song = one(filePath=filePath)
            print(obj, song.dBFS)

            with open(file=outfile, mode='a', encoding='utf-8') as f: # 保存处理结果
                f.write('%s\t%f\n' % (obj, song.dBFS))
    return hasfile

if __name__=='__main__':
    # 需要处理的文件夹
    mydir = 'd:\\越剧\\'
    hasfile = calc_dBFS(mydir)

    '''hasfile中已经存储了文件名和对应的dBFS
    '''
    ## 计算平均dBFS
    dBFS_list = []
    for key, value in hasfile.items():
        dBFS_list.append(value)
    print(np.mean(dBFS_list), np.median(dBFS_list), min(dBFS_list))

    # 按平均值重新调整mp3
    outdir = 'd:\\越剧\\output\\'
    avg = np.mean(dBFS_list)
    for obj in os.listdir(mydir):
        print('deal -- ', obj)
        filePath, outfilePath = mydir + obj , outdir + obj
        song = one(filePath=filePath)
        delta = avg - song.dBFS # 差值

        new_song = song + delta
        new_song.export(out_f=outfilePath, format='mp3')
    