#! /usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
import sys
import wifi_mapper
from flask import Flask, render_template, make_response, redirect, request, send_from_directory, url_for
app = Flask(__name__)
pcap_lst = list()
pcap_success = list()

@app.route('/')
@app.route('/pcap')
@app.route('/pcap/')
@app.route('/pcap/<int:num>')
def reviews(num=0):
	"""
		Main interface
	"""
	if len(pcap_lst) <= num or pcap_lst[num] is None:
		return redirect("/pcap/")
	return render_template('pcap_review.html',
							file_names=pcap_success,
							file_n=len(pcap_success),
							page_num=num,
							get_broadcast=wifi_mapper.get_broadcast,
							handshakes=pcap_lst[num]['Handshakes'],
							ap=pcap_lst[num]['AP'],
							station=pcap_lst[num]['Station'],
							traffic=pcap_lst[num]['Traffic'])

@app.route('/pcap/<int:num>/traffic', methods=['GET'])
def traffic_detail(num=0):
	"""
		Traffic detail between station and ap
		Uses ?sta=some_mac_addr&ap=some_bssid keys
	"""
	if len(pcap_lst) <= num or pcap_lst[num] is None:
		return redirect("/pcap/")
	dic = request.args.to_dict()
	if not isinstance(dic, dict) or\
		'sta' not in dic or 'ap' not in dic or\
		dic['sta'] not in pcap_lst[num]['Station'] or\
		dic['sta'] not in pcap_lst[num]['Traffic']:
		return redirect("/pcap/%d" % num)
	return render_template('pcap_traffic.html',
							file_names=pcap_success,
							file_n=len(pcap_success),
							page_num=num,
							ap=dic['ap'],
							sta=dic['sta'],
							station=pcap_lst[num]['Station'][dic['sta']],
							traffic=pcap_lst[num]['Traffic'][dic['sta']])

@app.route('/pcap/<int:num>/handshake', methods=['GET'])
def dl_handshake(num=0):
	"""
		Download handshake between ap and station
		Uses ?sta=some_mac_addr&ap=some_bssid keys
	"""
	if len(pcap_lst) <= num or pcap_lst[num] is None:
		return redirect("/pcap/")
	dic = request.args.to_dict()
	if not isinstance(dic, dict) or\
		'sta' not in dic or 'ap' not in dic or\
		dic['sta'] not in pcap_lst[num]['Station']:
		return redirect("/pcap/%d" % num)
	name = "bssid_{}_sta_{}_hdshake.pcap".format(dic['sta'], dic['ap'])
	path = "/tmp/{}".format(name)
	ret = wifi_mapper.get_handshake_pcap(pcap_lst[num], dic['sta'], dic['ap'], path)
	if not ret:
		return make_response("No such wpa handshake", 404)
	return send_from_directory("/tmp", name,
		mimetype="application/vnd.tcpdump.pcap",
		as_attachment=True,
		attachment_filename=name)

@app.route('/pcap/<int:num>/station_handshake', methods=['GET'])
def dl_station_handshake(num=0):

	"""
		Download all station handshakes
		Uses ?sta=some_mac_addr key
	"""
	if len(pcap_lst) <= num or pcap_lst[num] is None:
		return redirect("/pcap/")
	dic = request.args.to_dict()
	if not isinstance(dic, dict) or\
		'sta' not in dic or\
		dic['sta'] not in pcap_lst[num]['Station']:
		return redirect("/pcap/%d" % num)
	name = "station_{}_hdshake.pcap".format(dic['sta'])
	path = "/tmp/{}".format(name)
	ret = wifi_mapper.get_station_handshake_pcap(pcap_lst[num], dic['sta'], path)
	if not ret:
		return make_response("No such wpa handshake", 404)
	return send_from_directory("/tmp", name,
		mimetype="application/vnd.tcpdump.pcap",
		as_attachment=True,
		attachment_filename=name)

@app.route('/pcap/<int:num>/all_handshake')
def dl_file_handshake(num=0):
	"""
		Download all handshakes present in file
	"""
	if len(pcap_lst) <= num or pcap_lst[num] is None:
		return redirect("/pcap/")
	name = "file_{0}_hdshakes.pcap".format(num)
	path = "/tmp/{}".format(name)
	ret = wifi_mapper.get_all_handshake_pcap(pcap_lst[num], path)
	if not ret:
		return make_response("No such wpa handshake", 404)
	return send_from_directory("/tmp", name,
		mimetype="application/vnd.tcpdump.pcap",
		as_attachment=True,
		attachment_filename=name)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		for pcap_file in sys.argv[1:]:
			dic = wifi_mapper.parse(pcap_file)
			if dic is not None:
				pcap_lst.append(dic)
				pcap_success.append(pcap_file)
		if len(pcap_success):
			app.run(debug=False)
		else:
			print("Error: none of the files provided are usable",
				file=sys.stderr)
	else:
		print("Error: please provide a pcap file", file=sys.stderr)

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
