import qrcode
import cv2 as cv


img = qrcode.make("Hello World")
print(type(img))
img.save("Hello_World.jpg")