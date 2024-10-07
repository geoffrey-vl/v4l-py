from linuxpy.video.device import Device, VideoCapture, PixelFormat

EXPOSURE_MODE_MANUAL = 1
EXPOSURE_MODE_AUTO = 3
EXPOSURE_MODES = [EXPOSURE_MODE_MANUAL, EXPOSURE_MODE_AUTO]

def printInfo(cam):
    print("---- FILE -------------------------")
    print(cam.filename)
    print("---- INFO -------------------------")
    print(cam.info)
    print("---- FORMATS -------------------------")
    for format in cam.info.frame_sizes:
        print(format)
    print("---- CONTROLS -------------------------")
    for control in cam.controls.values():
        print(control)


def setAutoExposure(cam, mode):
    if mode not in EXPOSURE_MODES:
        raise Exception("illegal value")
    for control in cam.controls.values():
        if control.config_name != "auto_exposure":
            continue
        control.value = mode
        print(control)
        return
    raise Exception("no such control 'auto_exposure'")

def setDynamicFramerate(cam, value: bool):
    for control in cam.controls.values():
        if control.config_name != "exposure_dynamic_framerate":
            continue
        control.value = value
        print(control)
        return
    raise Exception("no such control 'exposure_dynamic_framerate'")

# in 100us units
def setExposure(cam, value: int):
    for control in cam.controls.values():
        if control.config_name != "exposure_time_absolute":
            continue
        if value < control.minimum:
            raise Exception("illegal value for control 'exposure_dynamic_framerate'")
        if value > control.maximum:
            raise Exception("illegal value for control 'exposure_dynamic_framerate'")
        control.value = value
        print(control)
        return
    raise Exception("no such control 'exposure_time_absolute'")

with Device.from_id(0) as cam:
    printInfo(cam)
    print("---- SETP -------------------------")
    capture = VideoCapture(cam)
    capture.set_format(1280, 720, "MJPG")
    setAutoExposure(cam, EXPOSURE_MODE_MANUAL)
    setDynamicFramerate(cam, False)
    setExposure(cam, 626)
    print("---- CAPTURE -------------------------")
    with capture: # opens camera
        cnt = 0
        for frame in capture: # start frame capturing
            cnt = cnt+1
            if cnt == 1:
                continue # drop first frame
            print(f"w={frame.width}, h={frame.height}, bytes={frame.nbytes}")
            file = open(f'picture{cnt}.jpg', 'wb')
            file.write(frame.data)
            file.close()
            if cnt == 2:
                break