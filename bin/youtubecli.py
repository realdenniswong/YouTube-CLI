import sys, subprocess, requests, json, os

res_dict = {}
cur_page = 1;
q = '';
pgt = ''
qt_flag = False
s_flag = True
k = ''

show_preview_image = True;

def youtubecli():
  global s_flag

  while qt_flag == False:
 
    if s_flag == True:
      print("[========type and press enter to search========]")
      q = input()
      s_flag = False
 
    print("you searched",q+", currently in search record page",cur_page)
  
    res = ''
  
    #find the data in res
    if(cur_page in res_dict):
      res = res_dict[cur_page]
      print("res_dict has the record!")
    else:
      res = requests.get(ytapi_search_curl(q,pgt,cur_page))
      res_dict[cur_page] = res
      print("no page",str(cur_page),"record in res_dict, requested from api.")
  
    show_rec(res.json())
    print("[========type command========]\n[========numbers to select video, q to quit========]\n[========s to search other words========]\n[========n and p to go to next page and prev page========]")
    cmd = input()    
    cmd_proc(cmd)



def show_rec(json):

  items = json['items']
  
  for i in range(0, len(items)):
    print(i+1, items[i]['snippet']['title'], "[___BY___]", items[i]['snippet']['channelTitle'])
    if show_preview_image == True:
      try:
        #vmenu_i_cmd = 'curl https://i.ytimg.com/vi/'+res_dict[cur_page].json()['items'][i - 1]['id']['videoId']+'/hqdefault.jpg | imgcat'
        ps = subprocess.Popen(('curl', 'https://i.ytimg.com/vi/'+res_dict[cur_page].json()['items'][i]['id']['videoId']+'/default.jpg', '-s'), stdout=subprocess.PIPE)
        subprocess.run(('imgcat'), stdin=ps.stdout)
      except KeyError:
        print("no preview image")

def ytapi_search_curl(q,pgt,cur_page):
  if(cur_page < 1):
    error(1)
  q_str = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=7'
  if(cur_page > 1):
    q_str += '&pageToken=' + pgt
  q_str += '&q='+q+'&key=' + k
  return q_str  


    
def cmd_proc(cmd):
 
  global cur_page
  global pgt
  global qt_flag
  global res_dict
  global s_flag 

  if (cmd == 'n'):
    print("[========>>>>next page<<<<========]")
    cur_page += 1
    pgt = res_dict[cur_page-1].json()['nextPageToken']
    #youtubecli(res_dict[cur_page-1].json()['nextPageToken'])
  if (cmd == 'p'):
    if(cur_page > 1):
      print("[========>>>>prev page<<<<========]")
      cur_page -= 1
      pgt = res_dict[cur_page+1].json()['prevPageToken']
      #youtubecli(res_dict[cur_page+1].json()['prevPageToken'])
    elif(cur_page < 1):
      error(1)
    else:
      cur_page = 1
      pgt = ''
  if (cmd == 'q'):
      print("[========>>>>quit the application<<<<========]")
      qt_flag = True
  if cmd == 's':
      res_dict = {}
      cur_page = 1
      pgt = ''
      s_flag = True
  if (cmd.strip().isdigit()):
    v_id = int(cmd)
    quit_vmenu = False
    while quit_vmenu == False:
      print("[========select command========]\n[========v for video, a for audio========]\n[========i to preview image, d to download as mp3========]\n[========q for quit========]")
      vmenu_cmd = input()
      if vmenu_cmd == 'q':
        quit_vmenu = True
      if vmenu_cmd == 'v':
        print("[========play video========]")
        subprocess.run(['mpv','https://www.youtube.com/watch?v='+res_dict[cur_page].json()['items'][v_id - 1]['id']['videoId']])
      if vmenu_cmd == 'a':
        print("[========play audio========]")
        subprocess.run(['mpv','--no-video','https://www.youtube.com/watch?v='+res_dict[cur_page].json()['items'][v_id - 1]['id']['videoId']])
      if vmenu_cmd == 'i':
        print("[========preview image========]")
        vmenu_i_cmd = 'curl https://i.ytimg.com/vi/'+res_dict[cur_page].json()['items'][v_id - 1]['id']['videoId']+'/hqdefault.jpg | imgcat'
        ps = subprocess.Popen(('curl', 'https://i.ytimg.com/vi/'+res_dict[cur_page].json()['items'][v_id - 1]['id']['videoId']+'/hqdefault.jpg'), stdout=subprocess.PIPE)
        subprocess.run(('imgcat'), stdin=ps.stdout)
      if vmenu_cmd == 'd':
        print("[========download video========]")
        subprocess.run(['youtube-dl','-f','bestaudio','--extract-audio','--audio-format','mp3','--audio-quality','0','https://www.youtube.com/watch?v='+res_dict[cur_page].json()['items'][v_id - 1]['id']['videoId']])

def error(code):
  if (code == 1):
    print("cur_page is now",cur_page+". check that again!")

#full_path = os.path.realpath(__file__)
#api_key_path = os.path.dirname(os.path.split(full_path)[0]) + "/apikey"
#f = open(api_key_path, "r")
#k = f.readline()
k = "AIzaSyDWYc8iVdVqGssvvp53J-nMlULNfV342Nw" #!!!!!!!!TYPE YOUR YOUR API KEY THIS LINE!!!!!!!!
for x in sys.argv[1:]:
  if(x == "-np"):
    show_preview_image = False;
  elif(x == ""):continue
  else:
    print(x,"is not a valid command, ignore.")
youtubecli()
