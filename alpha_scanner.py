import cv2.cv as cv
import DynamsoftBarcodeReader

# All supported Barcode type
formats = {0x1FFL : "OneD",0x1L   : "CODE_39",0x2L : "CODE_128",0x4L   : "CODE_93",0x8L : "CODABAR",0x10L   : "ITF",0x20L :"EAN_13",0x40L   : "EAN_8",0x80L : "UPC_A",0x100L   : "UPC_E",}

title = "Dynamsoft Barcode Reader"
# Create a window with OpenCV
cv.NamedWindow(title, 1)
capture = cv.CaptureFromCAM(0)

is_saved = False
is_camera_paused = False
line_type = cv.CV_AA
font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX,
                          0.1, 1, 1, 1, line_type)
key_code = -1
fileName = '/home/caratred/test.jpg'

while True:
    if is_camera_paused:
        if not is_saved:
            is_saved = True
            # Capture a frame from Webcam
            img = cv.QueryFrame(capture)

            # fileName = 'dynamsoft_barcode_test.jpg'
            # img = cv.LoadImage('dynamsoft_barcode_test.jpg')
            # Save captured frame to local disk
            cv.SaveImage(fileName, img)
            # Decode the captured image by Dynamsoft Barcode library
            results = DynamsoftBarcodeReader.decodeFile(fileName)
            print (results)

            top = 30
            increase = 20

            if results:
                for result in results:
                    barcode_format = "Format: " + formats[result[0]]
                    barcode_value = "Value: " + result[1]

                    # Draw text
                    cv.PutText(img, barcode_format,
                                  (10, top), font, (254, 142, 20))
                    top += increase
                    cv.PutText(img, barcode_value,
                                  (10, top), font, (254, 142, 20))
                    top += increase
                    cv.PutText(img, "************************",
                                  (10, top), font, (254, 142, 20))
                    top += increase

            # Display Webcam preview
            cv.ShowImage(title, img)
    else:
        img = cv.QueryFrame(capture)
        cv.ShowImage(title, img)

    key_code = cv.WaitKey(10)
    if key_code != -1:
        print (key_code)

    if key_code == 27: # 27 => ESC
        break
    elif key_code == 13: # 13 => Enter
        if is_camera_paused:
            is_camera_paused = False
        else:
            is_camera_paused = True
            is_saved = False

cv.DestroyAllWindows()
