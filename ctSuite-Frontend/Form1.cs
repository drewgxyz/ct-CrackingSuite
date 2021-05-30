using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ctSuite_Frontend
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void fileSystemWatcher1_Changed(object sender, System.IO.FileSystemEventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            Process test = new Process();
            test.StartInfo.FileName = "../../../../run.bat";
            test.StartInfo.UseShellExecute = false;
            test.StartInfo.Arguments = "";
            test.StartInfo.RedirectStandardOutput = true;
            test.Start();
            textBox1.Text = test.StandardOutput.ReadToEnd();

        }
    }
}
