import sensor, image, time, lcd, gc, cmath
from maix import KPU
from machine import UART
lcd.init()
lcd.clear(lcd.RED)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(False)
sensor.set_hmirror(False)
sensor.skip_frames(time = 1000)
clock = time.clock()
print("ready load model")
labels = ["tu","da","wang"]
anchor = (1.99, 1.26, 2.61, 2.18, 3.70, 1.92, 3.67, 2.80, 5.35, 2.79)
kpu = KPU()
kpu.load_kmodel('/sd/det.kmodel')
kpu.init_yolo2(anchor, anchor_num=(int)(len(anchor)/2), img_w=320, img_h=240, net_w=320 , net_h=240 ,layer_w=10 ,layer_h=8, threshold=0.6, nms_value=0.3, classes=len(labels))
uart = UART(UART.UART2, baudrate=115200)
unicode_map = {
	"wang": ord("王"),
	"tu": ord("土"),
	"da": ord("大")
}
while(True):
	gc.collect()
	clock.tick()
	img = sensor.snapshot()
	kpu.run_with_output(img)
	dect = kpu.regionlayer_yolo2()
	fps = clock.fps()
	if len(dect) > 0:
		for l in dect:
			if l[5] > 0.7:
				a = img.draw_rectangle(l[0], l[1], l[2], l[3], color=(0, 255, 0))
				info = "%s %.3f" % (labels[l[4]], l[5])
				a = img.draw_string(l[0], l[1], info, color=(255, 0, 0), scale=2.0)
				print(info)
				label = labels[l[4]]
				if label in unicode_map:
					unicode_dec = unicode_map[label]
					uart.write("{}".format(unicode_dec))       #在串口助手上发送数据慢，将uart.write函数提前，先传数据再考虑延时
					time.sleep(0.5)


				del info
	a = img.draw_string(0, 0, "%2.1ffps" % (fps), color=(0, 60, 255), scale=2.0)
	lcd.display(img)