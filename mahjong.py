from os import read
import sys
import copy

def checkInput(handstr):
    """
    检查输入字符串是否合法
    输入字符串最多只有一个空格，且只能包含1-9、TBZFW和空格
    """
    num_space = 0
    for i in handstr:
        if i.isdigit():
            if int(i) == 0:
                print('手牌不能出现0！')
                return False
        elif i.isalpha():
            if i not in ['T', 'B', 'W', 'Z', 'F', 'O']:
                print('手牌出现非法字母！')
                return False
        elif i == ' ':
            num_space += 1
            if num_space >1:
                print('只能出现一个空格！')
                return False
        else:
            print('手牌出现非法字符！')
            return False
    
    return True

def convertHandstr(fullHandstr):
    """
    将手牌字符串转换为两个列表：手牌列表和刻子列表，并进行排序，然后检查同种牌是否超过四个
    牌面编号：1-9饼，11-19条，21-29万（预留）
             31东，33南，35西，37北，
             41中，43发，45白
    刻子列表中每种牌组成一个列表
    """
    handlist = fullHandstr.split()
    if len(handlist) == 1:
        handstr = handlist[0]
        tripletstr = ''
    elif len(handlist) == 2:
        handstr, tripletstr = handlist
    else:
        print('手牌分割出错！')
        return False, None, None
    
    currentType = -1
    tmplist = list()
    hands = list()
    for i in handstr:
        if i.isdigit():  # 数字则转换为整数并加入临时列表
            tmplist.append(int(i))
        elif i in ['T', 'B', 'W']:  #遇到条饼万，则检查临时列表是否有数字
            if len(tmplist) == 0:
                # 之前没有数字，报错
                print('条、饼、万之前必须指定数字！')
                return False, None, None
            else:
                if i == 'B':
                    currentType = 0
                elif i == 'T':
                    currentType = 1
                elif i == 'W':
                    currentType = 2
                for j in tmplist:
                    hands.append(j + currentType * 10)
                tmplist = list()
        elif i in ['Z', 'F', 'O']:  #遇到中发白，检查临时列表是否没有数字
            if len(tmplist) > 0:
                # 之前有数字，报错
                print('中发白之前不能有数字！')
                return False, None, None
            else:
                if i == 'Z':
                    hands.append(41)
                elif i == 'F':
                    hands.append(43)
                elif i == 'O':
                    hands.append(45)
    
    tmplist = list()
    triplets = list()
    for i in tripletstr:
        if i.isdigit():  # 数字则转换为整数并加入临时列表
            tmplist.append(int(i))
        elif i in ['T', 'B', 'W']:  #遇到条饼万，则检查临时列表是否有数字
            if len(tmplist) == 0:
                # 之前没有数字，报错
                print('条、饼、万之前必须指定数字！')
                return False, None, None
            else:
                if i == 'B':
                    currentType = 0
                elif i == 'T':
                    currentType = 1
                elif i == 'W':
                    currentType = 2
                for j in tmplist:
                    triplets.append(j + currentType * 10)
                tmplist = list()
        elif i in ['Z', 'F', 'O']:  #遇到中发白，检查临时列表是否没有数字
            if len(tmplist) > 0:
                # 之前有数字，报错
                print('中发白之前不能有数字！')
                return False, None, None
            else:
                if i == 'Z':
                    triplets.append(41)
                elif i == 'F':
                    triplets.append(43)
                elif i == 'O':
                    triplets.append(45)
                
    # 排序和检测数量
    hands.sort()
    triplets.sort()
    full = hands + triplets
    fullset = set(full)
    for i in fullset:
        if full.count(i) > 4:
            print('手牌中' + str(i) + '多于4张，不合法！')
            return False, None, None
    
    #刻子列表分组、检测数量
    cur = 0
    tmp = list()
    new_triplets = list()
    for i in triplets:
        if i != cur:
            if len(tmp) > 0:
                new_triplets.append(tmp)
                tmp = list()
            cur = i
        tmp.append(i)
    if len(tmp) > 0:
        new_triplets.append(tmp)
    for i in new_triplets:
        if len(i) < 3 or len(i) > 4:
            print('刻子必须为3张或4张！')
            return False, None, None
            
    return True, hands, new_triplets

def checkWin(hands, triplets):
    """
    胡牌检测函数，输入排序后的手牌列表和刻子列表，输出是否胡牌
    """
    # 检测牌数，每个刻子不论碰杠均算3张，只有14张才能胡
    tileNum = len(triplets) * 3 + len(hands)
    if tileNum != 14:
        print('您有' + str(tileNum) + '张牌，是相公！')
        return False
    
    # 七对为特殊牌型，优先检测
    # 七对不能有碰或杠
    if len(triplets) == 0:
        pairNum = 0
        i = 0
        while i < len(hands):
            if hands[i] == hands[i+1]:
                pairNum += 1
                i += 2
            else:
                break
        if pairNum == 7:
            return True

    # 检测其他牌型
    tileSetsNum = 4 - len(triplets)    # 需要检测的剩余牌组数
    # 生成将牌候选列表
    pairCandidate = list()
    for i in set(hands):
        if hands.count(i) >= 2:
            pairCandidate.append(i)
  
    for p in pairCandidate:
        tmp = copy.deepcopy(hands)
        tileSetsNumRemain = tileSetsNum
        # 提取一对将
        tmp.remove(p)
        tmp.remove(p)

        while tileSetsNumRemain > 0:
            # 判断前三张是否相同，相同则作为刻子移除，否则试图组顺子
            if tmp[0] == tmp[1] and tmp [1] == tmp[2]:
                tileSetsNumRemain -= 1
                tmp.pop(0)
                tmp.pop(0)
                tmp.pop(0)
            else:
                if tmp[1] == tmp[0]+1 and tmp[2] == tmp[1]+1:
                    # 前三张组成顺子则移除并继续判断
                    tileSetsNumRemain -= 1
                    tmp.pop(0)
                    tmp.pop(0)
                    tmp.pop(0)
                else:
                    # 该对做将无法胡牌，跳出重新选将
                    break

        if tileSetsNumRemain == 0:
            return True
    
    return False

def findReady(hands, triplets):
    """
    听牌检测函数，检测当前是否听牌，以及听什么牌
    """
    # 检测牌数，每个刻子不论碰杠均算3张，只有14张才能胡
    tileNum = len(triplets) * 3 + len(hands)
    if tileNum != 13:
        print('您有' + str(tileNum) + '张牌，无法听牌！')
        return False, None

    tilesAvailable = list(range(1, 10))+ list(range(11, 20)) + [41, 43, 45]
    readyTiles = list()
    for i in tilesAvailable:
        tmp = copy.deepcopy(hands)
        tmp.append(i)
        tmp.sort()
        if checkWin(tmp, triplets):
            readyTiles.append(i)
    
    if len(readyTiles) == 0:
        #print('您没有听牌！')
        return False, None
    else:
        #print('您听以下牌：')
        print(readyTiles)
        return True, readyTiles

def giveAdvice(hands, triplets):
    """
    建议函数，给出当前打哪些牌可以听，以及分别听什么牌
    """
    # 检测牌数，必须14张牌才有意义
    tileNum = len(triplets) * 3 + len(hands)
    if tileNum != 14:
        print('您有' + str(tileNum) + '张牌，不可能胡牌！')
        return False, None
    
    # 检测当前是否已胡牌
    if checkWin(hands, triplets):
        print('您当前已胡牌！')
    else:
        print('您尚未胡牌！')
    
    playAvailable = set(hands)
    result = list()
    for i in playAvailable:
        tmp = copy.deepcopy(hands)
        tmp.remove(i)
        status, readyTiles = findReady(tmp, triplets)
        if status:
            result.append((i, readyTiles))
    
    if len(result) > 0:
        print('您可以打以下牌从而听牌：')
        for i in result:
            print(i)
    else:
        print('您暂时无法听牌。')
    return result

if __name__ == '__main__':
    print('输入记号：T-条，B-饼，W-万，Z-红中，F-发财，O-白板')
    print('输入格式：手牌（空格）刻子，例如：345T1245BZZF 888T')
    handstr = input('请输入待计算的牌：')
    handstr = handstr.upper()
    if not checkInput(handstr):
        sys.exit()
    status, hands, triplets = convertHandstr(handstr)
    if not status:
        sys.exit()
    
    print(hands)
    print(triplets)

    findReady(hands, triplets)
    # giveAdvice(hands, triplets)
    
    
    

    

