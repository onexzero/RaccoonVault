import sys
import requests
import json
import datetime
from urllib import parse
F="https://apis.pooq.co.kr/login?apikey=E5F3E0D30947AA5440556471321BB6D9&credential=none&device=pc&drm=wm&partner=pooq&pooqzone=none&region=kor&targetage=all"
l="https://apis.wavve.com/fz/streaming?device=pc&partner=pooq&apikey=E5F3E0D30947AA5440556471321BB6D9&credential={0}&service=wavve&pooqzone=none&region=kor&drm=none&targetage=all&contentid={1}&hdr=sdr&videocodec=avc&audiocodec=ac3&issurround=n&format=normal&withinsubtitle=n&contenttype=live&action=hls&protocol=hls&quality=auto&deviceModelId=Windows%2010&guid=1d191e5c-568a-11ed-b37d-92dd5a1cfeb9&lastplayid=46fa3c25a79145d088caebeeebbee4dc&authtype=cookie&isabr=y&ishevc=n"
t="https://apis.wavve.com/live/epgs?enddatetime={0}&genre=all&limit=500&offset=0&startdatetime={1}&apikey=E5F3E0D30947AA5440556471321BB6D9&credential={2}&device=pc&drm=wm&partner=pooq&pooqzone=none&region=kor&targetage=all"
X="https://apis.pooq.co.kr/logout?apikey=E5F3E0D30947AA5440556471321BB6D9&credential={0}&device=pc&drm=wm&partner=pooq&pooqzone=none&region=kor&targetage=all"
K="https://apis.pooq.co.kr/live/channels/{0}?device=pc&partner=pooq&pooqzone=none&region=kor&drm=wm&targetage=all&apikey=E5F3E0D30947AA5440556471321BB6D9&credential=none"
def R(m,V):
 try:
  e=json.loads('{{"type": "general","id": "{0}","pushid": "","password":"{1}","profile": "0"}}'.format(m,V))
  h=requests.post(F,json=e)
  P=json.loads(h.text)
  W=P.get("credential")
  e='{{"type": "credential","id": "{0}","pushid": "","password":"","profile": "0"}}'.format(W)
  h=requests.post(F,data=e)
  P=json.loads(h.text)
  if P.get("needselectprofile")!='n':
   raise Exception("Unexpected server response.")
 except Exception as e:
  print(str(e))
  return None
 else:
  return W
def o(W):
 try:
  A=X.format(parse.quote(W))
  h=requests.options(A)
 except Exception as e:
  return False
 else:
  return True
def U(u,J,W):
 A=t.format(parse.quote(J),parse.quote(u),parse.quote(W))
 h=requests.get(A)
 P=json.loads(h.text)
 H=P.get("list")
 return H
def r(Y):
 A=K.format(Y)
 h=requests.get(A)
 P=json.loads(h.text)
 return P.get("genretext")
def D(Y,W):
 A=l.format(parse.quote(W),Y)
 h=requests.get(A)
 P=json.loads(h.text)
 b=P.get("playurl")
 a=P.get("awscookie").replace(';','&').replace(' ','')
 return b+'?'+a
def C(W,outpath):
 try:
  u=datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
  J=(datetime.datetime.today()+datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
  L=U(u,J,W)
  file=open(outpath,'w',encoding='utf8')
  file.write("#EXTM3U8\n")
  w=0
  for E in L:
   Y=E["channelid"]
   n=E["channelname"]
   I=E["channelimage"]
   b=D(Y,W)
   Q=r(Y)
   file.write('#EXTINF:-1 tvg-id="{0}" tvg-logo="https://{1}" group-title="{2}" tvg-chno="{3}",{4}\n'.format(Y,I,Q,w,n))
   file.write(b+"\n") 
   w=w+1 
 except Exception as e:
  print(str(e))
  return False
 else:
  return True
 finally:
  if not file.closed:
   file.close()
def B(x):
 x=x.replace("&","&amp;")
 x=x.replace("<","&lt;")
 x=x.replace(">","&gt;")
 x=x.replace('"',"&quot;")
 x=x.replace("'","&apos;")
 return x
def S(W,outpath):
 try:
  u=datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
  J=(datetime.datetime.today()+datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
  L=U(u,J,W)
  file=open(outpath,'w',encoding='utf8')
  file.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
  file.write('<!DOCTYPE tv SYSTEM "xmltv.dtd">\n')
  file.write('<tv generator-info-name="Raccoon\'s wavve tool v1.0">\n')
  cn=0
  for E in L:
   Y=E["channelid"]
   n=B(E["channelname"])
   file.write('  <channel id="{0}">\n'.format(Y))
   file.write('    <display-name>{0}</display-name>\n'.format(n))
   file.write('    <display-name>{0}</display-name>\n'.format("WAVVE"))
   file.write('    <display-name>{0}</display-name>\n'.format(cn))
   file.write('    <display-name>{0} {1}</display-name>\n'.format(cn,n))
   file.write('    <display-name>{0} {1}</display-name>\n'.format(cn,"WAVVE"))
   file.write('    <icon src="https://{0}" />\n'.format(E["channelimage"]))
   file.write('  </channel>\n')
   cn=cn+1
  for E in L:
   Y=E["channelid"]
   q=E["list"]
   for N in q:
    G=parse.unquote(N["title"])
    k=datetime.datetime.strptime(N["starttime"],'%Y-%m-%d %H:%M')
    f=datetime.datetime.strptime(N["endtime"],'%Y-%m-%d %H:%M')
    p=k.strftime("%Y%m%d%H%M%S")
    d=f.strftime("%Y%m%d%H%M%S")
    try:
     T=int(N["targetage"])
    except ValueError:
     T=0
    if T==0:
     j="전체 관람가"
    else:
     j="{0}세 이상 관람가".format(T)
    file.write('  <programme start="'+p+' +0900" stop="'+d+' +0900" channel="'+Y+'">\n')
    file.write('    <title lang="kr">'+B(G)+'</title>\n')
    file.write('    <desc lang="kr">'+B(G)+'\n'+j+'</desc>\n')
    file.write('    <rating system="KMRB">\n')
    file.write('      <value>{0}</value>\n'.format(j))
    file.write('    </rating>\n')
    file.write('  </programme>\n')
  file.write('</tv>') 
 except Exception as e:
  print(str(e))
  return False
 else:
  return True
 finally:
  file.close
if __name__=='__main__':
 if len(sys.argv)<5:
  print('USAGE\n  python {0} userId password EPG|M3U "outPath" \n'.format(sys.argv[0]))
 else:
  m=sys.argv[1]
  V=sys.argv[2]
  g=sys.argv[3].lower()
  c=sys.argv[4]
  W=R(m,V)
  if W!=None:
   if g=='epg':
    if S(W,c):
     print('EPG created!\n')
    else:
     print('EPG creation failed!\n')
   elif 'm3u':
    if C(W,c):
     print('M3U created!\n')
    else:
     print('M3U creation failed!\n')
   else:
    print("Invalid argument - "+g)
   o(W)
  else:
   print('Login failed! please check userid/password and try again!')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
