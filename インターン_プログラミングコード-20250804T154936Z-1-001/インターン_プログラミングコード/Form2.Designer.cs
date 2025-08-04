namespace WinFormsApp6
{
    partial class CameraOutput
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            button1 = new Button();
            FPS_Label = new Label();
            SuspendLayout();
            // 
            // button1
            // 
            button1.Font = new Font("Yu Gothic UI", 13.8F, FontStyle.Bold, GraphicsUnit.Point, 128);
            button1.Location = new Point(16, 65);
            button1.Margin = new Padding(7);
            button1.Name = "button1";
            button1.Size = new Size(175, 60);
            button1.TabIndex = 0;
            button1.Text = "Screenshots\r\n";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // FPS_Label
            // 
            FPS_Label.AutoSize = true;
            FPS_Label.Font = new Font("Yu Gothic UI", 25.8000011F, FontStyle.Bold, GraphicsUnit.Point, 128);
            FPS_Label.Location = new Point(0, -2);
            FPS_Label.Name = "FPS_Label";
            FPS_Label.Size = new Size(108, 60);
            FPS_Label.TabIndex = 1;
            FPS_Label.Text = "FPS:";
            // 
            // CameraOutput
            // 
            AutoScaleDimensions = new SizeF(19F, 45F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1717, 997);
            Controls.Add(FPS_Label);
            Controls.Add(button1);
            Font = new Font("Yu Gothic UI", 19.8000011F, FontStyle.Bold, GraphicsUnit.Point, 128);
            Margin = new Padding(7);
            Name = "CameraOutput";
            Text = "Form2";
            Shown += CameraOutput_Shown;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private Label FPS_Label;
    }
}