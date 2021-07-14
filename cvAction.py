import cv2

from PySide6.QtGui import QImage
import numpy as np


class CvAction:
    def __init__(self):
        pass

    def loadImage(self, path):
        self.matOriginalImg = cv2.imread(path)
        #cv2.imshow('image', self.matOriginalImg)
        # cv2.waitKey(0)

    def getMat(self):
        return self.matOriginalImg

    @staticmethod
    def cvToQImage(cvImg):
        height, width, channel = cvImg.shape
        rgb_image = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        bytesPerLine = 3 * width
        qImg = QImage(rgb_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg

    @staticmethod
    def templateMatching(source, template):
        img_rgb = source.copy()
        # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        cv2.imshow("img_rgb", img_rgb)
        cv2.waitKey(0)
        cv2.imshow("template", template)
        cv2.waitKey(0)
        h, w = template.shape[:2]
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            cv2.imshow("detected image", img_rgb)
            cv2.waitKey(0)

    @staticmethod
    def compareMat(image_1, image_2):
        # TODO: check if it works
        # reject if sizes are different
        height1, width1, _ = image_1.shape
        height2, width2, _ = image_2.shape
        if height1 != height2 or width1 != width2:
            return 1000
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])
        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = \
        cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff

    @staticmethod
    def pixelCompareMat(img1, img2):
        if img1.shape == img2.shape:
            #cv2.imshow("img1",img1)
            #cv2.imshow("img2",img2)
            dst = cv2.bitwise_xor(img1, img2)
            #cv2.imshow("dst",dst)
            gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
            count=cv2.countNonZero(gray)
            print(count)
            if count>0:
                return count
            else:
                return 0

        else:
            return 100
