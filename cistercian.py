# Cistercian number converter
#
# https://en.wikipedia.org/wiki/Cistercian_numerals

from PIL import Image, ImageDraw
import sys



# check a value has been given as an argument
if len(sys.argv)<2:
    number=0
    print("Give a number between 0 - 9999 as an argument")
else:
    if str(sys.argv[1]).isnumeric():
        number = int(sys.argv[1])
    else:
        number = 0
if number>9999:
    number =9999

# The number should now be an actual number to work with...
width =-1
bg = (255,255,255)
fg = (0,0,0)
# let's check the arguments for a -w flag and set the width
for i in range(len(sys.argv)):
    if sys.argv[i] == "-w" and len(sys.argv)>i+1:
        if str(sys.argv[i+1]).isnumeric():
            if int(str(sys.argv[i+1]))>49 and int(str(sys.argv[i+1]))<10001: # limits of image width allowed
                width = int(sys.argv[i+1])
            else:
                width=-1

    if sys.argv[i] == "-fg" and len(sys.argv)>i+1:
        rgb = sys.argv[i+1]
        try:
            fR, fG, fB = [int(c) for c in rgb.split(',')]
            fg = -1
        except:
            print("RGB Foreground format not correct - eg: 0,0,0. Default of 0,0,0 used.")

    if sys.argv[i] == "-bg" and len(sys.argv)>i+1:
        rgb = sys.argv[i+1]
        try:
            bR, bG, bB = [int(c) for c in rgb.split(',')]
            bg = -1
        except:
            print("RGB Background format not correct - eg: 255,255,255. Default of 255,255,255 used.")

# setup width of final image to output
if width == -1:
    width = 800 # default
height = int(width * 1.25)
pen_size = int(width /4)
pen_width = int(width/16)

# Colours of the output image
#bg = (255,255,255)

if fg == -1:
    fg = (fR,fG,fB)
else:
    fg = (0,0,0)

if bg == -1:
    bg = (bR,bG,bB)
else:
    bg = (255,255,255)
	
    
string_num = "0"*(4-len(str(number)))+str(number)

# Convert the number to thousands, hundreds, tens and units...
full = [int(string_num[0])*1000,int(string_num[1])*100,int(string_num[2])*10,int(string_num[3])]

# A dictionary for each individual number. The coordinates are basic XY, to be multiplied later.
c_num = {1:[(0,0),(1,0)],2:[(0,1),(1,1)],3:[(0,0),(1,1)],4:[(0,1),(1,0)],5:[(0,1),(1,0),(0,0)],6:[(1,0),(1,1)],7:[(0,0),(1,0),(1,1)],8:[(0,1),(1,1),(1,0)],9:[(0,0),(1,0),(1,1),(0,1)],
         10:[(-1,0),(0,0)],20:[(-1,1),(0,1)],30:[(0,0),(-1,1)],40:[(-1,0),(0,1)],50:[(0,0),(-1,0),(0,1)],60:[(-1,0),(-1,1)],70:[(0,0),(-1,0),(-1,1)],80:[(-1,0),(-1,1),(0,1)],90:[(0,0),(-1,0),(-1,1),(0,1)],
         100:[(0,3),(1,3)],200:[(0,2),(1,2)],300:[(0,3),(1,2)],400:[(0,2),(1,3)],500:[(0,3),(1,3),(0,2)],600:[(1,2),(1,3)],700:[(0,3),(1,3),(1,2)],800:[(0,2),(1,2),(1,3)],900:[(0,2),(1,2),(1,3),(0,3)],
         1000:[(-1,3),(0,3)],2000:[(-1,2),(0,2)],3000:[(-1,2),(0,3)],4000:[(-1,3),(0,2)],5000:[(0,3),(-1,3),(0,2)],6000:[(-1,2),(-1,3)],7000:[(-1,2),(-1,3),(0,3)],8000:[(0,2),(-1,2),(-1,3)],9000:[(0,2),(-1,2),(-1,3),(0,3)],
         0:[(0,0)]}

# Create a new image to draw on
img = Image.new('RGB',(width,height),color = bg)
draw = ImageDraw.Draw(img)

# Draw the centre line. Back and forward to get rounded ends! PIL....
new_draw_points=[pen_size*2,pen_size,pen_size*2,pen_size*4,pen_size*2,pen_size,pen_size*2,pen_size*4]
draw.line(new_draw_points,width=pen_width,fill = fg,joint = "curve")

# Iterate through every number to render
for num in full:

    
    raw_points =c_num[num]
    draw_points =[(x*pen_size) for i in raw_points for x in i]
    new_draw_points = [0]*len(draw_points)
    # Scale all the points for the image
    new_draw_points[0::2] = [i+(pen_size*2) for i in draw_points[0::2]]
    new_draw_points[1::2] = [i+(pen_size) for i in draw_points[1::2]]
    # draw the now scaled lines
    draw.line(new_draw_points,width=pen_width,fill = fg,joint = "curve")

    # Now get each XY coordinate and draw a circle at each point to get rounded edges. PIL........
    t=0
    for i in range(len(new_draw_points)-1):
        if t==0:
            x=new_draw_points[i]
            y=new_draw_points[i+1]
            #print(x,y)
            draw.ellipse((x-int(pen_width/2),y-int(pen_width/2),x+int(pen_width/2),y+int(pen_width/2)), fill = fg)
            t=1
        else:
            t=0 # Skip every other one.

# Output the image
img.save(string_num+".png","png")
