from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2 as cv
import numpy as np



# img = qrcode.make("Hello World")
# print(type(img))
# img.save("Hello_World.jpg")

def capture(kDist, kWidth, ctr):
    cap = cv.VideoCapture(1)
    detector = cv.QRCodeDetector()
    while (True):
        ret, img = cap.read()
        # data, one, _ = detector.detectAndDecode(frame)
        for barcode in decode(img, symbols=[ZBarSymbol.QRCODE]):
            myData = barcode.data.decode('utf-8')
            # print(barcode)
            # print(barcode.data)
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv.polylines(img, [pts], True, (255,0,255),5)
            pts2 = barcode.rect
            # print(pts2)
            # print(pts2.width)
            if (ctr == 1):
                f = focalLength(kDist, kWidth, pts2.width)
                ctr+=1
            d = findDistance(f, kWidth, pts2.width)
            # print(pts2)
            cv.putText(img, str(d), (pts2[0], pts2[1]), cv.FONT_HERSHEY_COMPLEX,
                        0.9, (255,0,255),3)
        cv.imshow('Frame', img)
        # cv.imshow('Data',frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        if not ret:
            print("Can't retrieve frame - stream may have ended. Exiting..")
            break
    cap.release()
    cv.destroyAllWindows()

def focalLength(kDist, kWidth, Width):
    fLength = ((Width * kDist) / kWidth)
    return fLength
def findDistance(f, kWidth, Width):
    d = ((kWidth * f) / Width)
    return d
def main():
    ctr=1
    kDist = 20
    kWidth = 10
    capture(kDist, kWidth, ctr)

if __name__ == "__main__":
    main()