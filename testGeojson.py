import requests

def main():
    url = "http://localhost:5000/api/v1/postGIS"
    res = requests.get(url)
    data = res.json()
    #print(data[features])
    #for key, value in data.iteritems():
    print (data.keys())
    # print (data.values())
    # for key in data:
    #   print (f"the key name is {key} and its value is {data[key]}")
if __name__ == "__main__":
    main()
