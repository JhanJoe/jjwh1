import urllib.request
import bs4
import csv

headers = {
    "cookie": "over18=1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
}

def fetch_page(url):
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        data = response.read().decode('utf-8')
    return data

def extract_likes(nrec_div):
    if nrec_div.find("span") is not None:
        return nrec_div.find("span").text
    return '0'

def main():
    page_url = 'https://www.ptt.cc/bbs/Lottery/index.html'
    count = 0
    all_data = [] 
    
    while count < 3:  
        content = fetch_page(page_url)
        if content is None:
            print(f"Failed to fetch {page_url}")
            break  

        soup = bs4.BeautifulSoup(content, 'html.parser')
        
        articles = soup.find_all("div", class_="r-ent")
        for article in articles:
            title_tag = article.find("div", class_="title").a
            if title_tag is None: 
                continue
            
            title_text = title_tag.text.strip()
            link = 'https://www.ptt.cc' + title_tag['href']
            like_tag = article.find("div", class_="nrec")
            likes = extract_likes(like_tag)

            article_content = fetch_page(link)
            if article_content is None:
                print(f"Failed to fetch {link}")
                continue  

            article_soup = bs4.BeautifulSoup(article_content, 'html.parser')
            meta_values = article_soup.find_all("span", class_="article-meta-value")
            date = meta_values[3].text if len(meta_values) > 3 else "" 
            
            all_data.append([title_text, likes, date])
            
        next_link = soup.find("a", string="‹ 上頁")
        if next_link:
            page_url = 'https://www.ptt.cc' + next_link["href"]
        else:
            break  
        count += 1

    with open('article.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['ArticleTitle', 'Like/DislikeCount', 'PublishTime'])  
        writer.writerows(all_data)  

if __name__ == "__main__":
    main()
