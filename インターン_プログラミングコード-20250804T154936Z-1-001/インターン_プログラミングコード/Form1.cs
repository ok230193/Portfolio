namespace WinFormsApp6;

public partial class CameraInformationInput : Form
{
    public string RtspUrl1 { get; set; } = string.Empty;// �v���p�e�B�����J


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
        //\r\n��Windows�̉��s�`���A\n��Linux��Unix�n�̉��s�`���AStringSplitOptions.RemoveEmptyEntries�ŋ�̍s�����������ɔr��
        string[] IPAddresses = textBox1.Text.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries);
        string[] Passwords = textBox2.Text.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries);

        //IP�A�h���X�̐�����Form2���N��
        for (int i = 0; i < IPAddresses.Length; i++)
        {
            string rtspUrl = $"rtsp://root:{Passwords[i]}@{IPAddresses[i]}/axis-media/media.amp";

            // �e�J�����p�� Form2 ���N��
            CameraOutput form2 = new CameraOutput(rtspUrl);
            //�t�H�[�����O�ύX����
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

