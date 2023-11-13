import turtle


def draw_text_formation(string_array):
   turtle.setup(width=1400, height=100)  # Set the window width to 1400 pixels


   turtle.hideturtle() # hide turtle
   turtle.speed(0)


   window_width = turtle.window_width() # Get the window width
   window_height = turtle.window_height() # Get the window height
   turtle.penup() # Pull the pen up
   # Set the initial position of the turtle
   turtle.goto(-window_width / 2 + 30, -window_height / 2 + 30)
   turtle.pendown() # Pull the pen down


   for string in string_array:
       start_position = turtle.position()  # Store the starting position of the string
      
       for char in string:
           if char == 'u':
               turtle.setheading(90)  # Face upwards
               turtle.forward(3)     # Move up by 3 units
           elif char == 'r':
               turtle.setheading(0)   # Face right
               turtle.forward(3)     # Move right by 3 units
           elif char == 'd':
               turtle.setheading(270) # Face downwards
               turtle.forward(3)     # Move down by 3 units
           elif char == 'l':
               turtle.setheading(180) # Face left
               turtle.forward(3)     # Move left by 3 units
      
       # Teleport to the right while maintaining the y-axis position
       turtle.penup()
       turtle.goto(start_position[0] + 30, start_position[1])
       turtle.pendown()
  
   turtle.done()


# read string from cmd file where splitted by new line
strings = []
with open('cmd.txt', 'r') as f:
   for line in f:
       strings.append(line.strip())


draw_text_formation(strings)