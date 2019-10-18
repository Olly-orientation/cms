import math
def abc(page,articleCount,perPage,panelItem=3):
    pageList=[]
    allPages = math.ceil(articleCount / perPage)
    # print("页数",allPages)
    if page==1:
        print("页面为1")
        for i in range(1,panelItem+1):
            pageList.append(i)
        # print(pageList)
        pageList = filter(lambda x: x <= allPages, pageList)
        # print(list(pageList))
    else:
        leftover = (panelItem) % 2
        average = (panelItem - 1) / 2
        if leftover == 0:
            # 均分
            # print("能")
            left, right = ((page - 1) - math.floor(average), page + math.ceil(average))
        else:
            # print("不能")
            average = int(average)
            left, right = ((page) - average, page + average)
            # print("left",left)
            # print("right",right)
        # 左右进行加减
        for i in range(left,page):
            pageList.append(i)
        for i in range(page, right + 1):
            pageList.append(i)
        # print(pageList)
        pageList=filter(lambda x:x<=allPages and x>=1,pageList)
        # print(pageList)
        # print("page",page)
        # print(list(pageList))
abc(19,105,5,5)