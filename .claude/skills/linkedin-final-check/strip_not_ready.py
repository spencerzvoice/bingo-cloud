import base64, sys, re, json
def strip(raw):
    b=base64.urlsafe_b64decode(raw+'='*(-len(raw)%4)).decode('utf-8')
    head,body=b.split('\r\n\r\n',1)
    keep=[l for l in head.split('\r\n') if re.match(r'(To|From|Subject|MIME-Version|Content-Type|Content-Transfer-Encoding):',l)]
    body2,n=re.subn(r'<span style="background-color:#ffff00">\[NOT READY:[^\]]*\]</span><br><br>','',body,count=1)
    assert n==1 and 'NOT READY' not in body2
    return base64.urlsafe_b64encode(('\r\n'.join(keep)+'\r\n\r\n'+body2).encode('utf-8')).decode()
d=json.load(open(sys.argv[1]))
for k,v in d.items(): print('=='+k); print(strip(v))
