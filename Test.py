from PIL import Image
import Queue
import time

ext = "png"
imageName = "p.%s" % ext
saveName = "{0:05d}.{1}"

im = Image.open(imageName)
im = im.convert("RGB")
print im.format, im.size, im.mode
pix = im.load()
size = im.size

half = 256 >> 1
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
fillColor = red
lineColor = yellow
colors = [red, green, blue, yellow, (0, 223, 248), (223, 8, 248), (255, 2, 146)]
cLen = len(colors)

startPoint = [400, 984]
endPoint = [398, 25]
fa = [0] * size[0] * size[1]

def changeImage():
    x, y = size
    for i in xrange(x):
        for j in xrange(y):
            r, g, b = pix[i, j]
            if r > half and g > half and b > half:
                pix[i, j] = white
            else:
                pix[i, j] = black

def getNeighbor(point):
    x, y = point
    return [[x, y + 1], [x + 1, y], [x, y - 1], [x - 1, y]]

def inBounds(point, size):
    x, y = point
    sx, sy = size
    if x < 0 or y < 0 or x >= sx or y >= sy:
        return False
    return True

def isWhite(point):
    x, y = point
    if pix[x, y] == white:
        return True
    return False

def bfs(start, end):
    count = no = 0
    q = [[start]]
    while len(q):
        path = q.pop(0);
        p = path[-1]
        if p[0] == end[0] and p[1] == end[1]:
            im.save(saveName.format(no, ext))
            no += 1
            for pa in path:
                pix[pa[0], pa[1]] = pix[pa[0], pa[1] - 1] = pix[pa[0], pa[1] - 2] = lineColor
                count += 1
                if not count % 200:
                    im.save(saveName.format(no, ext))
                    no += 1
            no += 1
            im.save(saveName.format(no, ext))
            return path
        for ne in getNeighbor(p):
            if inBounds(ne, size) and isWhite(ne):
                newPath = list(path)
                newPath.append(ne)
                q.append(newPath)
                pix[ne[0], ne[1]] = fillColor
        if not count % 10000:
            im.save(saveName.format(no, ext))
            no += 1
        count += 1
    return None

def getValue(point, end):
    return abs(point[0] - end[0]) + abs(point[1] - end[1])

def aStar(start, end):
    fillColor = green
    lineColor = black
    count = no = 0
    Q = Queue.PriorityQueue()
    Q.put([0,[start]])
    while(Q.qsize()):
        q = Q.get()
        path = q[-1]
        p = path[-1]
        if p[0] == end[0] and p[1] == end[1]:
            im.save(saveName.format(no, ext))
            no += 1
            for pa in path:
                pix[pa[0], pa[1]] = pix[pa[0], pa[1] - 1] = pix[pa[0], pa[1] - 2] = lineColor
                count += 1
                if not count % 200:
                    im.save(saveName.format(no, ext))
                    no += 1
            im.save(saveName.format(no, ext))
            return path
        for ne in getNeighbor(p):
            if inBounds(ne, size) and isWhite(ne):
                newPath = list(path)
                newPath.append(ne)
                newList = [getValue(p, end) + len(newPath), newPath]
                Q.put(newList)
                pix[ne[0], ne[1]] = fillColor
        if not count % 10000:
            im.save(saveName.format(no, ext))
            no += 1
        count += 1
    return None

def getID(x, y):
    return x * size[0] + y

def ufInit(size):
    for i in range(size[0]):
        for j in range(size[1]):
            fa[getID(i, j)] = getID(i, j)

def ufFind(v):
    if v != fa[v]:
        fa[v] = ufFind(fa[v])
        return fa[v]
    return fa[v]

def ufUnion(x, y):
    x = ufFind(x)
    y = ufFind(y)
    if x == y: return
    fa[x] = y

def connectivity():
    fillColor = yellow
    no = count = now = 0
    d = {}
    x_range = (5, 792)
    y_range = (22, 986)

    ufInit(size)

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            if pix[x, y] != black:
                if pix[x - 1, y] == black and pix[x, y - 1] == black:
                    pass
                elif pix[x - 1, y] == white and pix[x, y - 1] == black:
                    ufUnion(getID(x - 1, y), getID(x, y))
                elif pix[x - 1, y] == black and pix[x, y - 1] == white:
                    ufUnion(getID(x, y - 1), getID(x, y))
                else:
                    ufUnion(getID(x - 1, y), getID(x, y - 1))
                    ufUnion(getID(x, y), getID(x - 1, y))

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            count += 1
            if pix[x, y] != black:
                father = ufFind(getID(x,y))
                if father not in d:
                    d[father] = colors[now % cLen]
                    now += 1
                pix[x, y] = d[father]
            if not count % 15000:
                im.save(saveName.format(no, ext))
                no += 1
    im.save(saveName.format(no, ext))

t1 = time.time()

changeImage()
#bfs(startPoint, endPoint)
#aStar(startPoint, endPoint)
connectivity()

t2 = time.time()
print t2- t1
