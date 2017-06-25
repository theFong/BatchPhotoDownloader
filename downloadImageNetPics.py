import urllib2
import sys
import threading
import time
from reprint import output
import mimetypes

def downloadPhoto(link, name, output_lines):
	
	try:
		picOnlineRef =	urllib2.urlopen(link)
		picOnline = picOnlineRef.read()
		if 'html' in picOnline:
			updateDownloadStatus(output_lines,link, name, "Failed to find photo")
			return
		url = picOnlineRef.geturl()
		if 'photo_unavailable' in url:
			updateDownloadStatus(output_lines,link, name, "Failed to find photo")
			return
	except urllib2.HTTPError as e:
		updateDownloadStatus(output_lines, link, name, str(e))
		return
	picLocal = open(out_file+str(name)+'.jpg', 'wb')
	picLocal.write(picOnline)
	picLocal.close()
	updateDownloadStatus(output_lines, link, name, "Done")

def updateDownloadStatus(output_lines, link, lineNum, status):
	returncl
	output_lines[str(lineNum)] = "{lnk} | Status: {sts}".format(
                lnk = link,
                sts = status
                )

class DownloadThread(threading.Thread):
	def __init__(self, line, count, output_lines):
		threading.Thread.__init__(self)
		self.line = line
		self.count = count
		self.output_lines = output_lines
	def run(self):
		downloadPhoto(self.line, self.count, self.output_lines)
		


source_link = sys.argv[1]
out_file = sys.argv[2]
number_of_downloads = sys.argv[3]

if __name__ == "__main__":
	with output(output_type='dict') as output_lines:
		threads = []
		print "Starting batch download from source: "+source_link
		response = urllib2.urlopen(source_link)
		links = response.read()
		count = 0
		lines = links.splitlines()
		if number_of_downloads == "":
			for line in lines:
				thread = DownloadThread(line, count, output_lines)
				threads.append(thread)
				thread.start()
				count+=1
		else:
			for i in xrange(int(number_of_downloads)):
				line = lines[i]
				thread = DownloadThread(line, count, output_lines)
				threads.append(thread)
				updateDownloadStatus(output_lines, line, count, "Downloading..")
				thread.start()
				count+=1

		for t in threads:
			t.join()
		print "All links downloaded."




# if __name__ == "__main__":
#     with output(output_type='dict') as output_lines:
#         output_lines['Moving file'] = "File_{}".format(1)
#         for progress in range(100):
#             output_lines['Total Progress'] = "[{done}{padding}] {percent}%".format(
#                 done = "#" * int(progress/10),
#                 padding = " " * (10 - int(progress/10)),
#                 percent = progress
#                 )
#             output_lines['Moving file'] = "File_{}".format(progress)
#             time.sleep(0.05)