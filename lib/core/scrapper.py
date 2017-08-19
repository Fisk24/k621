import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import HTTPError

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
			
	def getUnparsedJsonResponce(self, url):
		req = Request(
			url = url,
			headers = {'User-Agent': self.userAgent}
			)
		with urlopen(req) as responce:
			return responce.read()
	
	def fetchPostById(self, id):
		return self.getJsonResponce("{url}post/show.json?id={i}".format(url=self.url, i=id))
		
	def fetchPostsByPage(self, page):
		return self.getJsonResponce("{url}post/index.json?page={p}limit=1".format(url=self.url, p=page))
	
	def fetchCommentsById(self, id):
		data = self.getJsonResponce("{url}comment/index.json?&order=date&post_id={i}".format(url=self.url, i=id))
		data.reverse()
		return data
	
	def fetchUnparsedCommentsById(self, id):
		return self.getUnparsedJsonResponce("{url}comment/index.json?post_id={i}".format(url=self.url, i=id))
	
	def fetchUserById(self, id):
		return self.getJsonResponce("{url}user/show.json?id={u}".format(url=self.url, u=id))
	
	def fetchUserAvatarById(self, id):
		try:
			user = self.fetchUserById(id)
			avatar = self.fetchPostById(user['avatar_id'])
			return avatar
		except HTTPError:
			return None
		
	def printNPMD(self):
		data = self.fetchPosts(1)
		for key in data[1]:
			print("{k}: {v}".format(k=key, v=data[1][key]))

if __name__ == "__main__":		
	print(Scrapper().fetchCommentsById(1304902))
	
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




















