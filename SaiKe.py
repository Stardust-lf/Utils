from bs4 import BeautifulSoup
import requests
import csv


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        print(url + "  has been catched")
        return r.text.encode("gbk", 'ignore').decode("gbk", "ignore")
        pass
    except:
        return 'ERROR'

def get_item(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('span', class_="item-tit")
    title = soup.find_all('a',class_="link")
    state = soup.find_all('em')
    list = [];
    if (item == None):
        return ""
    else:
        i = 0
        j = 0
        while i < len(item)/4:
            '''
            print(title[j].get_text())
            print(state[j].get_text()[21:])
            print(item[i * 4 + 0].parent.get_text()[3:])
            print(item[i * 4 + 1].parent.get_text()[4:])
            print(item[i * 4 + 2].parent.get_text()[4:].replace(' ',''))
            print(item[i * 4 + 3].parent.get_text()[29:].replace(' ',''))
            i += 1
            j += 1
            pass
            '''
            temp = []
            temp.append(title[j].get_text().replace(' ', ''))
            temp.append(state[j].get_text()[21:].replace(' ', ''))
            temp.append(item[i * 4 + 0].parent.get_text()[3:].replace(' ', ''))
            temp.append(item[i * 4 + 1].parent.get_text()[4:].replace(' ', ''))
            temp.append(item[i * 4 + 2].parent.get_text()[4:].replace(' ', ''))
            temp.append(item[i * 4 + 3].parent.get_text()[29:].replace(' ', ''))
            list.append(temp)
            i += 1
            j += 1
            pass
        pass
    return list

if __name__ == '__main__':
    file = open('SaiKe.csv','w')
    writer = csv.writer(file)
    writer.writerow(['title','state','organizer','level','startTime','endTime',])
    n = 0
    while n <= 50:
        writer.writerows(get_item(get_html("https://www.saikr.com/vs?page=" + str(n))))
        n += 1
    pass
