import re,psutil,json,boto3,time,datetime,csv
def csw(d):
	with open('log.csv','a') as f:
		writer = csv.DictWriter(f,fieldnames=list(d.keys()))
		writer.writerow(d)
		f.close()
def ramck():
	rawram = psutil.virtual_memory()
	vmatr=['total','used','available','cached','percent','free']
	k={}
	for i in vmatr:
		k[i] = getattr(rawram,i)
	return k
def cpuck():
	k ={}
	k["CPU-per"] = psutil.cpu_percent(interval=1)
	k["Physical_CPU-Count"] = psutil.cpu_count(logical=False) 
	x  = str(psutil.cpu_freq())[9:-1].split(',')
	for i in x:
		k[i.split('=')[0]] = i.split('=')[1]
	return k
def sendData(s,d,k):
	k.put_object(Body=json.dumps(d),Bucket='harsha1221',Key=s)
	k.put_object_acl(ACL='public-read',Bucket='harsha1221',Key=s)
def dskusg():
	k={}
	m = psutil.disk_usage('/')
	l = ['total','used','free','percent']
	for i in l:
		k[i]=getattr(m,i)
	return k
def swp():
	k={}
	m = psutil.swap_memory()
	for i in ['total','used','free','percent']:
		k[i]=getattr(m,i)
	return k
def dskio():
	k={}
	m = psutil.disk_io_counters()
	for i in ['read_count','write_count','read_bytes','write_bytes']:
		k[i]=getattr(m,i)
	return k
def ntwrkio():
	k={}
	m = psutil.net_io_counters()
	for i in ['packets_sent','packets_recv','dropin','dropout']:
		k[i]=getattr(m,i)
	return k
def bootym():
	return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
def users():
	return 0
def process():
	return {p.pid:p.info for p in psutil.process_iter(['name','username'])}
b = time.time()
d={}
k=boto3.client('s3')
d['Memory']=ramck()
d['CPU']=cpuck()
d['Disk_Utilization']=dskusg()
d['Swap_Memory']=swp()
d['Disk_IO']=dskio()
d['Network_IO']=ntwrkio()
d['Boot_Time']=bootym()
d['Processes_By_PIDs']=process()
sendData('mini.json',d,k)
csw(d)
print(time.time()-b)