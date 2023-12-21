import cv2
import numpy as np
import socket
import struct




class UDPClient:
    
    ret=1
    frame=1
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 최대 청크 크기 정의
        self.MAX_CHUNK_SIZE = 65507  # UDP 페이로드의 최대 크기

        # 크기 조절을 위한 목표 폭 및 높이 정의
        self.TARGET_WIDTH = 320
        self.TARGET_HEIGHT = 240
        self.ret=1
        self.frame
        # 라즈베리 파이 카메라 모듈을 사용하여 비디오 캡처 시작
        self.cap = cv2.VideoCapture(0)  # 0은 라즈베리 파이 카메라 모듈을 나타냅니다.


    def send_webcam_frame_to_server(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("에러: 프레임 캡처 실패")
                continue

            # 프레임이 비어 있는지 확인
            if frame is None:
                print("에러: 빈 프레임")
                continue

            # 프레임 크기 조절
            frame = cv2.resize(frame, (udp_client.TARGET_WIDTH, udp_client.TARGET_HEIGHT))

            # 프레임을 JPEG로 압축하여 바이트로 변환
            _, img_encoded = cv2.imencode('.jpg', frame)

            # 이미지 크기 정보를 추가하여 전송
            img_size = len(img_encoded)
            packed_size = struct.pack("!I", img_size)

            # 이미지 데이터를 청크로 분할
            img_bytes = img_encoded.tobytes()
            for i in range(0, len(img_bytes), udp_client.MAX_CHUNK_SIZE):
                chunk = img_bytes[i:i + udp_client.MAX_CHUNK_SIZE]

                # 각 청크에 이미지 크기 정보 추가
                img_data = packed_size + chunk

                # UDP로 프레임 청크 전송
                udp_client.client_socket.sendto(img_data, (UDP_IP, UDP_PORT))

                # 각 청크마다 전송된 바이트 수 출력
                print(f"전송된 바이트 수: {len(img_data)}")

            # 영상 표시 (옵션)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        

    def close_connection(self):
        self.client_socket.close()
        self.cap.release()
        cv2.destroyAllWindows()






UDP_IP = "10.10.15.58"
UDP_PORT = 12345

udp_client = UDPClient(UDP_IP,UDP_PORT)

udp_client.send_webcam_frame_to_server()
