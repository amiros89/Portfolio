using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AsinGrabber
{
    public class GrabAsync
    {
        public static async Task<Dictionary<string,string>> GrabberAsync(UI ui,string url,int numOfPages)
        {
            var asinsTask = Task.Run(() => Grabber.Grab(ui,url,numOfPages));
            Dictionary<string,string> result = await asinsTask;
            return result;
        }
    }
}
