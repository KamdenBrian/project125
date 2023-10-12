import turtle as trtl
import random as rand
import leaderboard as lb

#leaderboard variable
score = 0
leaderboard_file_name = "leaderboard.txt"

timer = 15 #game length
timer_up = False
counter_interval = 1000 #1 second

#turtle that draws the time
counter = trtl.Turtle()
counter.hideturtle()
counter.penup()
counter.goto(-100,-350) #below the map
counter.pendown()

#minion variables
minion_spawn_time = 3000 #3 seconds
minions_spawned = 0
minions_list = []

#gru variables
direction = "up" #default direction

#turtle that writes the score
score_writer = trtl.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.goto(0,300) #above the map
font_setup = ("Arial",20,"normal")

#turtle that draws leadeboard
leaderboard_writer = trtl.Turtle()
leaderboard_writer.hideturtle()

#add gru as valid turtle shape
trtl.register_shape("gru.gif")
gru_shape = "gru.gif"

#add minion as valid turtle shape
trtl.register_shape("minion2.gif")
minion_shape = "minion2.gif"

#add banana as valid turtle shape
trtl.register_shape("banana2.gif")
banana_shape = "banana2.gif"

#called once at beggining, makes gru appear at center
def countdown():
  global timer, timer_up
  counter.clear() #remove current time to update with new time
  if timer<= 0: #if game is over
    counter.write("Time's Up", font = font_setup)
    timer_up = True
    wn.bgpic("nopic") #remove background
    gru.hideturtle() #hide gru
    score_writer.clear() #hide the score
    i = 1 #variable for index on list
    for minion in minions_list: #hide every minion and empty out the list
      minion.hideturtle()
    display_leaderboard() 
  else: #if game is ongoing
    counter.write("Time: " + str(timer), font = font_setup) #updates with new time
    timer -=1
    counter.getscreen().ontimer(countdown, counter_interval) #calls method again after 1 second

#gets player name to put on leaderboard
def get_name():
  global player_name
  player_name = trtl.textinput("Name", "What is your name?")

#spawns gru which player controls
def spawn_gru():
  global gru
  gru = trtl.Turtle()
  gru.shape(gru_shape)
  gru.penup() #doesn't leave marker while moving

#on "a" press
def move_left():
  gru.goto(gru.xcor() - 15, gru.ycor())
  global direction 
  direction = "left"

#on "d" press
def move_right():
  gru.goto(gru.xcor() + 15, gru.ycor())
  global direction
  direction = "right"

#on "s" press
def move_down():
  gru.goto(gru.xcor(), gru.ycor() - 15)
  global direction
  direction = "down"

#on "w" press
def move_up():
  gru.goto(gru.xcor(), gru.ycor() + 15)
  global direction
  direction = "up"

#called every 3 seconds at first, speeds up as score goes up
def spawn_minion():
  global minions_spawned
  if(minions_spawned%2 == 0): #every even number
    spawnX = rand.randint(-450, 450)
    spawnY = rand.randint(200, 250) #top part of screen
  if(minions_spawned%2==1): #every odd number
    spawnX = rand.randint(-450,450)
    spawnY = rand.randint(-250, -200) #bottom part of screen
  #spawns in minion and moves to random spot
  minion = trtl.Turtle()
  minion.hideturtle()
  minion.penup()
  minion.shape(minion_shape)
  minion.goto(spawnX, spawnY)
  minion.showturtle()
  minions_list.append(minion) #adds to minion list
  minions_spawned += 1
  if(timer_up!=True): #if game isn't over
    wn.ontimer(spawn_minion, minion_spawn_time) #calls method again based on how fast spawn time is
  else: #if game ended
    for minion in minions_list:
      minion.hideturtle() #makes sure all minions are gone

#on "e" press
def throw_banana():
  #spawn banana on top of Gru
  banana = trtl.Turtle()
  banana.hideturtle()
  banana.penup()
  banana.goto(gru.xcor(), gru.ycor())
  banana.shape(banana_shape)
  banana.showturtle()
  #direction based on Gru's last movement
  if(direction == "up"):
    banana.goto(gru.xcor(), gru.ycor() + 150)
  elif(direction == "left"):
    banana.goto(gru.xcor() - 150, gru.ycor())
  elif(direction == "right"):
    banana.goto(gru.xcor() + 150, gru.ycor())
  elif(direction == "down"):
    banana.goto(gru.xcor(), gru.ycor()-150)
  banana.hideturtle()
  #checks with where banana ended up
  check_hit(banana)

def check_hit(banana):
  index = 0
  global score
  for minion in minions_list:
    #checks if banana within 50 pixels of a minion
    if(banana.distance(minion) < 50):
      minion.hideturtle()
      minions_list.pop(index) #remove minion from list
      score+= 1#increases score when fed
      update_score() #updates the score shown with the new score
    index+=1

#writes the score at the top of screen
def update_score():
  global minion_spawn_time
  score_writer.clear()
  score_writer.write(score, font=font_setup)
  if(score%5 == 0): #every 5 points decrease spawn time by .5 seconds
    minion_spawn_time -= 500 #.5 seconds

#shows the leaderboard at end of game
def display_leaderboard():
  leader_names_list = lb.get_names(leaderboard_file_name) #get all names of the leaderboard players
  leader_scores_list = lb.get_scores(leaderboard_file_name) #get all scores of the leaderboard players
  if (len(leader_scores_list) < 5 or score >= leader_scores_list[4]): #if the list is below 5 players or current player got in top 50
    lb.update_leaderboard(leaderboard_file_name, leader_names_list, leader_scores_list, player_name, score) #updates lb with new players score
    lb.draw_leaderboard(True, leader_names_list, leader_scores_list, leaderboard_writer, score) #draws the leaderboard on screen
    wn.bgpic("happyminion2.gif")
  else: #if player doesn't make it on the leaderboard
    lb.draw_leaderboard(False, leader_names_list, leader_scores_list, leaderboard_writer, score) #draws the lb on screen
    wn.bgpic("sadminion2.gif") 


wn = trtl.Screen()
wn.setup()
wn.bgpic("grassField2.gif") #background picture

#functions called on start
get_name() #gets the player name
spawn_gru() 
spawn_minion() #starts the minion spawning
update_score() #displays score as 0
countdown() #every 1 second updates countdown.

#event functions
wn.onkeypress(move_left, "a") #calls method on a press
wn.onkeypress(move_right, "d")
wn.onkeypress(move_up, "w")
wn.onkeypress(move_down, "s")
wn.onkeypress(throw_banana, "e")

wn.listen()
wn.mainloop()