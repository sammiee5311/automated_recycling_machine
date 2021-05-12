import cv2
import json
import numpy as np
import socket
import struct
from collections import defaultdict
from typing import Dict, List, Any

##################################################
from yolo_module import Object_Detection
##################################################


class Recycling:
    def __init__(self, info: Dict[str, Dict[str, List[str, str]]]) -> None:
        self.info = info
        self.classes = {0: 'PET plastic_bottle with_label',  1: 'PAPER coffee_cup without_cap',
                        2: 'PET plastic_bottle with_label', 3: 'PET plastic_bottle without_label',
                        4: 'CAN drink_can crushed', 5: 'CAN drink_can no_crushed'}
        self.object_cnt = defaultdict(int)
        self.reward = 0
        self.OD = Object_Detection()
        self.connection = None
        self.start_socket()

    def start_socket(self) -> None:
        IP, PORT = '', 1234
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("waiting for connection")
        server_socket.bind((IP, PORT))
        server_socket.listen(1)
        self.connection, _ = server_socket.accept()

    def recvall(self, sock: Any, count: int) -> bytes:
        buf = b''
        while count:
            new_buf = sock.recv(count)
            if not new_buf:
                return None
            buf += new_buf
            count -= len(new_buf)
        return buf

    def start_capturing(self) -> None:
        while True:
            length = self.recvall(self.connection, 16)
            string_data = self.recvall(self.connection, int(length))
            data = np.frombuffer(string_data, dtype='uint8')
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            img = self.get_info(frame)
            cv2.imshow('img', img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    def get_info(self, img: np.ndarray[np.int64]) -> np.ndarray[np.int64]:
        changed_img, object_x, object_y, object_w, object_h, class_id = self.OD.detect_object(img)
        if class_id != -1 and (object_x != -1 or object_y != -1 or object_w != -1 or object_h != -1):
            cv2.putText(changed_img, self.classes[class_id], (object_x - 10, object_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

            self.object_cnt[class_id] += 1

            idx = max(self.object_cnt, key=lambda key: self.object_cnt[key])

            if self.object_cnt[idx] > 30:
                detected_object = self.classes[idx]
                string = detected_object.split(' ')
                self.reward += int(self.info[string[0]][string[1]][1])
                self.connection.send(struct.pack('f', (idx+1)*1000 + self.reward))
                self.object_cnt.clear()
            else:
                self.connection.send(struct.pack('f', -1))

            return changed_img

        self.connection.send(struct.pack('f', -1))
        return img


if __name__ == '__main__':
    with open("./recycle_information.json", 'r', encoding='UTF-8') as file:
        info = json.load(file)
        
    recycle = Recycling(info)
    recycle.start_capturing()

