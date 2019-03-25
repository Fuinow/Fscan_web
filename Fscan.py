from Domain_Collect import DomainCollect
from Scanner import Scanner
from flask import Flask, render_template
from outputer import Outputer
import multiprocessing
app = Flask(__name__)


@app.route('/')
def index():
	root_domains = Outputer().get_collection_name()
	return render_template("index.html", root_domains=root_domains)

@app.route('/domain/<root_domain>')
def domain(root_domain):
		domains_temp = Outputer().get_domain_list(root_domain)
		domains = []
		num = 1
		for domain in domains_temp:
			domain["num"] = num 
			domains.append(domain)
			num += 1
		return render_template("domain.html", domains=domains, root_domain=root_domain)

@app.route('/info/<root_domain>/<domain>')
def info(root_domain, domain):
	data = Outputer().get_info(root_domain, domain)
	_dir = data.get("dir")
	ports = data.get("port")
	finger = data.get("finger")
	poc = data.get("poc")
	ip = data.get("ip")
	if not ports:
		ports = []
	return render_template('info.html', _dir=_dir, ports=ports, finger=finger, poc=poc, ip=ip)

@app.route('/scan/<root_domain>/<domain>/<type>')
def scan(root_domain, domain, type):
	scanner.add_task(root_domain, domain, type)
	dic = {"dir":0,"port":1,"finger":2,"poc":3}
	if type in dic.keys():
		Outputer().change_scan_state(root_domain, domain, dic[type], "info")
	return 'ok'

@app.route('/domain_col/<domain>')
def collect_domain(domain):
	domain_col= DomainCollect(domain)
	domain_col.run()
	return 'ok'

@app.route('/test')
def test(data):
	resp = jsonify({'code':0, 'message':"test", 'msg':"test", 'data':{
	"redirectUrl":"http://baidu.com"}})
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


if __name__ == '__main__':
	scanner = Scanner()
	p = multiprocessing.Process(target=scanner.run)
 	p.start()
	app.run("0.0.0.0")