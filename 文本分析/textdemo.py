from snownlp import SnowNLP

print('############  0代表负面，1代表正面  ###########')
f = open('input.txt', 'r', encoding='utf-8')
i = 1
while True:
    try:
        line = f.readline()
        s = SnowNLP(line)
        print('第'+str(i)+'条博物馆新闻')
        print('关键词是：', s.keywords(3))
        print('情感分数：'+str(s.sentiments))
    except:
        print('')
    i = i+1
    if len(line) == 0:
        break
f.close()




