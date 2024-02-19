import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Scale, Button, Entry, Label, Radiobutton, IntVar
import sys

class ImageProcessor:
    def __init__(self, root):
        #初期値の設定
        self.root = root
        self.image_path = None
        self.threshold_value = 70  # 2値化の閾値
        self.threshold1_value = 30  # Cannyエッジ検出低い閾値
        self.threshold2_value = 30  # Cannyエッジ検出高い閾値
        self.min_contour_area_value = 5  # 初期の最小輪郭面積
        self.morphology_threshold_value = 5  # 初期のモルフォロジー変換の閾値
        self.alert_threshold_area = 1000  # アラートを出す面積の閾値

        self.create_widgets()


    def create_widgets(self):
        # 画像ファイルを開くボタン
        self.open_button = Button(self.root, text="画像を選択", command=self.open_file)
        self.open_button.grid(row=0, column=0)

        # カメラを使用するか画像ファイルを使用するかを選択するラジオボタン
        self.selection_var = IntVar()
        self.selection_var.set(0)  # 初期値: 画像ファイルを選択
        self.radio_file = Radiobutton(self.root, text="画像ファイル", variable=self.selection_var, value=0)
        self.radio_file.grid(row=0, column=1)
        self.radio_camera = Radiobutton(self.root, text="カメラ", variable=self.selection_var, value=1)
        self.radio_camera.grid(row=0, column=2)

        # 画像パスの表示
        self.path_label = Label(self.root, text="画像パス:")
        self.path_label.grid(row=1, column=0, sticky="e")

        self.path_entry = Entry(self.root)
        self.path_entry.grid(row=1, column=1, columnspan=2, sticky="we")

        # 実行ボタン
        self.execute_button = Button(self.root, text="実行", command=self.process_image)
        self.execute_button.grid(row=8, column=0, columnspan=3)


        # 2値化の閾値のスライダー
        # 画像を2値化する際の閾値を調整します。閾値より大きい値は白に、小さい値は黒になります。
        self.threshold_slider = Scale(self.root, label="2値化の閾値", from_=0, to=255, orient=tk.HORIZONTAL)
        self.threshold_slider.set(self.threshold_value)
        self.threshold_slider.grid(row=2, column=0, columnspan=3, sticky="we")

        # Cannyエッジ検出の低い閾値のスライダー
        # エッジの検出感度が変化し、より多くのエッジが検出されるか、または検出されるエッジの種類が変わります。この閾値以下の勾配値はエッジではないと見なされます。
        self.threshold1_slider = Scale(self.root, label="Cannyエッジ検出の低い閾値", from_=0, to=255, orient=tk.HORIZONTAL)
        self.threshold1_slider.set(self.threshold1_value)
        self.threshold1_slider.grid(row=3, column=0, columnspan=3, sticky="we")

        # Cannyエッジ検出高い閾値のスライダー　
        # エッジの検出感度が変化し、エッジの検出に影響します。低い値ではノイズが含まれ、高い値ではエッジが欠落する可能性があります。この閾値以上の勾配値は確実にエッジと見なされます。
        self.threshold2_slider = Scale(self.root, label="Cannyエッジ検出の高い閾値", from_=0, to=255, orient=tk.HORIZONTAL)
        self.threshold2_slider.set(self.threshold2_value)
        self.threshold2_slider.grid(row=4, column=0, columnspan=3, sticky="we")

        # モルフォロジー変換の閾値のスライダー
        # ノイズの削減や輪郭の形状に影響が及びます。
        self.morphology_threshold_slider = Scale(self.root, label="モルフォロジー変換の繰り返し数", from_=1, to=20, orient=tk.HORIZONTAL)
        self.morphology_threshold_slider.set(self.morphology_threshold_value)
        self.morphology_threshold_slider.grid(row=5, column=0, columnspan=3, sticky="we")

        # 最小輪郭面積のスライダー
        self.min_contour_area_slider = Scale(self.root, label="最小輪郭面積", from_=0, to=1000, orient=tk.HORIZONTAL)
        self.min_contour_area_slider.set(self.min_contour_area_value)
        self.min_contour_area_slider.grid(row=6, column=0, columnspan=3, sticky="we")

        # アラートの閾値面積のスライダー
        self.alert_threshold_slider = Scale(self.root, label="アラートを出す輪郭面積の閾値", from_=0, to=5000, orient=tk.HORIZONTAL)
        self.alert_threshold_slider.set(self.alert_threshold_area)
        self.alert_threshold_slider.grid(row=7, column=0, columnspan=3, sticky="we")




    def open_file(self):
        if self.selection_var.get() == 0:  # 画像ファイル選択が選ばれた場合のみ処理
            filetypes = (
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            )

            self.image_path = filedialog.askopenfilename(filetypes=filetypes)
            if self.image_path:
                self.image_path = self.image_path.encode(sys.getfilesystemencoding()).decode('UTF-8')
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, self.image_path)

    def process_image(self):
        if self.selection_var.get() == 0:  # 画像ファイルを選択した場合のみ処理
            if self.image_path is None:
                print("画像が選択されていません。")
                return

            # 画像を読み込む
            with open(self.image_path, 'rb') as f:
                nparr = np.frombuffer(f.read(), np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # グレースケールに変換
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 2値化して白黒反転
            _, binary_image = cv2.threshold(gray_image, self.threshold_slider.get(), 255, cv2.THRESH_BINARY_INV)

            # モルフォロジー変換 オープニング処理 ノイズ除去
            kernel = np.ones((5, 5), np.uint8)
            morphology_threshold = self.morphology_threshold_slider.get()
            morphology_iterations = morphology_threshold // 10  # イテレーション数は閾値に基づいて調整
            binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=morphology_iterations)

            # エッジ検出を行う
            edges = cv2.Canny(binary_image, threshold1=self.threshold1_slider.get(), threshold2=self.threshold2_slider.get())

            # 輪郭検出を行う
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 傷と見なされる可能性のある小さな輪郭をフィルタリング
            min_contour_area = self.min_contour_area_slider.get()
            detected_scratches = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

            # 元の画像に輪郭を描画
            result_image = image.copy()
            cv2.drawContours(result_image, detected_scratches, -1, (0, 255, 0), 2)

            # アラートを出す輪郭の面積の閾値
            alert_threshold_area = self.alert_threshold_slider.get()

            for contour in detected_scratches:
                contour_area = cv2.contourArea(contour)
                if contour_area > alert_threshold_area:
                    cv2.putText(result_image, f'Alert! Area: {contour_area}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)  # フォントサイズを変更

            # ウィンドウを作成し、画像を表示
            cv2.namedWindow('OpenCV Inspector', cv2.WINDOW_NORMAL)  # サイズを変更可能にする
            cv2.imshow('OpenCV Inspector', result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif self.selection_var.get() == 1:  # カメラを選択した場合の処理
            cap = cv2.VideoCapture(0)  # カメラデバイスのインデックスを指定します。0はデフォルトのカメラを指します。
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("カメラからの画像読み込みに失敗しました。")
                    break

                # グレースケールに変換
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 2値化して白黒反転
                _, binary_image = cv2.threshold(gray_image, self.threshold_slider.get(), 255, cv2.THRESH_BINARY_INV)

                # モルフォロジー変換 オープニング処理 ノイズ除去
                kernel = np.ones((5, 5), np.uint8)
                morphology_threshold = self.morphology_threshold_slider.get()
                morphology_iterations = morphology_threshold // 10  # イテレーション数は閾値に基づいて調整
                binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=morphology_iterations)

                # エッジ検出を行う
                edges = cv2.Canny(binary_image, threshold1=self.threshold1_slider.get(), threshold2=self.threshold2_slider.get())

                # 輪郭検出を行う
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # 傷と見なされる可能性のある小さな輪郭をフィルタリング
                min_contour_area = self.min_contour_area_slider.get()
                detected_scratches = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

                # 元の画像に輪郭を描画
                result_image = frame.copy()
                cv2.drawContours(result_image, detected_scratches, -1, (0, 255, 0), 2)

                # アラートを出す輪郭の面積の閾値
                alert_threshold_area = self.alert_threshold_slider.get()

                for contour in detected_scratches:
                    contour_area = cv2.contourArea(contour)
                    if contour_area > alert_threshold_area:
                        cv2.putText(result_image, f'Alert! Area: {contour_area}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow('OpenCV Inspector - press q to exit', result_image)

                if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'キーを押すとループを終了します。
                    break

            cap.release()
            cv2.destroyAllWindows()

root = tk.Tk()
root.title("OpenCV Inspector")

app = ImageProcessor(root)

# ウィンドウサイズを固定しない
root.resizable(width=True, height=True)

root.mainloop()
