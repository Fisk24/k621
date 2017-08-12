import json
from urllib.request import urlopen
from urllib.request import Request

class Scrapper():
	def __init__(self):
		self.url = "http://e621.net/"
		self.userAgent = "k621/0.01 (Arch Linux; by Fisk42 / Fisk24 on e621)"
		self.postLimit = 75
		
	def getJsonResponce(self, url):
		req = Request(
			url = url,
			headers = {'User-Agent': self.userAgent}
			)
		with urlopen(req) as responce:
			data = json.loads(responce.read())
			return data
		
	def fetchPostsByPage(self, page):
		return self.getJsonResponce("{url}post/index.json?page={p}limit=1".format(url=self.url, p=page))
	
	def fetchCommentsById(self, id):
		# Use /comment/search.json instead. example: https://e621.net/comment/search.json?post_id=1300285&order=date_asc
		return self.getJsonResponce("{url}comment/index.json?post_id={i}".format(url=self.url, i=id))
	
	def printNPMD(self):
		data = self.fetchPosts(1)
		for key in data[1]:
			print("{k}: {v}".format(k=key, v=data[1][key]))

if __name__ == "__main__":		
	Scrapper().printNPMD()
	
'''
Example Comment:
{
"id":3412996,
"created_at":"2017-08-11 16:41",
"post_id":1300285,
"creator":"Spyrox17",
"creator_id":106834,
"body":"Not harmless with a weapon like that.",
"score":3
}	
'''




















