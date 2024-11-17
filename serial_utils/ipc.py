import struct, time, os, sys

class NamedPipe:
    def __init__(self, right_hand=True):
        if right_hand:
            self.pipename = '/tmp/vrapplication_input_right'
        else:
            self.pipename = '/tmp/vrapplication_input_left'
        self.fingers = [False]*5
        self.joys = [0.0, 0.0]
        self.buttons = [False]*8

        # Create named pipe if it doesn't exist
        if not os.path.exists(self.pipename):
            os.mkfifo(self.pipename)

    def encode(self, flexion, joys=None, bools=None):
        if joys is not None:
            print(joys)
            joyX = joys[0]
            joyY = joys[1]
        else:
            joyX = 0.0
            joyY = 0.0
        
        if bools is None:
            bools = [False, False, False, False, False, False, False, False] 

        pack_obj = struct.pack('@5f', flexion[0], flexion[1], flexion[2], flexion[3], flexion[4])
        joys = struct.pack('@2f', joyX, joyY)
        pack_bools = struct.pack('@8?', *bools)
        pack_obj = pack_obj + joys + pack_bools
        return pack_obj

    def send(self, fingers, joys=None, bools=None):
        encoded = self.encode(fingers, joys, bools)
        try:
            with open(self.pipename, 'wb') as pipe:
                pipe.write(encoded)
        except OSError as e:
            print(f"Pipe error: {e}")

if __name__ == "__main__":
    ipc_right = NamedPipe(right_hand=True)
    ipc_left = NamedPipe(right_hand=False)

    try:
        for i1 in range(0,10):
            for i2 in range(0,10):
                for i3 in range(0,10):
                    for i4 in range(0,10):
                        for i5 in range(0,10):
                            fingers = [i1/10, i2/10, i3/10, i4/10, i5/10]
                            bools = [True]*8
                            bools[6] = True
                            ipc_left.send(fingers, bools=bools)
                            ipc_right.send(fingers, bools=bools)
                            
                            time.sleep(0.01)
                            print(f"Wrote {fingers} to IPC")
    except KeyboardInterrupt:
        print("Quitting")
        quit()