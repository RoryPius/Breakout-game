from kepoco import display, buttonL, buttonR, buttonB, buttonA


# Set up the display
display.setFPS(30)  # Run at 30 frames per second
#set font
display.setFont("/lib/font3x5.bin", 3, 5, 1)

# Paddle properties
paddle_x = 35  # Starting x position (middle of screen)
paddle_y = 34  # Y position (near bottom, screen is 128 pixels tall)
paddle_width = 9
paddle_height = 1
paddle_speed = 1 # PHASE 2: How many pixels paddle moves per frame

# PHASE 3: Ball properties
ball_x = 16  # Start in middle of screen (72 / 2)
ball_y = 20  # Start in upper-middle area
ball_size = 2  # Ball is 2x2 pixels
ball_speed_x = 1  # Horizontal speed (positive = right)
ball_speed_y = 1 
ball_counter = 0 
ball_base_delay = 3  # Base delay for ball movement (lower = faster)

# game state
game_over = False
you_win = False  # Track if player won

# PHASE 6: Score and Lives
score = 0  # Player's score
lives = 3  # Number of lives remaining
you_win = False  # Track if player won

# PHASE 5: Brick properties
brick_rows = 4  # Number of rows of bricks
brick_cols = 8  # Number of columns of bricks
brick_width = 8  # Width of each brick
brick_height = 3  # Height of each brick
brick_gap = 1  # Gap between bricks


# PHASE 7: Function to reset the game
def reset_game():
    global bricks, ball_x, ball_y, ball_speed_x, ball_speed_y
    global score, lives, game_over, you_win, paddle_x,paddle_speed, ball_base_delay
    
    # Reset score and lives
    score = 0
    lives = 3
    game_over = False
    you_win = False
    
    # Reset paddle position
    paddle_x = 26
    
    # Reset paddle speed
    paddle_speed = 1
    
    # Reset ball
    ball_x = 36
    ball_y = 20
    ball_speed_x = 1
    ball_speed_y = 1
    ball_base_delay = 3
    
    # Recreate all bricks
    bricks = []
    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick_row.append(1)
        bricks.append(brick_row)


# Phase 5: Creating the brick grid (list)
bricks = [] #empty list to hold all bricks 
for row in range (brick_rows):
    brick_row = [] #empty list for row
    for col in range (brick_cols):
        brick_row.append(1)
    bricks.append(brick_row)


# PHASE 6: Function to reset ball position, (when losing a life)
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x
    ball_x = 36
    ball_y = 20
    ball_speed_x = 1
    ball_speed_y = 1

# PHASE 6: Function to reset paddle position, (when losing a life)
def reset_paddle():
    global paddle_x, paddle_speed
    paddle_x = 35


    
    
# Initialize game at start
reset_game()

# Main game loop
while True:
    
    # PHASE 7: Check for restart with A button
    if buttonA.justPressed() and (game_over or you_win):
        reset_game()
        
    # Check if B button is pressed to quit
    if buttonB.justPressed():
        display.fill(display.BLACK)  # Clear screen
        display.update()
        break  # Exit the game loop
    
    # game_over check 
    if not game_over and not you_win: 
    
        # PHASE 2: Paddle movement with buttons
        if buttonL.pressed():
            paddle_x = paddle_x - paddle_speed
        if buttonR.pressed():
            paddle_x = paddle_x + paddle_speed
        
        
        # PHASE 2: Keep paddle on screen (boundary checking)
        if paddle_x < 0:
            paddle_x = 0
        
        if paddle_x > 72 - paddle_width:
            paddle_x = 72 - paddle_width
        
        # # PAHSE 3: Move ball
        # ball_x = ball_x + ball_speed_x
        # ball_y = ball_y + ball_speed_y
        
        # PHASE 3: Move the ball (slower - every other frame)
        ball_counter = ball_counter + 1
        if ball_counter >= ball_base_delay:
            ball_x = ball_x + ball_speed_x
            ball_y = ball_y + ball_speed_y
            ball_counter = 0
        
        
            # PAHSE 3: Ball bounces off walls
            if ball_x <= 0 or ball_x >= 72 - ball_size:
                ball_speed_x = -ball_speed_x
            
            if ball_y <=0:
                ball_speed_y = -ball_speed_y
            
            # PHASE 5: Check collisions
            for row in range (brick_rows):
                for col in range (brick_cols):
                    if bricks[row][col] == 1: #if brick exists 
                        #calculate brick position
                        brick_x = col * (brick_width + brick_gap)
                        brick_y = row * (brick_height + brick_gap) + 2
                        
                        # Check if ball hits this brick
                        if (ball_x + ball_size >= brick_x and 
                            ball_x <= brick_x + brick_width and
                            ball_y + ball_size >= brick_y and 
                            ball_y <= brick_y + brick_height):
                            # Brick hit! Destroy it
                            bricks[row][col] = 0
                            # PHASE 6: Add to score
                            score = score + 2    
                            
                            
                            # PHASE 7: difficulty progression
                            # Speed up every 16 points (8 bricks) and only down to delay of 1
                            if score == 16 and ball_base_delay > 1:
                                ball_base_delay = 2
                                paddle_speed = paddle_speed + 1
                            elif score == 32 and ball_base_delay > 1:
                                ball_base_delay = 1
                                
                            
                                
                            # Bounce ball
                            ball_speed_y = -ball_speed_y

            # PHASE 6: Check if all bricks destroyed (win condition)
            bricks_remaining = 0
            for row in range(brick_rows):
                for col in range(brick_cols):
                    if bricks[row][col] == 1:
                        bricks_remaining = bricks_remaining + 1
            
            if bricks_remaining == 0:
                you_win = True                        
        
            # PHASE 4: Ball hits paddle (bounce up)
            if ball_y + ball_size >= paddle_y and ball_y <= paddle_y + paddle_height:
                if ball_x + ball_size >= paddle_x and ball_x <= paddle_x + paddle_width:
                    ball_speed_y = -ball_speed_y
                    ball_y = paddle_y - ball_size  # Move ball above paddle to prevent sticking
    
            # Game over check
            if ball_y > 40:
                game_over = True
            
            # PHASE 6: Ball goes below paddle (lose a life)
            if ball_y >= 40:
                lives = lives - 1
                if lives <= 0:
                    game_over = True
                else:
                    reset_ball()  # Reset ball position for next life
                    reset_paddle() # Reset paddle position for next life

        
    # Clear the screen (fill with black)
    display.fill(display.BLACK)
        
    # PHASE 5: draw all bricks
    for row in range(brick_rows):
        for col in range(brick_cols):
            if bricks[row][col] == 1:
                brick_x = col * (brick_width + brick_gap)
                brick_y = row * (brick_height + brick_gap) + 2
                display.drawFilledRectangle(brick_x, brick_y, brick_width, brick_height, display.WHITE)
        
    # Draw the paddle (a white rectangle)
    display.drawFilledRectangle(paddle_x, paddle_y, paddle_width, paddle_height, display.WHITE)
    
    # PHASE 3: Draw the ball (a white square)
    display.drawFilledRectangle(ball_x, ball_y, ball_size, ball_size, display.WHITE)
    
    # PHASE 6: Display score and lives at bottom
    display.drawText("S:" + str(score), 1, 30, display.LIGHTGRAY)
    display.drawText("L:" + str(lives), 55, 30, display.LIGHTGRAY)
    
    #PHASE 4: Display game over message
    if game_over:
        display.fill(display.BLACK)
        display.drawText("GAME OVER", 10, 8, display.WHITE)
        display.drawText("press:", 10, 15, display.WHITE)
        display.drawText("B to end", 10, 23, display.WHITE)
        display.drawText("A to restart", 10, 30, display.WHITE)
    
    # PHASE 6: Display win message
    if you_win:
        display.fill(display.BLACK)
        display.drawText("YOU WIN!", 10, 8, display.WHITE)
        display.drawText("press:", 10, 15, display.WHITE)
        display.drawText("B to end", 10, 23, display.WHITE)
        display.drawText("A to restart", 10, 30, display.WHITE)
    
        
    # Update the display to show what we drew
    display.update()