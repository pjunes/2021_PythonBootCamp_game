import random
import time

##################################################
# 사용자와 기록
##################################################


class User():
    def __init__(self, name, speed=10, strength=10):
        self.name = name
        self.speed = speed
        self.strength = strength

    def modifyUser(self, name, speed, strength):
        self.name = name
        self.speed = speed
        self.strength = strength

# class ScoreBoard():
#     # 파일에 저장된 기록을 읽어와야함.
#     def __init__(self):
#         pass
#         self.scoreList = list()
#         self.loadBoard()
#
#     def resetBoard(self):
#         self.scoreList.clear()
#
#     def loadBoard(self):
#         pass
#
#     def saveBoard(self):
#         pass

class Score():
    def __init__(self, name, time):
        self.name = name
        self.time = time

##################################################
# 핵심 게임 진행
##################################################

class Object():
    def __init__(self, name, weight, width, height):
        self.name = name
        self.weight = weight
        self.width = width
        self.height = height

    def __str__(self):
        if self.name == "Empty" : return f"{self.name}"
        return f"{self.name} / {self.weight} / {self.width}x{self.height}"

    def getArea(self):
        return self.width * self.height

    # # Object의 내용 설정
    # def activateObject(self):
    #     pass

def createObject_random(name, weight_min, weight_max, width_min, width_max, height_min, height_max):
    return Object(name, random.randint(weight_min, weight_max),
                  random.randint(width_min, width_max),
                  random.randint(height_min, height_max))

def createObject(name, weight, width, height):
    return Object(name, weight, width, height)

# 칸마다 새로운 empty를 만들지 / 하나로 사용할지
empty = Object("Empty", 0, 1, 1)

class ObjectList():
    def __init__(self):
        self.data = list()

    def append(self, object):
        self.data.append(object)

    def sortByArea(self):
        self.data.sort(key=lambda object : object.getArea(), reverse=True)

class Block():
    def __init__(self):
        self.status = empty
        self.purpose = empty

    def isEmpty(self):
        if self.status == empty:
            return True
        return False

    def isPurposeEmpty(self):
        if self.purpose == empty:
            return True
        return False

    # Block에 Object를 배치
    def setObject(self, object):
        if self.isEmpty():
            self.status = object.name
            return True
        return False

    # Block에 배치될 Object를 예정
    def setPurpose(self, object):
        if self.isPurposeEmpty():
            self.purpose = object.name
            return True
        return False

    def __str__(self):
        return f"Empty : {self.isEmpty} / Purpose : {self.isPurposeEmpty} / current : {self.status}"


class House():
    def __init__(self):
        self.width = 8 # 가로 길이
        self.height = 8 # 세로 길이
        self.blockArr = list()

    # blockArr(2차원 배열)의 각 칸에 Block을 채워 넣는다.
    # Block 처음 생성시 empty를 가진다.
    def activateHouse(self):
        for i in range(self.width):
            self.blockArr.append(list())
            for j in range(self.height):
                self.blockArr[i].append(Block())

    # 난이도에 따라 집의 크기를 조정
    def setSize(self, m, n):
        self.houseWidth = m
        self.houseHeight = n

    # 집의 크기에 따라 House() 에서 사용가능한 범위 반환.
    def getWidthRange(self):
        return [4 - self.houseWidth / 2, 4 + self.houseWidth / 2] # 4x4라면, range(2, 6)

    def getHeightRange(self):
        return [4 - self.houseHeight / 2, 4 + self.houseHeight / 2]

    # object와 좌표를 받고, 배치가 가능한지 알려주는 함수.
    # 주의 : 매개변수로 object와 좌표를 줄 때, object가 절대 집 밖으로 나갈 여지가 있는 값을 넘기면 안된다.
    def checkPlace_status(self, object, x, y):
        m = object.width
        n = object.height
        for i in range(x, x + m):
            for j in range(y, y + n):
                if not self.blockArr[i][j].isEmpty():
                    return False
        return True

    def checkPlace_purpose(self, object, x, y):
        m = object.width
        n = object.height
        for i in range(x, x + m):
            for j in range(y, y + n):
                if not self.blockArr[i][j].isPurposeEmpty():
                    return False
        return True

    # def checkBlock_status(self, x, y):
    #     return self.blockArr[x][y].isEmpty

    # def checkBlock_purpose(self, x, y):
    #     return self.blockArr[x][y].isPurpose

    # object가 들어갈 자리가 비어있을 경우 실행되어 object를 원하는 자리에 배치하는 함수
    def locateObject(self, object, x, y):
        for i in range(object.width):
            for j in range(object.height):
                self.blockArr[x + i][y + j].setPurpose(object)

    def putObject(self, object, x, y):
        for i in range(object.width):
            for j in range(object.height):
                self.blockArr[x + i][y + j].setObject(object)

    # objectList에 포함된 object들을 전부 집에 배치하는 함수
    def locateObjectList(self, objectList):
        objectList.sortByArea() # 면적을 많이 차지하는 object부터 배치

        widthRange = self.getWidthRange()
        heightRange = self.getHeightRange()

        for object in objectList.data:
            while True:
                x = random.randint(widthRange[0], widthRange[1] - object.width)
                y = random.randint(heightRange[0], heightRange[1] - object.height)
                if self.checkPlace_purpose(object, x, y):
                    break
            self.locateObject(object, x, y)

   # def putObjectList():

    def printHouse(self):
        for i in range(self.width):
            print("=" * 20)
            for j in range(self.height):
                print(self.blockArr[i][j])

    def printHouseGraphic(self):
        for i in range(self.width):
            for j in range(self.height):
                print(f"{str(self.blockArr[i][j].status):^10}", end="")
            print()

    def printHouseGraphic_purpose(self):
        for i in range(self.width):
            for j in range(self.height):
                print(f"{str(self.blockArr[i][j].purpose):^10}", end="")
            print()

##################################################
# 설정
##################################################


# def setting():
#     pass
#
# def controlDifficulty(difficulty):
#     if difficulty == "Easy":
#         pass
#     elif difficulty == "Normal":
#         pass
#     elif difficulty == "Hard":
#         pass
#     else:
#         pass

