import json
import urllib.request

def fetch_data(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    return json.loads(data.decode(encoding))

def create_serial_dict(data):
    serial_dict = {} 
    for item in data['data']: 
        serial_dict[item['SERIAL_NO']] = {
            'MRT': item['MRT'], 'address': item['address']}
    return serial_dict 

def parse_data(items, serial_dict):
    results = []
    mrt_results = {}
    for item in items: 
        title = item.get('stitle') 
        if not title:
            continue

        serial_no = item.get('SERIAL_NO', None)
        if serial_no in serial_dict:  
            address = serial_dict[serial_no]['address']
            district = address[5:8] if address != "未知區域" else "未知區域"
            mrt_station = serial_dict[serial_no]['MRT']

            title = item.get('stitle', "未知景點")
            longitude = item.get('longitude', "0")
            latitude = item.get('latitude', "0")
            images = item.get('filelist', "").split('https://')
            first_image_url = 'https://' + images[1] if len(images) > 1 else ''
          
            results.append([title, district, longitude,
                           latitude, first_image_url])

            if mrt_station not in mrt_results:
                mrt_results[mrt_station] = []
            mrt_results[mrt_station].append(title)

    return results, mrt_results

def save_to_csv(data, filename, headers):
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(headers + "\n")
        for row in data:
            file.write(",".join(row) + "\n")

def main():
    url1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
    url2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

    data1 = fetch_data(url1)
    data2 = fetch_data(url2)

    serial_dict = create_serial_dict(data2)

    items1 = data1.get('data', {}).get('results', [])
    items2 = data2.get('data', []) if isinstance(
        data2.get('data', []), list) else data2.get('data', {}).get('results', [])
    all_data = items1 + items2

    parsed_data, mrt_data = parse_data(all_data, serial_dict)
   
    save_to_csv(parsed_data, 'spot.csv',
                "SpotTitle,District,Longitude,Latitude,ImageURL")
    save_to_csv([[mrt] + titles for mrt, titles in mrt_data.items()], 'mrt.csv',
                "StationName,AttractionTitle1,AttractionTitle2,AttractionTitle3,AttractionTitle4,AttractionTitle5,AttractionTitle6")
 
if __name__ == "__main__":
    main()

