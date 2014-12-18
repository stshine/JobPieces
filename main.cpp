#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <highgui.h>

#include <libxml++/libxml++.h>
#include <libxml/tree.h>
#include <libxml/HTMLparser.h>

#include "curl_easy.h"
#include <vector>

using curl::curl_easy;

bool MatCmp(cv::Mat src1, cv::Mat src2) {
    cv::Mat diff;
    cv::compare(src1, src2, diff, cv::CMP_NE);
    if (cv::countNonZero(diff) == 0){
        return true;
    } else {
        return false;
    }
}

bool checkBorder(cv::Mat image) {
    if(!MatCmp(image.row(0), image.row(image.rows-1)) || !MatCmp(image.col(0),image.col(image.cols-1))) {
        return false;
    }
    cv::Vec3b color = image.at<cv::Vec3b>(0,0);
    cv::Mat mask (image.size(), image.type(), &color);
    cv::Mat invert;
    cv::subtract(mask, image, invert);

    // Store the set of points in the image before assembling the bounding box
    std::vector<cv::Point> points;
    cv::Mat_<uchar>::iterator it = invert.begin<uchar>();
    cv::Mat_<uchar>::iterator end = invert.end<uchar>();
    for (; it != end; ++it)
    {
        if (*it) points.push_back(it.pos());
    }

    // Compute minimal bounding box
    cv::RotatedRect box = cv::minAreaRect(cv::Mat(points));
    if ((box.size.height = image.rows) && (box.size.width == image.cols)) {
        return true;
    } else {
        return false;
    }
}

std::string getPage(const char *url) {
    std::ostringstream stream;
    curl_writer writer(stream);
    curl_easy curl(writer);

    // Add some option to the easy handle
    curl.add(curl_pair<CURLoption,string>(CURLOPT_URL, url));
    curl.add(curl_pair<CURLoption,long>(CURLOPT_FOLLOWLOCATION,1L));
    try {
        curl.perform();
    } catch (curl_easy_exception error) {
        // If you want to get the entire error stack we can do:
        vector<pair<string,string>> errors = error.what();
        // Otherwise we could print the stack like this:
        error.print_traceback();
    }
    return stream.str();
}

bool checkPage(const char *url) {
    std::string content = getPage(url);
    htmlDocPtr doc = htmlReadDoc((const xmlChar*)content.c_str(), NULL, "UTF-8",
                                 HTML_PARSE_RECOVER | HTML_PARSE_NOERROR | HTML_PARSE_NOWARNING);
    if (!doc) {
      cout << "Parsing failed:" << url << endl;
      exit(1);
    }
    xmlNode* r = xmlDocGetRootElement(doc);
    if(!r) {
      cout << "Get root element failed:" << url << endl;
      exit(1);
    }
    xmlpp::Element* root = new xmlpp::Element(r);
    std::string xpath = "/html/body/div[4]/div[4]/div[1]/div[1]/dl/dt/div/div[2]/ul/li/a/img";
    auto elements = root->find(xpath);
    for (int i=0; i<elements.size(); i++) {
        cout << dynamic_cast<xmlpp::ContentNode*>(elements[i])->get_content();
//        if (!checkImage(imgUrl)) {
//            return false;
//        }
    }

    delete root;
    xmlFreeDoc(doc);

    return true;
}

int main(int argc, char* argv[])
{
    checkPage("http://www.3158.cn/xiangmu/137391/");
    return 0;
}
