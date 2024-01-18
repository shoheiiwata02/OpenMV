import sensor,image,time,math
import pyb,struct

uart = pyb.UART(1,9600, timeout=1000)
uart.init(9600, bits=8, parity=None, stop=1)

red_threshold1 = (0, 100, 18, 127, -8, 127)
Width = 180
Height = 180

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
sensor.set_windowing((Width,Height))
sensor.set_auto_gain(True, gain_db_ceiling=16.0)
clock = time.clock()

#K = 70 * 2  #（定数）焦点距離　K=直径/px & K=距離(㎝)＊Rpix
    #50cmの時28,28.5    70cm(19.5)


while(True):
    clock.tick()
    img = sensor.snapshot()#.lens_corr(1.8)
    blobs = img.find_blobs([red_threshold1])
    length = 0

    for c in img.find_circles(threshold = 4000, x_margin = 10, y_margin = 10, r_margin = 1900):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255,0,0))


        if len(blobs) == 1:
            b = blobs[0]
            img.draw_rectangle(b[0:4])
            img.draw_cross(b[5], b[6])
            Rpix = (b[2]+b[3])/2 #画面に映る円の直径ピクセル

            const_cm = 11 / Rpix #px->cmの変換係数

            obj_center_x_px = b.cx() - (Width/2)
            obj_center_y_px = b.cy() - (Height/2)

            obj_center_x = obj_center_x_px * const_cm
            obj_center_y = obj_center_y_px * const_cm

            offset_y = obj_center_y - 10

            length = math.sqrt((obj_center_x ** 2) + (offset_y ** 2))

            #bytesに変換
            length_bytes = struct.pack('<f', length)
            # 2つのデータを1つのバイト列に結合して返す
            #packed_data = struct.pack('<ff', red_circle, length)
            uart.write(length_bytes)
            #uart.write(packed_data)
            #print(length_bytes)
#            print(length_bytes)



#    print("FPS %f" % (clock.fps()))
