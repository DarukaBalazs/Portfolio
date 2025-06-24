import pygame as pg
from player import Player
from buttons import Button
from table import Table
import xlsxwriter as xw

pg.init()

#import datas
gamenumber = int(open("data/gamenum.txt").readline())
gamenumber += 1
excelname = "Game"+str(gamenumber)+".xlsx"
workbook = xw.Workbook(excelname)
worksheet = workbook.add_worksheet()

#pictures import
chesstablep = pg.image.load("pic/board.png")
Menup = pg.image.load("pic/Menu.png")
startp = pg.transform.scale(pg.image.load("pic/start-button.png"),(100,100))
continp = pg.transform.scale(pg.image.load("pic/Continue.png"), (200,75))
forwardp = pg.transform.scale(pg.image.load("pic/forward.png"),(100,100))
backwardp = pg.transform.scale(pg.image.load("pic/backward.png"),(100,100))
chesspiecep = pg.transform.scale(pg.image.load("pic/chesspieces.png"),(300,300))
wwinp = pg.image.load("pic/WWIN.png")
bwinp = pg.image.load("pic/BWIN.png")
drawp = pg.image.load("pic/Draw.png")
roundp = pg.image.load("pic/endround.png")


#Colors
LGreen = (101, 224, 134)
Green = (0,255,0)
Red = (255,0,0)
Blue = (0,0,255)
White = (255,255,255)
Black = (0,0,0)
DTBlue = (1,25,54)
LTBlue = (171,200,199)
LRBlue = (156,175,174)
LBlue = (141,150,149)
Grey = (110,99,96)
NGreen = (135,255,101)

#rectangles
namebox = pg.Rect(100,150,600,50)

#Fonts
inputfont = pg.font.SysFont('fonts/bascifont.ttf', 50)

#display settings
screen_w = 800
screen_h = 700
screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("Sakk bajnokság")
pg.display.set_icon(chesspiecep) 

#clock
clock = pg.time.Clock()

#states
main_state = True
menu_state = True
names_state = False
game_state = False
end_state = False
started = False

#buttons
menubtn = Button(10, 16, Menup, 0.05)
startbtn = Button(350, 0, startp, 1)
sstartbtn = Button(350,400,startp,1)
continbtn = Button(300, 10, continp, 1)
forwardbtn = Button(600,400,forwardp,1)
backwardbtn = Button(600,200,backwardp,1)
bwinbtn = Button(100,125,bwinp,1)
drawbtn = Button(100,250,drawp,1)
wwinbtn = Button(100,375,wwinp,1)
endroundbtn = Button(100,500,roundp,1)



#Early variables (zeros)
tablecount = 1
currenttable = 0
tables = []
nameinput = ""
nameboxactive = False
previd = 0
game_played = 0
players = []
roundstart = True
roundendcounter = 0



#main loop
while main_state:
    
    #refreshing variables
    event = pg.event.poll()
    clock.tick(30)
    key = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()
    
    for et in pg.event.get():
        #quitting
        if et.type == pg.QUIT:
            main_state = False
        #clicks
        if et.type == pg.MOUSEBUTTONDOWN:
            if namebox.collidepoint(et.pos):
                nameboxactive = True
            else:
                nameboxactive = False
        #namebox 
        if nameboxactive:
            if et.type == pg.KEYDOWN:
                if et.key == pg.K_BACKSPACE:
                    nameinput = nameinput[:-1]
                elif et.key == pg.K_RETURN and nameinput != "":
                    previd += 1
                    players.append(Player(nameinput,previd))
                    nameinput = ""
                else:
                    nameinput += et.unicode
                
    screen.fill(White)


    #header
    pg.draw.rect(screen,LBlue,(0,0,800,100))


    #Menu part
    if menu_state:
        if menubtn.draw(screen):
            menu_state = True

        #started
        if started: 
            if continbtn.draw(screen):
                game_state = True
                menu_state = False

        #First start
        else: 
            if startbtn.draw(screen):
                started = True
                names_state = True
                menu_state = False

    #Name Selections
    if names_state:
        
        #name inputs
        if nameboxactive:
            nameboxcolor = LTBlue
        else:
            nameboxcolor = Grey
        if menubtn.draw(screen):
            menu_state = True
            names_state = False
        pg.draw.rect(screen, nameboxcolor, namebox)
        namesurf = inputfont.render(nameinput, True, Black)
        screen.blit(namesurf, (105,155))
        
        #table number input

        
        #start button usage
        if sstartbtn.draw(screen):
            tablecount = len(players)//2
            for i in range(tablecount):
                tables.append(Table(screen))
            names_state = False
            game_state = True

    #game system
    if game_state:
        #chess board draw
        screen.blit(chesspiecep,(250,200))   
        
        #menu button
        if menubtn.draw(screen):
            game_state = False
            menu_state = True
            
        #always sort players by their points
        players.sort(key=lambda x: x.point)

        #show the next table table
        if len(tables) > 1:
            tablecountsurf = inputfont.render(f"{currenttable + 1}", True, Black)
            tablec_rect = tablecountsurf.get_rect(center=(100,125))
            screen.blit(tablecountsurf,tablec_rect)
            if forwardbtn.draw(screen) and currenttable < len(tables)-1:
                currenttable += 1
        
        #show the previous table
            if backwardbtn.draw(screen) and currenttable > 0:
                currenttable -= 1
        
        #give all free tables new pairs, if cant 
        if roundstart:
            for table in tables:
                if table.free:
                    loopbrake = False
                    for num,player in enumerate(players):
                        if num > 0 and player.free:
                            for i in range(1,num+1):
                                if players[num-i].free and (players[num-i].id not in player.played_with):
                                    player.free = False
                                    players[num-i].free = False
                                    player.played_with.append(players[num-i].id)
                                    players[num-i].played_with.append(player.id)
                                    table.currentplayers.append(player.id)
                                    table.currentplayers.append(players[num-i].id)
                                    if player.black >= players[num-i].black:
                                        player.currentcolor = 1
                                        players[num-i].currentcolor = 0
                                        players[num-i].black += 1
                                    else:
                                        player.currentcolor = 0
                                        player.black += 1
                                        players[num-i].currentcolor = 1
                                    table.free = False
                                    loopbrake = True
                                    currenttable = tables.index(table)
                                    print(f"{table.currentplayers}")
                                    break
                            if loopbrake:
                                break   
        roundstart = False    
        #current names and stats
        #black wins
        if bwinbtn.draw(screen):
            if currenttable != None:
                for player in players:
                    if player.id in tables[currenttable].currentplayers:
                        if player.currentcolor == 0:
                            player.point += 2
                        player.free = True
                tables[currenttable].currentplayers = []
            game_played += 1
            
        #white wins
        if wwinbtn.draw(screen):
            if currenttable != None:
                for player in players:
                    if player.id in tables[currenttable].currentplayers:
                        if player.currentcolor == 1:
                            player.point += 2
                        player.free = True
                tables[currenttable].currentplayers = []
            game_played += 1
            
        #draw
        if drawbtn.draw(screen):
            if currenttable != None:
                for player in players:
                    if player.id in tables[currenttable].currentplayers:
                        player.point += 1
                        player.free = True
                tables[currenttable].currentplayers = []
            game_played += 1

        if currenttable != None:
            for player in players:
                if player.id in tables[currenttable].currentplayers:
                    if player.currentcolor == 0:
                        bnamesurf = inputfont.render(player.name, True, Black)
                        bname_rect = bnamesurf.get_rect(center=(300,175))
                        screen.blit(bnamesurf,bname_rect)
                    else:
                        wnamesurf = inputfont.render(player.name, True, Black)
                        wname_rect = wnamesurf.get_rect(center=(300,525))
                        screen.blit(wnamesurf,wname_rect)
                        
        if endroundbtn.draw(screen):
            roundstart = True
            for table in tables:
                table.free = True
            
            
        
    if end_state:
        pass
    #display update
    pg.display.update()
    
    
#excel outting
worksheet.write(0,0,'Placement')
worksheet.write(0,1,'Name')
worksheet.write(0,2,'Point')
row = 1
col = 0
players.sort(key=lambda x: x.point,reverse = True)
for num,player in enumerate(players):
    worksheet.write(row,col,num+1)
    worksheet.write(row,col+1,player.name)
    worksheet.write(row,col+2,player.point)
    row += 1
workbook.close()

with open('data/gamenum.txt','w') as f:
    f.write(str(gamenumber))

print(game_played)
print(', '.join(map(str,players)))
pg.quit()