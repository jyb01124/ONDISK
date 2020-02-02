import cv2, time, os
import numpy as np

class video_thumbnail_make:
    def __init__(self):
        pass

    def set_file(self, name, path):
        self.file_name = name
        self.file_path = path
        self.v_name = self.file_path + "\\" + self.file_name

    def one_chTothree_ch(self, one_ch_int_img):
        return cv2.merge((one_ch_int_img, one_ch_int_img, one_ch_int_img))
    
    def video_init(self):
        self.resizeHeight = 150
        self.resizeWidth = 300

        self.page = 11
        self.cap = cv2.VideoCapture(self.v_name)
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.devide = int(self.length / (self.page-1))    
        
        _, tmp_frame = self.cap.read()

        self.total_edge = self.one_chTothree_ch(np.zeros((100,600), dtype=tmp_frame.dtype))
        self.black_img = self.one_chTothree_ch(np.zeros((50,300), dtype=tmp_frame.dtype))

    def run(self):
        v_pic_past = None
        for i in range(0,int(self.page/2)):
            H_pic = []
            for j in range(2*i+1,2*(i+1)+1):    
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, (j)*self.devide+1)
                ret, frame = self.cap.read()
                frame = cv2.resize(frame, (self.resizeWidth, self.resizeHeight), interpolation=cv2.INTER_CUBIC)
                frame = np.vstack([frame, self.black_img])
                FrameNumber2Time = time.strftime("%M:%S", time.gmtime(int(self.cap.get(cv2.CAP_PROP_POS_MSEC)/1000)))
                cv2.putText(frame, FrameNumber2Time, (10, 175), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255,255,255))
                H_pic.append(frame)
            H_complete = cv2.hconcat(H_pic)
            if i == 0:
                v_pic_past = H_complete
                continue
            v_pic_past = cv2.vconcat([v_pic_past, H_complete])

        total_pic = np.vstack([self.total_edge, v_pic_past])
        cv2.putText(total_pic, "Name : "+self.file_name, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(total_pic, "Size : "+str(os.path.getsize(self.v_name)), (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(total_pic, "ONDISK jyb01124", (5, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

        return total_pic

    def img_save(self, img, name):
        name = name + ".jpg"
        cv2.imwrite(name, img)