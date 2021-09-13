using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using System.IO;

namespace AsinGrabber
{

    public partial class UI : Form
    {
        
        public void SetProgress(int progress)
        {
            progressBar1.Increment(progress);
        }
        public UI()
        {
            InitializeComponent();
            numOfPages.SelectedIndex = 4;
        }
        private async void button1_Click(object sender, EventArgs e)
        {
            if (Asins != null)
                Asins.Rows.Clear();
            if (UrlBox.Text.StartsWith("https://www.amazon") || UrlBox.Text.StartsWith("http://www.amazon"))
            {
                btnRun.Text = "Running...";
                btnRun.Enabled = false;
                progressBar1.Value = 0;
                var asins = await GrabAsync.GrabberAsync(this, UrlBox.Text, numOfPages.SelectedIndex+1);
                foreach (KeyValuePair<string,string> kvp in asins)
                {
                    Asins.Rows.Add(kvp.Key, kvp.Value);
                }
                MessageBox.Show("Found " + asins.Count + " unique results", "Run finished successfully", MessageBoxButtons.OK, MessageBoxIcon.Information);
                btnRun.Text = "Run";
                btnRun.Enabled = true;  
            }
            else
            {
                MessageBox.Show("Invalid URL! Try again!","Invalid URL", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        private void btnCopyToClipboard_Click(object sender, EventArgs e)
        {
            try
            {
                Asins.SelectAll();
                DataObject dataObj = Asins.GetClipboardContent();
                Clipboard.SetDataObject(dataObj, true);
            }
            catch
            {
                MessageBox.Show("Nothing to copy!", "No results to copy", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            UrlBox.Clear();
            Asins.Rows.Clear();
            progressBar1.Value = 0;
            numOfPages.SelectedIndex = 4; 
        }

        private void btnCsv_Click(object sender, EventArgs e)
        {
            string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            var filename = desktopPath + "\\Asins " + DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss") + ".csv";
            try
            {
                Asins.SelectAll();
                DataObject dataObj = Asins.GetClipboardContent();
                File.WriteAllText(filename, dataObj.GetText(TextDataFormat.CommaSeparatedValue),Encoding.UTF8);
            }
            catch
            {
                MessageBox.Show("Nothing to export!", "No results to export", MessageBoxButtons.OK, MessageBoxIcon.Error);

            }
        }

        private void numOfPages_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }
}
