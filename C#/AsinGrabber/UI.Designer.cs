
namespace AsinGrabber
{
    partial class UI
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
            this.btnRun = new System.Windows.Forms.Button();
            this.btnCopyToClipboard = new System.Windows.Forms.Button();
            this.btnCsv = new System.Windows.Forms.Button();
            this.btnClear = new System.Windows.Forms.Button();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.Title = new System.Windows.Forms.Label();
            this.UrlBox = new System.Windows.Forms.TextBox();
            this.Asins = new System.Windows.Forms.DataGridView();
            this.ASIN = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.TITTLE = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.numOfPages = new System.Windows.Forms.ComboBox();
            ((System.ComponentModel.ISupportInitialize)(this.Asins)).BeginInit();
            this.SuspendLayout();
            // 
            // btnRun
            // 
            this.btnRun.Location = new System.Drawing.Point(61, 625);
            this.btnRun.Name = "btnRun";
            this.btnRun.Size = new System.Drawing.Size(150, 50);
            this.btnRun.TabIndex = 0;
            this.btnRun.Text = "Run";
            this.btnRun.UseVisualStyleBackColor = true;
            this.btnRun.Click += new System.EventHandler(this.button1_Click);
            // 
            // btnCopyToClipboard
            // 
            this.btnCopyToClipboard.Location = new System.Drawing.Point(246, 625);
            this.btnCopyToClipboard.Name = "btnCopyToClipboard";
            this.btnCopyToClipboard.Size = new System.Drawing.Size(150, 50);
            this.btnCopyToClipboard.TabIndex = 1;
            this.btnCopyToClipboard.Text = "Copy To Clipboard";
            this.btnCopyToClipboard.UseVisualStyleBackColor = true;
            this.btnCopyToClipboard.Click += new System.EventHandler(this.btnCopyToClipboard_Click);
            // 
            // btnCsv
            // 
            this.btnCsv.Location = new System.Drawing.Point(435, 625);
            this.btnCsv.Name = "btnCsv";
            this.btnCsv.Size = new System.Drawing.Size(150, 50);
            this.btnCsv.TabIndex = 2;
            this.btnCsv.Text = "Export to CSV";
            this.btnCsv.UseVisualStyleBackColor = true;
            this.btnCsv.Click += new System.EventHandler(this.btnCsv_Click);
            // 
            // btnClear
            // 
            this.btnClear.Location = new System.Drawing.Point(628, 625);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new System.Drawing.Size(150, 50);
            this.btnClear.TabIndex = 3;
            this.btnClear.Text = "Clear";
            this.btnClear.UseVisualStyleBackColor = true;
            this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
            // 
            // progressBar1
            // 
            this.progressBar1.Location = new System.Drawing.Point(151, 576);
            this.progressBar1.Name = "progressBar1";
            this.progressBar1.Size = new System.Drawing.Size(553, 23);
            this.progressBar1.TabIndex = 4;
            // 
            // Title
            // 
            this.Title.AutoSize = true;
            this.Title.Font = new System.Drawing.Font("Aharoni", 48F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.Title.Location = new System.Drawing.Point(200, 24);
            this.Title.Name = "Title";
            this.Title.Size = new System.Drawing.Size(458, 63);
            this.Title.TabIndex = 6;
            this.Title.Text = "ASIN Grabber";
            // 
            // UrlBox
            // 
            this.UrlBox.Location = new System.Drawing.Point(151, 133);
            this.UrlBox.Name = "UrlBox";
            this.UrlBox.Size = new System.Drawing.Size(482, 23);
            this.UrlBox.TabIndex = 8;
            // 
            // Asins
            // 
            this.Asins.AllowUserToAddRows = false;
            this.Asins.AllowUserToDeleteRows = false;
            this.Asins.AllowUserToResizeColumns = false;
            this.Asins.AllowUserToResizeRows = false;
            this.Asins.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.Asins.BackgroundColor = System.Drawing.SystemColors.Control;
            this.Asins.ClipboardCopyMode = System.Windows.Forms.DataGridViewClipboardCopyMode.EnableWithoutHeaderText;
            this.Asins.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.Asins.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.ASIN,
            this.TITTLE});
            this.Asins.GridColor = System.Drawing.SystemColors.Control;
            this.Asins.Location = new System.Drawing.Point(151, 233);
            this.Asins.Name = "Asins";
            this.Asins.RowHeadersVisible = false;
            this.Asins.RowHeadersWidthSizeMode = System.Windows.Forms.DataGridViewRowHeadersWidthSizeMode.DisableResizing;
            this.Asins.RowTemplate.Height = 25;
            this.Asins.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.Asins.Size = new System.Drawing.Size(553, 335);
            this.Asins.TabIndex = 9;
            // 
            // ASIN
            // 
            this.ASIN.HeaderText = "ASIN";
            this.ASIN.Name = "ASIN";
            this.ASIN.ReadOnly = true;
            // 
            // TITTLE
            // 
            this.TITTLE.HeaderText = "TITTLE";
            this.TITTLE.Name = "TITTLE";
            this.TITTLE.ReadOnly = true;
            // 
            // numOfPages
            // 
            this.numOfPages.BackColor = System.Drawing.SystemColors.Window;
            this.numOfPages.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.numOfPages.FlatStyle = System.Windows.Forms.FlatStyle.System;
            this.numOfPages.FormattingEnabled = true;
            this.numOfPages.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"});
            this.numOfPages.Location = new System.Drawing.Point(655, 133);
            this.numOfPages.Name = "numOfPages";
            this.numOfPages.Size = new System.Drawing.Size(49, 23);
            this.numOfPages.TabIndex = 10;
            this.numOfPages.SelectedIndexChanged += new System.EventHandler(this.numOfPages_SelectedIndexChanged);
            // 
            // UI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(843, 711);
            this.Controls.Add(this.numOfPages);
            this.Controls.Add(this.Asins);
            this.Controls.Add(this.UrlBox);
            this.Controls.Add(this.Title);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.btnClear);
            this.Controls.Add(this.btnCsv);
            this.Controls.Add(this.btnCopyToClipboard);
            this.Controls.Add(this.btnRun);
            this.Name = "UI";
            this.Text = "ASIN Grabber";
            ((System.ComponentModel.ISupportInitialize)(this.Asins)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnRun;
        private System.Windows.Forms.Button btnCopyToClipboard;
        private System.Windows.Forms.Button btnCsv;
        private System.Windows.Forms.Button btnClear;
        public System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Label Title;
        private System.Windows.Forms.TextBox UrlBox;
        private System.Windows.Forms.DataGridView Asins;
        private System.Windows.Forms.DataGridViewTextBoxColumn ASIN;
        private System.Windows.Forms.DataGridViewTextBoxColumn TITTLE;
        private System.Windows.Forms.ComboBox numOfPages;
    }
}

