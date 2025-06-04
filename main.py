import math, time
 
# importing cv2 
import cv2 

import numpy as np
# black blank image
image = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
 
# Window name in which image is displayed
window_name = 'Image'

# Green color in BGR
color = (255, 255, 255)

# Line thickness of 9 px
thickness = 3

arm_length = [200,200,100]
arm_angle = -45

cv2.imshow(window_name, image)

x=0
y=0

def calculate(l1,l2,l4,arm3_angle,pos):
	global arm_target,l3
	arm_offset_x = l4*math.cos(math.radians(arm3_angle))
	arm_offset_y = l4*math.sin(math.radians(arm3_angle))
	arm_target = [pos[0]-arm_offset_x,pos[1]-arm_offset_y]
	l3 = math.dist(arm_target,[0,0])
	#print("[pos[0]-50,pos[1]-50]:", [pos[0]-50,pos[1]-50])
	print("arm_target:",arm_target)
	print("l3:",l3)
	angle_c = math.acos(-((l3*l3)-(l1*l1)-(l2*l2))/(2*l1*l2))
	angle_b = math.asin(l2*(math.sin(angle_c)/l3))
	print("angle_c",math.degrees(angle_c),"angle_b",math.degrees(angle_b))
	return math.degrees(angle_b),math.degrees(angle_c)
def find_endpoint(start_pos,angle,length):
	angle = math.radians(angle)
	x = length*math.cos(angle)
	y = length*math.sin(angle)
	return (int(start_pos[0]+x),int(start_pos[1]+y))
#position = str(input("Enter Target position: "))
#position = position.split(',')
#input_pos = [int(position[0]),int(position[1])]
def mouse_click(event, mx, my, flags, param):
	global x,y 
	x = mx
	y = my
	#image = cv2.circle(image, (int(arm_target[0]),int(arm_target[1])), 20, color, thickness)

# Displaying the image 

cv2.setMouseCallback(window_name, mouse_click) 
while True:
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
	elif key == ord('w'):
		arm_angle+=1
	elif key == ord('s'):
		arm_angle-=1
	time.sleep(0.05)
	image = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
	#if event == cv2.EVENT_LBUTTONDOWN: 
	try:
		angle1,angle2 = calculate(arm_length[0],arm_length[1],arm_length[2],arm_angle,[x,y])
	except ValueError:
		print ("Math Error")
	print("mouse:",[x,y])
	angle3 = math.degrees(math.atan(arm_target[1]/arm_target[0]))
	joint1 = (find_endpoint([0,0],angle1+angle3,arm_length[0]))
	joint2 = (find_endpoint(joint1,(angle1+angle3)-(180-angle2),arm_length[1]))
	print("joint1:",joint1,"joint2:",joint2)
	image = cv2.line(image, (0,0), joint1, color, thickness)
	image = cv2.line(image, joint1, joint2, color, thickness)
	image = cv2.line(image, joint2, find_endpoint(joint2,arm_angle,arm_length[2]), color, thickness)
	image = cv2.line(image, (0,0), find_endpoint((0,0),angle3,l3), color, 1)
	image = cv2.circle(image, (x,y), 20, color, thickness)
	cv2.imshow(window_name, image) 
cv2.destroyAllWindows()
