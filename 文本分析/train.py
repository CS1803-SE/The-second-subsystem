from snownlp import sentiment
sentiment.train(
    'D:\\python3\\Lib\\site-packages\\snownlp\\sentiment\\neg.txt',
    'D:\\python3\\Lib\\site-packages\\snownlp\\sentiment\\pos.txt' )                                #neg.txt为消极词汇训练集；pos.txt为积极词汇训练集
sentiment.save('D:\\python3\\Lib\\site-packages\\snownlp\\sentiment\\sentiment.marshal.2')          #新的训练集命名