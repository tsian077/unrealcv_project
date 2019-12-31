from unrealcv import client

trajectory = []



if __name__ == '__main__':
   
    client.connect()
    print("connect....after 3s start record camera_trajectory")
    #延遲三秒後開始
    time.sleep(3)
    # client.message_handler = message_handler
    for i in range(1,100):
        time.sleep(0.5)
        rot = [float(v) for v in client.request('vget /camera/0/rotation').split(' ')]
        loc = [float(v) for v in client.request('vget /camera/0/location').split(' ')]
        print("rot:",rot,"loc",loc)
        trajectory.append(dict(rotation = rot, location = loc))

    if not client.isconnected():
        print('Can not connect to the game, please run the game downloaded from http://unrealcv.github.io first')
    else:
        time.sleep(5)


