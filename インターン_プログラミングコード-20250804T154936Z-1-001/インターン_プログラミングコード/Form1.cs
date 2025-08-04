namespace WinFormsApp6;

public partial class CameraInformationInput : Form
{
    public string RtspUrl1 { get; set; } = string.Empty;// プロパティを公開


    public CameraInformationInput()
    {
        InitializeComponent();
    }


    protected override void OnFormClosed(FormClosedEventArgs e)
    {
        base.OnFormClosed(e);
        textBox1?.Dispose();
        textBox2?.Dispose();
    }


    private void button1_Click(object sender, EventArgs e)
    {
        //\r\nはWindowsの改行形式、\nはLinuxとUnix系の改行形式、StringSplitOptions.RemoveEmptyEntriesで空の行があった時に排除
        string[] IPAddresses = textBox1.Text.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries);
        string[] Passwords = textBox2.Text.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries);

        //IPアドレスの数だけForm2を起動
        for (int i = 0; i < IPAddresses.Length; i++)
        {
            string rtspUrl = $"rtsp://root:{Passwords[i]}@{IPAddresses[i]}/axis-media/media.amp";

            // 各カメラ用の Form2 を起動
            CameraOutput form2 = new CameraOutput(rtspUrl);
            //フォーム名前変更処理
            form2.Text = $"Camera {i + 1}";
            form2.Show();
        }

    }


    public void textBox1_TextChanged(object sender, EventArgs e)
    {
        string InputIP = textBox1.Text;
    }


    public void textBox2_TextChanged(object sender, EventArgs e)
    {
        string InputPassword = textBox2.Text;
    }

    private void label1_Click(object sender, EventArgs e)
    {

    }
}

