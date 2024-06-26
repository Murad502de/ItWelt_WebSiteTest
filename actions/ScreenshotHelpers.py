import cv2
import time
import numpy as np
from skimage.metrics import structural_similarity as ssim


class ScreenshotActions:
    def __init__(self, driver):
        self.driver = driver

    def open_page(self, url):
        self.driver.get(url)

    def take_screenshot(self, output_file):
        self.driver.save_screenshot(output_file)

    def take_screenshot_with_size(self, url, width, height, output_file):
        self.driver.set_window_size(width, height)
        self.driver.get(url)
        time.sleep(3)  # Даем время на загрузку страницы
        self.driver.save_screenshot(output_file)

    def compare_images(self, img_path1, img_path2):
        # Загрузка изображений
        imageA = cv2.imread(img_path1)
        imageB = cv2.imread(img_path2)

        # Преобразование изображений в черно-белый формат
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        # Вычисление структурного сходства (SSIM)
        score, diff = ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")

        print(f"SSIM: {score}")

        # Пороговая обработка различий
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Подсветка различий
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return score, imageA, imageB, diff
