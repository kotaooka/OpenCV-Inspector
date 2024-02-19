## OpenCV Inspector

これはOpenCVのCannyで画像検査をする試みです。

画像ファイルまたはライブカメラの両方で、しきい値処理、エッジ検出、輪郭検出などのさまざまな操作を実行できます。

### 必要条件
- Python 3.x
- OpenCV (`cv2` ライブラリ)
- NumPy (`numpy` ライブラリ)
- Tkinter (`tkinter` ライブラリ)

### 使い方
1. batファイルからスクリプトを実行します。
2. 画像ファイルを使用するか、カメラを使用するかを選択します。
3. 画像ファイルを使用する場合：
   - "画像を選択" ボタンをクリックして画像ファイルを選択します。
   - スライダーを使用してさまざまなパラメーターを調整します。
   - "実行" ボタンをクリックして画像を処理します。
4. カメラを使用する場合：
   - カメラが正しく接続されていることを確認します。
   - スライダーを使用してパラメーターを調整します。
   - 処理された画像はウィンドウに表示されます。終了するには 'q' キーを押します。

### 画像処理の流れ
1. 2値化
2. モルフォロジー変換(オープニング処理)
3. Cannyエッジ検出
4. 輪郭検出
5. 輪郭のフィルタリング
6. 元画像に輪郭を描画
7. 輪郭面積の閾値設定によってアラート表示

### コントロール
- **2値化の閾値:** 画像を2値化する際の閾値を調整します。閾値より大きい値は白に、小さい値は黒になります。
- **Cannyエッジ検出の低い閾値:** より多くのエッジが検出されるか、または検出されるエッジの種類が変わります。この閾値以下の勾配値はエッジではないと見なされます。
- **Cannyエッジ検出の高い閾値:** エッジの検出に影響します。低い値ではノイズが含まれ、高い値ではエッジが欠落する可能性があります。この閾値以上の勾配値は確実にエッジと見なされます。
- **モルフォロジー変換の繰り返し数:** モルフォロジー変換の反復回数を設定します。ノイズの削減や輪郭の形状に影響が及びます。
- **最小輪郭面積:** 考慮する最小の輪郭面積を設定します。
- **アラートを出す輪郭面積の閾値:** アラートをトリガーする輪郭面積の閾値を設定します。

### 注意
- 画像処理を行う場合は、必要なライブラリ（`cv2`、`numpy`、`tkinter`）がインストールされていることを確認してください。
- カメラを使用する場合は、適切にカメラが接続されていることを確認し、必要に応じてパラメーターを調整してください。
- カメラフィードウィンドウを終了するには 'q' キーを押します。