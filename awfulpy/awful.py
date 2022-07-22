from bs4 import BeautifulSoup
from bs4 import Comment
import re

class ForumPost:
    def __init__(self, post):
        soup = BeautifulSoup(post, 'lxml')
        self.author = ForumPoster(str(soup.find_all("dl", class_="userinfo")))
        self.postid = int(soup.table['id'][4:])
        #self.timestamp = None
        body = soup.find("td", class_="postbody")
        for child in body.find_all("div", class_="bbc-block"):
            child.decompose()
        self.body = body.text.strip()

class ForumPoster:
    def __init__(self, sidebar):
        soup = BeautifulSoup(sidebar, 'lxml')
        self.name = soup.find("dt", class_="author").string
        #self.userid = None
        #self.avatar = None
        #self.signature = None
        #self.regdate = None

class ForumThreadPage:
    def __init__(self, text):
        soup = BeautifulSoup(text, 'lxml')
        posts = soup.find_all("table", class_="post")
        self.posts = []
        for p in posts:
            pobj = ForumPost(str(p))
            self.posts.append(pobj)
        breadcrumbs = soup.find("div", class_="breadcrumbs").find("select")
        if breadcrumbs:
            self.pagenum = int(breadcrumbs.find("option", selected=True).text)
            self.maxpagenum = int(breadcrumbs.find_all("option")[-1].text)
        else:
            self.pagenum = 1
            self.maxpagenum = 1
        self.replyURL= str(soup.find("div", class_="threadbar bottom").find("ul", class_="postbuttons").find_all("li")[1].a["href"])

class ProfilePage:
    def __init__(self,text):
        soup = BeautifulSoup(text, 'lxml')
        
        raw_profile = soup.find("td", class_="info")
        
        
        self.raw_profile_text = str(raw_profile)
        if raw_profile is None:
            self.raw_profile_text = None
            self.userid = None
            return
        
        
        match = re.search(r"banlist\.php\?userid=([0-9]*)", text)
        self.userid = match.group(1)
        
        ## TODO: capture all the separate sections instead of just all of it as a blob.
        
        
        
class ReplyPage:
    def __init__(self, text):
        soup = BeautifulSoup(text, 'lxml')
        self.message = None
        self.action = "postreply"
        self.threadid = soup.find("input", attrs={"name": "threadid"})['value']
        self.formkey = soup.find("input", attrs={"name": "formkey"})['value']
        self.form_cookie = soup.find("input", attrs={"name": "form_cookie"})['value']