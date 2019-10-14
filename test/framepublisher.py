import zmq
import sys
import time
import glob

class ImagesFromDirectorySource:
    def __init__(self, src_path, interval=1):
        img_files =  glob.glob(src_path+'/*.jpg')
        self.imgs = []
        self.img_names = []
        self.interval = interval
        for f in img_files:
            self.img_names.append(f)
            self.imgs.append( open(f, 'rb').read() )

    def get_frame(self):
        time.sleep(self.interval)
        image_index = int(time.time()%3)
        print("Sending ", self.img_names[image_index])
        return self.imgs[image_index]

class ZMQFramePublisher:
    def __init__(self, source, endpoint="tcp://127.0.0.1:5600"):
        self.source = source
        self.endpoint = endpoint    
    def run(self):
        context = zmq.Context()
        sock = context.socket(zmq.PUB)        
        sock.bind(self.endpoint)
        while True:
            sock.send(self.source.get_frame())

if __name__ == "__main__":
    try:
        image_player=ImagesFromDirectorySource(src_path='data', interval=1)
        server = ZMQFramePublisher(            
            source=image_player,
            endpoint="tcp://127.0.0.1:5600"
        )
        server.run()
    except KeyboardInterrupt:
        pass
    print("Leaving")
