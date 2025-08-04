using OpenCvSharp;
using OpenCvSharp.Extensions;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using System.Diagnostics;

namespace WinFormsApp6
{
    public partial class CameraOutput : Form
    {
        private VideoCapture? CameraCapture;
        private PictureBox PictureBox1;
        private string rtspUrl1;
        private bool Running = false;
        private InferenceSession? session;

        // --- ONNXモデルのパス ---
        private const string ModelPath = @"C:\459_YOLOv9-Wholebody25\yolov9_e_wholebody25_post_0100_1x3x128x160.onnx";

        // 入力画像サイズ (1x3x128x160)
        private const int InputWidth = 160;
        private const int InputHeight = 128;

        private Thread? CaptureThread;
        private Thread? InferenceThread;
        private Mat? LatestFrame;
        private readonly object FrameLock = new object();
        private Stopwatch Stopwatch = Stopwatch.StartNew();  // FPS計測用
        private int FrameCounter = 0;
        private long LastUpdateTime = 0;
        private double CurrentFps = 0.0;

        public CameraOutput(string rtspUrl)
        {
            InitializeComponent();

            SessionOptions options = new SessionOptions();
            options.AppendExecutionProvider_CUDA(0);  // デフォルトGPU (デバイスID:0) を使用
            options.InterOpNumThreads = 4;  // ONNX Runtimeのスレッド間並列数
            options.IntraOpNumThreads = 6;  // ONNX Runtimeのスレッド内並列数

            // PictureBoxの生成・配置
            PictureBox1 = new PictureBox
            {
                Location = new System.Drawing.Point(10, 10),
                Size = new System.Drawing.Size(1900, 850),
                SizeMode = PictureBoxSizeMode.Zoom
            };
            Controls.Add(PictureBox1);

            rtspUrl1 = rtspUrl;
            session = new InferenceSession(ModelPath, options);
        }

        //フォーム起動後にカメラオープン
        private void CameraOutput_Shown(object sender, EventArgs e)
        {
            AfterFormAction(sender, e);
        }

        private void AfterFormAction(object sender, EventArgs e)
        {
            Running = true;

            // --- カメラ取り込み用スレッド ---
            CaptureThread = new Thread(() =>
            {
                CameraCapture = new VideoCapture(rtspUrl1);
                CameraCapture.Set(VideoCaptureProperties.BufferSize, 1);
                int frameSkip = (CurrentFps <= 7.5) ? 4 : 5; // FPS が低ければフレームスキップを減らす
                int frameCount = 0;

                while (Running)
                {
                    CameraCapture.Grab();
                    frameCount++;

                    if (frameCount % frameSkip == 0) // frameSkip 回に1回だけ処理
                    {
                        Mat tempFrame = new Mat();
                        if (CameraCapture.Retrieve(tempFrame))
                        {
                            lock (FrameLock)
                            {
                                LatestFrame?.Dispose();
                                LatestFrame = tempFrame;
                            }
                        }
                    }
                    else
                    {
                        Thread.Yield(); // 軽く待機してCPU負荷を下げる
                    }
                }

                // カメラの終了処理
                CameraCapture.Release();
                CameraCapture.Dispose();
                CameraCapture = null;
            });

            // --- 推論処理用スレッド ---
            InferenceThread = new Thread(() =>
            {
                while (Running)
                {
                    Mat? currentFrame = null;

                    // 最新フレームを取得
                    lock (FrameLock)
                    {
                        if (LatestFrame != null)
                        {
                            currentFrame = new Mat();
                            LatestFrame.CopyTo(currentFrame);
                        }
                    }

                    if (currentFrame != null)
                    {
                        // 推論実行＆結果を描画
                        Mat drawnFrame = RunInferenceAndDraw(currentFrame);

                        // FPS計算
                        FrameCounter++;
                        long elapsed = Stopwatch.ElapsedMilliseconds;
                        if (elapsed - LastUpdateTime >= 1000) // 1秒ごとに更新
                        {
                            CurrentFps = FrameCounter / ((elapsed - LastUpdateTime) / 1000.0);
                            FrameCounter = 0;
                            LastUpdateTime = elapsed;
                        }

                        // UIスレッドでPictureBoxを更新
                        if (!drawnFrame.Empty() && PictureBox1 != null && PictureBox1.IsHandleCreated && !PictureBox1.IsDisposed)
                        {
                            var bitmap = BitmapConverter.ToBitmap(drawnFrame);
                            PictureBox1.Invoke(new Action(() =>
                            {
                                PictureBox1.Image?.Dispose();
                                PictureBox1.Image = bitmap;

                                // FPSラベル更新
                                FPS_Label.Text = $"FPS: {CurrentFps:F1}";
                            }));
                        }

                        // 使用したフレームを破棄
                        currentFrame.Dispose();
                        drawnFrame.Dispose();
                    }
                    else
                    {
                        // フレームが無ければ少し待つ
                        Thread.Yield();
                    }
                }
            });

            // スレッド開始
            CaptureThread.Start();
            InferenceThread.Start();
        }

        private Mat RunInferenceAndDraw(Mat originalFrame)
        {
            // 1) 前処理: リサイズ (inputWidth, inputHeight)
            Mat resizedFrame = new Mat();
            Cv2.Resize(originalFrame, resizedFrame, new OpenCvSharp.Size(InputWidth, InputHeight));

            // 2) Tensor準備 (Pythonコードでいう _preprocess と同等)
            float[] inputData = PrepareInput(resizedFrame);
            var inputTensor = new DenseTensor<float>(inputData, new[] { 1, 3, InputHeight, InputWidth });

            // input_bgrはNetronの一番上の入力参照
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor("input_bgr", inputTensor)
            };

            // 3) 推論実行
            float scoreThreshold = 0.35f;
            var outputData = session!.Run(inputs).First().AsTensor<float>().ToArray();

            // 4) 後処理: 出力配列 [N,7] → [ (使わない), classsId, score, x1, y1, x2, y2 ]
            int numDetections = outputData.Length / 7;

            // 描画用にコピー
            Mat resultFrame = originalFrame.Clone();

            for (int i = 0; i < numDetections; i++)
            {
                int offset = i * 7;

                // batchNo を読み飛ばして classId, score, x1, y1, x2, y2 を取得
                float classId = outputData[offset + 1];
                float score = outputData[offset + 2];
                float x1 = outputData[offset + 3];
                float y1 = outputData[offset + 4];
                float x2 = outputData[offset + 5];
                float y2 = outputData[offset + 6];

                if (score < scoreThreshold) continue;

                int Width = originalFrame.Width;
                int Height = originalFrame.Height;
                float scaleX = (float)Width / InputWidth;
                float scaleY = (float)Height / InputHeight;

                x1 *= scaleX;
                y1 *= scaleY;
                x2 *= scaleX;
                y2 *= scaleY;

                // クリップ処理 (0～W-1, 0～H-1)
                x1 = Math.Max(0, Math.Min(Width - 1, x1));
                y1 = Math.Max(0, Math.Min(Height - 1, y1));
                x2 = Math.Max(0, Math.Min(Width - 1, x2));
                y2 = Math.Max(0, Math.Min(Height - 1, y2));

                // クラスIDに応じた色を取得（HSV→BGR変換）
                Scalar color = ClassIdToColorBgr((int)classId);

                // 描画
                Cv2.Rectangle(resultFrame, new Rect((int)x1, (int)y1, (int)(x2 - x1), (int)(y2 - y1)), color, 2);

                // クラスIDとスコアを文字列に
                Cv2.PutText(resultFrame, $"ID:{classId} Score:{score:F2}", new OpenCvSharp.Point((int)x1, (int)(y1 - 10)), HersheyFonts.HersheySimplex, 0.7, color, 2);
            }

            return resultFrame;
        }

        // クラスIDに基づいてHSVカラーをBGRに変換し、描画用の色として返す
        private Scalar ClassIdToColorBgr(int classId)
        {
            // クラスIDに応じて異なるHueを設定（360度を12クラスに分割）
            double hue = (classId * 30) % 360.0;
            double saturation = 1.0; // 彩度（最大）
            double value = 1.0;      // 明度（最大）

            return HsvToScalarBgr(hue, saturation, value);
        }

        // HSV(0..360, 0..1, 0..1) を BGR の Scalar に変換
        private Scalar HsvToScalarBgr(double h, double s, double v)
        {
            double c = v * s;
            double hh = h / 60.0;
            double x = c * (1.0 - Math.Abs(hh % 2.0 - 1.0));

            double[][] rgbMatrix = new double[][]
            {
                new double[] {c, x, 0},  // 0°- 60°
                new double[] {x, c, 0},  // 60°- 120°
                new double[] {0, c, x},  // 120 °- 180°
                new double[] {0, x, c},  // 180°- 240°
                new double[] {x, 0, c},  // 240°- 300°
                new double[] {c, 0, x}   // 300°- 360°
            };

            int index = (int)Math.Floor(hh) % 6;
            double r = rgbMatrix[index][0];
            double g = rgbMatrix[index][1];
            double b = rgbMatrix[index][2];

            double m = v - c;
            r += m; g += m; b += m;

            // [0..1] を [0..255] に変換
            byte R = (byte)Math.Round(r * 255.0);
            byte G = (byte)Math.Round(g * 255.0);
            byte B = (byte)Math.Round(b * 255.0);

            return new Scalar(B, G, R);
        }

        // (H,W,3) BGR画像を (3,H,W) float配列に詰め直す (demoプログラムより (3,H,W)であると確認)
        private float[] PrepareInput(Mat image)
        {
            float[] inputData = new float[3 * InputHeight * InputWidth];
            int imageSize = InputHeight * InputWidth;

            for (int y = 0; y < InputHeight; y++)
            {
                for (int x = 0; x < InputWidth; x++)
                {
                    Vec3b pixel = image.At<Vec3b>(y, x);
                    float b = pixel.Item0;
                    float g = pixel.Item1;
                    float r = pixel.Item2;

                    // (C=0, H=y, W=x) = B
                    inputData[0 * imageSize + y * InputWidth + x] = b;
                    // (C=1, H=y, W=x) = G
                    inputData[1 * imageSize + y * InputWidth + x] = g;
                    // (C=2, H=y, W=x) = R
                    inputData[2 * imageSize + y * InputWidth + x] = r;
                }
            }
            return inputData;
        }

        // Formが閉じられる際の後処理
        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            Running = false;

            // スレッドの終了を待機
            CaptureThread?.Join();
            InferenceThread?.Join();

            // 既存のリソース開放
            base.OnFormClosed(e);
            PictureBox1.Image?.Dispose();
            PictureBox1.Dispose();
            session?.Dispose();
        }

        // 「Screenshots」ボタン押下時の処理 (映像のスクリーンショットを保存する)
        private void button1_Click(object sender, EventArgs e)
        {
            var btn = sender as Button;
            btn!.Enabled = false;

            if (PictureBox1.Image != null)
            {
                string folderPath = @"C:\Users\ok230193\Pictures";
                if (!Directory.Exists(folderPath))
                {
                    Directory.CreateDirectory(folderPath);
                }

                string fileName = Path.Combine(folderPath, $"capture_{DateTime.Now:yyyyMMdd_HHmmss}.png");
                Task.Run(() =>
                {
                    // UIスレッドでPictureBox1.Imageを保存
                    PictureBox1.Invoke(new Action(() =>
                    {
                        PictureBox1.Image.Save(fileName, System.Drawing.Imaging.ImageFormat.Png);
                    }));
                    MessageBox.Show($"画像を保存しました: {fileName}");
                    btn.Invoke(new Action(() => btn.Enabled = true));
                });
            }
            else
            {
                MessageBox.Show("画像がありません。");
                btn.Enabled = true;
            }
        }
    }
}
