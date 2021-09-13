using System;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using System.Text;
using System.Web;

namespace AsinGrabber
{
    public class Grabber
    {
        public static Dictionary<string,string> Grab(UI ui,string url, int numOfPages)
        {
            var chromeDriverService = ChromeDriverService.CreateDefaultService();
            chromeDriverService.HideCommandPromptWindow = true;
            ChromeOptions options = new ChromeOptions();
            options.AddArguments("--headless");
            ChromeDriver driver = new ChromeDriver(chromeDriverService,options);
            ui.progressBar1.Increment(10);
            var hrefs = new List<string>();
            var myDict = new Dictionary<string, string>();
            Encoding windows = Encoding.GetEncoding("UTF-8");
            for (var i = 0; i < numOfPages; i++)
            {
                driver.Url = url +"&page=" + i;
                var links = driver.FindElementsByTagName("a");;
                var prefix = 0;          
                foreach (var link in links)
                {
                    var href = link.GetAttribute("href");
                    if (href != null)
                    {
                        var index = href.IndexOf("/dp/");
                        var review = href.IndexOf("customerReviews");
                        var from_query = href.IndexOf("qid");
                        if (index != -1 && review == -1 && from_query != -1)
                        {
                            hrefs.Add(href);
                            var asin = href.Substring(index + 4, 10);
                            if (!myDict.ContainsKey(asin))
                            {
                                if (href.Contains("https://www.amzn.com/"))
                                {
                                    prefix = 21;
                                }
                                else
                                {
                                    prefix = 23;
                                }
                                if ((index - prefix) > 0)
                                {
                                    var product_name = href.Substring(prefix, index - prefix).Replace('-', ' ');
                                    var decoded_product_name = HttpUtility.UrlDecode(product_name, windows);
                                    myDict.Add(asin, decoded_product_name);
                                }                               
                            }
                        }
                    }
                }
                ui.progressBar1.Increment(90/numOfPages);
            }
            driver.Quit();
            if (ui.progressBar1.Value < 100)
                ui.progressBar1.Value = 100;
            return myDict;
        }
    }
}



