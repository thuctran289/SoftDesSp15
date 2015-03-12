import cv2
import numpy as np
import time
"""
We are using global variables such as frame for this program. 
"""

#Represents the drawing point
class Point():
    """
    Defines a class for the characteristics of the drawing pen
    """
    def __init__(self, x,y,r):
        self.x = x
        self.y = y
        self.r = r

#Represents the bright sources of light
class Light():
    """
    Defines a class for the parts of the 'frame' image that make it through the color filter
    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

#Represents the interactive buttons
class CommandBox(object):
    """
    Defines a base class for different ways for light to interact with a screen. Defines a box where a command can be activated.
    """
    def __init__(self, x, y, w, h,box_bgr):
        """
        Initializes the box's position, size, and color. Will be overwritten in further base classes for more particular roles.
        x,y is lowerleft corner. w,h are width and height, and box_bgr is the color of the box. 
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h 
        self.box_bgr = box_bgr

    def display_box(self):
        """
        This displays to the global frame variable. Just draws the different displays barring other specific requirements. 
        """
        #Uses opencv to write a rectangle to. 
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)

    def inframe(self, point):
        """
        Checks to see if a point is in the frame of the CommandBox.
        """
        #Checks to see if a point is in the range of the box. 
        if self.x-25<= point.x <= self.x+self.w-25:
            if self.y-25<=point.y<=self.y + self.h-25:
                return True
        else:
            return False

#Represents the color-deciding box
class ColorBox(CommandBox):
    """
    Defines the box for figuring out a color, and keeping a record for what color a user is drawing with currently. 
    """
    def __init__(self, x, y, w, h, box_bgr, draw_bgr):
        """
        Like super, with the addition of having a draw_bgr.
        """
        self.draw_bgr = draw_bgr
        super(ColorBox, self).__init__(x,y,w,h,box_bgr)
    def set_draw_color(self, color_segment):
        """
        Finds the average color over a section the size of frame color_segment. 
        """
        #Splits the color_segment into the three color channels. 
        b,g,r = cv2.split(color_segment)
        #Averages the channels to determine the average value of that channel over the frame.
        #Sets draw_bgr to each of those channels. 
        self.draw_bgr[0] = np.average(b)
        self.draw_bgr[1] = np.average(g)
        self.draw_bgr[2] = np.average(r)
    def display_box(self, r):
        """color_segment = frame[color_box.y : color_box.y+color_box.h, color_box.x : color_box.x+color_box.w]
    
        draws the rectangular frame that corresponds to the ColorBox. Additionally draws a circle on the frame that indicates the size and color of new points drawn onto the 
        surface. 
        """
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.circle(frame, (100, 100), r, color_box.draw_bgr, -1)

#Represents the reset button
class ResetBox(CommandBox):
    """
    This class is used for resetting the screen of all points. Uses the inframe function of CommandBox that it inherits from. 
    """
    def display_box(self):
        """
        Displays the rectangle that corresponds to the location of ResetBox. Additionally draws a letter R for reset on the box. 
        """
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.putText(frame, "R",(self.x,self.y+self.h), cv2.FONT_HERSHEY_SIMPLEX, 2, 0)
    def check_reset(self,pointer, point_array):
        """
        This checks for a pointer in the box, if there is a pointer, than the input point_array is cleared. Otherwise, it just returns point_array as is.
        """
        if self.inframe(pointer):
            return []
        else:
            return point_array

#Represents the radius changing buttons
class RadiusBox(CommandBox):
    """
    This class determines how one controls the size of the draw radius. 
    """
    def __init__(self, x, y, w, h,box_bgr,r):
        """
        This initializes a box similar to any other box, but with the addition of an additional variable r for radius.
        """
        super(RadiusBox,self).__init__(x,y,w,h,box_bgr)
        self.r = r

    def display_box(self):
        """
        This function displays the two parts of a radius_box. The first part corresponds to the region for incrementing radius, the second for decrementing radius. 
        The function also prints a plus or minus depending on operation for each part. 
        """
        #For increments.
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.putText(frame, "+",(self.x,self.y+self.h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        #For decrements.
        cv2.rectangle(frame, (self.x+self.w/2, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.putText(frame, "-",(self.x+self.w/2,self.y+self.h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

    def inframe(self, point):
        """
        This is a revised inframe specifically for changing radii. It essentially outputs -1 if the point is in the decrement box, 1 if in increment box, and 0 otherwise. 
        """
        if self.x-25<= point.x <= self.x+self.w/2-25:
            if self.y-25<=point.y<=self.y + self.h-25:
                return 1
        elif self.x+self.w/2-25<= point.x <= self.x+self.w-25:
            if self.y-25<=point.y<=self.y + self.h-25:
                return -1
        else:
            return 0

    def change_radius(self, pointer):
        """
        Function uses above inframe function to determine how to change radius.
        If the inframe returns 0, it doesn't change the radius, if 1 it increments its r, if -1 it decrements its r.
        """
        if self.inframe(pointer)== 0:
            pass
        elif self.inframe(pointer) ==1:
            self.r += 1
        elif self.inframe(pointer) ==-1:
            self.r -= 1
        if self.r<=1:
            self.r = 1


if __name__ == '__main__':
    #Start cam stream
    cap = cv2.VideoCapture(0)

    #Define camera characteristics
    frameWidth = cap.get(3)
    frameHeight = cap.get(4)

    #Create the pen
    pointer = Point(0, 0, 5)
    light = Light(0, 0, 0, 0)

    #Create the buttons
    color_box = ColorBox(0, int(frameHeight-100), 100, 100, [0, 0, 255],[0,0,0])
    radius_box = RadiusBox(int(frameWidth-150),int(frameHeight-50),100,50,[0,255,0],5)
    reset_box = ResetBox(int(frameWidth-50),int(frameHeight-50),50,50,[255,0,0])

    #Define color to select for in BGR
    lower_BGR = np.array([210, 150, 150])
    upper_BGR = np.array([255, 255, 255])

    #Instantiate the list of drawings
    points = []

    #Instantiate the while loop counter
    counter = 0

    while(1):
        #Set 'frame' as the current cam capture
        _, frame = cap.read()

        #Flip the frame over the vertical axis (so that it looks like looking into a mirror)
        frame = cv2.flip(frame, 1)

        #Find the average color of the ColorBox by getting frame of the color, and inputting into function. 
        color_segment = frame[color_box.y : color_box.y+color_box.h, color_box.x : color_box.x+color_box.w]
        color_box.set_draw_color(color_segment)

        #Guarantees a clean point each iteration on the loop
        pointer.x = 0
        pointer.y = 0
        pointer.r = 0

        #Blur the frame to blend colors
        blurframe = cv2.blur(frame, (50, 50))

        # Threshold the image to get only the selected colors
        mask = cv2.inRange(blurframe, lower_BGR, upper_BGR)
        contour_mask = mask
        cv2.imshow('mask', mask)

        #Create a contour around the selected colors
        contours,_ = cv2.findContours(contour_mask, 1, 2)

        #If there is a contour, add the position and current drawing color to a list
        if len(contours) > 0:
            cnt = contours[0]
            M = cv2.moments(cnt)

            #Define the color-tracked light source
            light.x, light.y, light.w, light.h = cv2.boundingRect(cnt)

            #Assign the position of the pointer
            pointer.x = light.x
            pointer.y = light.y
            pointer.r = radius_box.r

            #Add the pointer and color characteristics to a reference list
            new_color = [color_box.draw_bgr[0],color_box.draw_bgr[1],color_box.draw_bgr[2]]
            points.append([[pointer.x+light.w/2, pointer.y+light.h/2, pointer.r], new_color])

        #Slows down the speed at which the radius change button activates
        counter += 1
        if counter % 5 == 0:
            radius_box.change_radius(pointer)
        points = reset_box.check_reset(pointer, points)

        #If there is anything to be drawn, draw it!
        if len(points) > 0:
            for i in xrange(len(points)):
                cv2.circle(frame, (points[i][0][0], points[i][0][1]), points[i][0][2], (points[i][1][0], points[i][1][1], points[i][1][2]), -1)
        
        #Display the buttons
        color_box.display_box(radius_box.r)
        radius_box.display_box()
        reset_box.display_box()

        #Display the final image
        cv2.imshow('frame', frame)

        #If ESC pressed, quit the program
        if cv2.waitKey(1) & 0xFF == 27:
            break

    #Release the capture and close the windows
    cap.release()
    cv2.destroyAllWindows()
