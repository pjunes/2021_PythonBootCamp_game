from Back import *
from tkinter import *
import time
import random

def predictLocation(objectCoord, dx, dy):
    objectCoord[0] += dx
    objectCoord[1] += dy
    objectCoord[2] += dx
    objectCoord[3] += dy
    return objectCoord

def isColide(object1Coord, object2Coord):
    obj1_x1 = object1Coord[0]; obj1_y1 = object1Coord[1]
    obj1_x2 = object1Coord[2]; obj1_y2 = object1Coord[3]

    obj2_x1 = object2Coord[0]; obj2_y1 = object2Coord[1]
    obj2_x2 = object2Coord[2]; obj2_y2 = object2Coord[3]

    if (obj1_x1 > obj2_x1 and obj1_x1 < obj2_x2) or (obj1_x2 > obj2_x1 and obj1_x2 < obj2_x2):
        if (obj1_y1 > obj2_y1 and obj1_y1 < obj2_y2) or (obj1_y2 > obj2_y1 and obj1_y2 < obj2_y2):
            return True
    return False

def nameToImg(name):
    if name == "Table":
        return table_img
    elif name == "Tv":
        return tv_img
    elif name == "Bed":
        return bed_img
    elif name == "Computer":
        return computer_img

def nameToImgBlock(name):
    if name == "Table":
        return table_block
    elif name == "Tv":
        return tv_block
    elif name == "Bed":
        return bed_block
    elif name == "Computer":
        return computer_block

class Character():
    def __init__(self, houseG):
        self.canvas = canvas

        # 공유되는 정보
        self.purposeList = houseG.purposeList
        self.objectRangeList = houseG.objectRangeList

        # 캐릭터 정보
        self.strength = 1
        self.pocket = empty

        # 캐릭터 시작 위치
        self.x = 256
        self.y = 360

        # 캐릭터 생성
        self.id = self.canvas.create_oval(self.x-25, self.y-25, self.x+25, self.y+25, fill="black")
        self.speed = 15

        # 캐릭터 움직임
        self.canvas.focus_set()
        self.canvas.bind("<Left>", lambda _: self.move(-1*self.speed,0))
        self.canvas.bind("<Right>", lambda _: self.move(self.speed,0))
        self.canvas.bind("<Up>", lambda _: self.move(0,-1*self.speed))
        self.canvas.bind("<Down>", lambda _: self.move(0,self.speed))

        self.canvas.bind("<Escape>", lambda _: window.destroy())

    def getRange(self):
        return self.canvas.coords(self.id)

    def move(self, dx, dy):
        # 충돌하지 않는 위치로 움직인다면, move / 충돌할 예정이라면 움직이지 않음 + 이벤트 발생
        if self.update(predictLocation(self.getRange(), dx, dy)):
            canvas.move(self.id, dx, dy)

    def setStrength(self, strength):
        self.strength = strength

    def setSpeed(self, weight):
        self.speed = self.speed - weight/self.strength

    def update(self, locationRange):
        # 충돌시 발생하는 이벤트들 작성
        # 맵 밖으로 나갈시
        if not isColide(locationRange, [0, 0, 1280, 720]):
            print("Map collision")
            return False

        # 트럭과 충돌시
        if isColide(locationRange, [60, 180, 190, 540]):
            print("Truck collision")
            if self.pocket == empty:
                if len(objList.data) > 0:
                    self.pocket = objList.data.pop().name
                else:
                    print("endGame")
                    self.endGame()
                print(self.pocket)
                self.canvas.create_image(180, 90, image=nameToImg(self.pocket))
                self.setSpeed(10)
            # 트럭과 충돌시 가구 받기 / 가구 이미 있으면 못받음
            return False

        # purpose와 충돌시
        for purpose in self.purposeList:
            if isColide(locationRange, purpose[1]):
                print("Purpose collision")
                if purpose[0] == self.pocket:
                    self.pocket = empty
                    self.canvas.create_image(180, 90, image=empty_img)

                    for i in range(8):
                        for j in range(8):
                            if houseG.blockList[i][j].purpose == purpose[0]:
                                houseG.blockList[i][j].changeImg(nameToImgBlock(purpose[0]))
                    self.setSpeed(-10)
                    print("배치성공")


                return False

        # 오브젝트와 충돌시
        for objectRange in self.objectRangeList:
            if isColide(locationRange, objectRange):
                print("Object collision")
                return False

        # 이동 가능하면 True
        return True

    def endGame(self):
        self.canvas.create_rectangle(0, 0, 1280, 720, fill="sky blue")
        self.canvas.create_image(640, 360, image=clear_img)

class BlockG():
    def __init__(self, x, y):
        self.canvas = canvas
        self.x = x+30
        self.y = y+30
        self.object = empty
        self.purpose = empty
        self.canvas.create_image(self.x, self.y, image=empty_img)

    def changePurpose(self, newPurpose):
        self.purpose = newPurpose
        self.changeImg(nameToImg(newPurpose))

    def changeImg(self, newImg):
        self.canvas.create_image(self.x, self.y, image=newImg)


class TruckG():
    def __init__(self):
        self.canvas = canvas
        self.canvas.create_rectangle(60, 180, 190, 540, fill="silver")

    def getRange(self):
        return [60, 180, 190, 540]

class HouseG():
    def __init__(self, house):
        self.canvas = canvas
        self.house = house
        self.blockList = list()
        self.purposeList = list()
        self.objectRangeList = list()

        # 배경 잔디밭
        self.canvas.create_rectangle(0, 0, 1280, 720, fill="pale green")
        self.canvas.create_image(105,90,image=pocket)
        self.canvas.create_image(180,90,image=empty_img)


        if self.house.houseWidth == 8:
            x0 = 600
            y0 = 120
        elif self.house.houseWidth == 6:
            x0 = 660
            y0 = 180
        else:
            x0 = 720
            y0 = 240

        for i in range(self.house.houseWidth):
            self.blockList.append(list())
            for j in range(self.house.houseHeight):
                x = x0 + (i * 60)
                y = y0 + (j * 60)
                self.blockList[i].append(BlockG(x, y))

        # house의 purpose를 houseG로 옮겨야됨.
        for i in range(8):
            for j in range(8):
                current_purpose = house.blockArr[i][j].purpose
                if not current_purpose == empty:
                    self.blockList[i][j].changePurpose(current_purpose)
                    x = x0 + (i * 60)
                    y = y0 + (j * 60)
                    self.purposeList.append([current_purpose,[x, y, x + 60, y + 60]])


window = Tk()
window.title("이사하기")
window.geometry("1280x720")
window.resizable(width=False, height=False)

pocket = PhotoImage(file="pocket.png")
empty_img = PhotoImage(file="empty.png")
table_img = PhotoImage(file="table.png")
table_block = PhotoImage(file="table_block.png")
tv_img = PhotoImage(file="tv.png")
tv_block = PhotoImage(file="tv_block.png")
bed_img = PhotoImage(file="bed.png")
bed_block = PhotoImage(file="bed_block.png")
computer_img = PhotoImage(file="computer.png")
computer_block = PhotoImage(file="computer_block.png")
clear_img = PhotoImage(file="clear.png")

canvas = Canvas(window, width=1280, height=720)
canvas.pack()

print("Start\n")

house = House()
house.activateHouse()
house.setSize(8, 8)

objList = ObjectList()
obj1 = createObject_random("Bed", 5, 15, 2, 2, 1, 1); objList.append(obj1)
obj2 = createObject_random("Tv", 5, 15, 1, 1, 2, 2); objList.append(obj2)
obj3 = createObject_random("Table", 5, 15, 2, 2, 2, 2); objList.append(obj3)
obj4 = createObject_random("Computer", 5, 15, 1, 1, 1, 1); objList.append(obj4)

house.locateObjectList(objList)
house.printHouseGraphic_purpose()

## GUI 시작

houseG = HouseG(house)
truckG = TruckG()
character = Character(houseG)

# Test
# 트럭과 충돌시 오브젝트 지급
random.shuffle(objList.data)


window.mainloop()