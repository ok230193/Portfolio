namespace WinFormsApp6
{
    partial class CameraInformationInput : Form
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            add = new Button();
            textBox1 = new TextBox();
            textBox2 = new TextBox();
            toolStrip1 = new ToolStrip();
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            SuspendLayout();
            // 
            // add
            // 
            add.BackColor = Color.Salmon;
            add.Font = new Font("Yu Gothic UI", 48F, FontStyle.Bold, GraphicsUnit.Point, 128);
            add.Location = new Point(105, 392);
            add.Name = "add";
            add.Size = new Size(522, 195);
            add.TabIndex = 0;
            add.Text = "ADD";
            add.UseVisualStyleBackColor = false;
            add.Click += button1_Click;
            // 
            // textBox1
            // 
            textBox1.Font = new Font("Yu Gothic UI", 12F, FontStyle.Bold, GraphicsUnit.Point, 128);
            textBox1.Location = new Point(791, 179);
            textBox1.Multiline = true;
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(1115, 297);
            textBox1.TabIndex = 1;
            textBox1.Text = "192.168.0.90\r\n192.168.0.91\r\n192.168.0.85\r\n192.168.0.225\r\n192.168.0.92\r\n192.168.0.57";
            textBox1.TextChanged += textBox1_TextChanged;
            // 
            // textBox2
            // 
            textBox2.Font = new Font("Yu Gothic UI", 12F, FontStyle.Bold, GraphicsUnit.Point, 128);
            textBox2.Location = new Point(791, 559);
            textBox2.Multiline = true;
            textBox2.Name = "textBox2";
            textBox2.Size = new Size(1119, 297);
            textBox2.TabIndex = 2;
            textBox2.Text = "Hutzper_pic\r\nHutzper_pic\r\nHutzper_pic\r\nHutzper_pic\r\nHutzper_pic\r\nHutzper_pic\r\n";
            textBox2.TextChanged += textBox2_TextChanged;
            // 
            // toolStrip1
            // 
            toolStrip1.ImageScalingSize = new Size(20, 20);
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Size = new Size(1922, 25);
            toolStrip1.TabIndex = 3;
            toolStrip1.Text = "toolStrip1";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Yu Gothic UI", 19.8000011F, FontStyle.Bold, GraphicsUnit.Point, 128);
            label1.Location = new Point(791, 130);
            label1.Name = "label1";
            label1.Size = new Size(207, 46);
            label1.TabIndex = 4;
            label1.Text = "IP ADDRESS";
            label1.Click += label1_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Yu Gothic UI", 19.8000011F, FontStyle.Bold, GraphicsUnit.Point, 128);
            label2.Location = new Point(787, 510);
            label2.Name = "label2";
            label2.Size = new Size(203, 46);
            label2.TabIndex = 5;
            label2.Text = "PASSWORD";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.BackColor = SystemColors.Highlight;
            label3.Font = new Font("Yu Gothic UI", 36F, FontStyle.Bold, GraphicsUnit.Point, 128);
            label3.Location = new Point(41, 56);
            label3.Name = "label3";
            label3.Size = new Size(672, 81);
            label3.TabIndex = 6;
            label3.Text = "CAMERA IMFOMATION";
            // 
            // CameraInformationInput
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1922, 1005);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(toolStrip1);
            Controls.Add(textBox2);
            Controls.Add(textBox1);
            Controls.Add(add);
            Name = "CameraInformationInput";
            Text = "Form1";
            Click += button1_Click;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button add;
        private TextBox textBox1;
        private TextBox textBox2;
        private ToolStrip toolStrip1;
        private Label label1;
        private Label label2;
        private Label label3;
    }
}
