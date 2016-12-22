from requests import session
from time import sleep
from multiprocessing import Pool
import re 	#regex
import sys 	#input

#require
urlLogin = 'http://dangkyhoc.vnu.edu.vn/dang-nhap'
urlSelect = 'http://dangkyhoc.vnu.edu.vn/chon-mon-hoc/' # + rowindex + '/1/1'
urlConfirm = 'http://dangkyhoc.vnu.edu.vn/xac-nhan-dang-ky/1'
urlSchoolList = 'http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc/1/1'
urlYourList = 'http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc-da-dang-ky/1'

#non-require
urlPageReg = 'http://dangkyhoc.vnu.edu.vn/dang-ky-mon-hoc-nganh-1'
# urlCheck = 'http://dangkyhoc.vnu.edu.vn/kiem-tra-tien-quyet/' # + id + '/1'



msv = ''
passwd = '' 
listClassId = ['MAT1093 4', 'HIS1002 5', 'PHY1103 2']

def main():
	#sys input
	register(listClassId)


#return '' if false
def login():
	global requestToken
	global cookies
	global msv
	global passwd

	sess = session()


	loginName = msv
	password = passwd

	if loginName == '' or password == '':
		print 'Login error'
		return ''


	match = re.search( '__RequestVerificationToken" type="hidden" value="(.*?)"', sess.get(urlLogin).text)
	if not match:
		return ''

	token = match.group(1)
	

	data = {'__RequestVerificationToken' : token, 'LoginName' : loginName, 'Password' : password}
	if not re.search('Logout', sess.post(urlLogin, data=data).text):
		print 'Wrong username or password'
		requestToken = ''
		return ''

	sess.headers.update({'referer': urlPageReg})

	return sess

def get_class_index(classId, sess):
	print classId, ': Getting index...'

	if sess == '':
		print classId, ': get index error'
		return ''

	while 1:
		sourceListReg = sess.post(urlSchoolList).text
		for row in re.findall('(?s)\<tr(.*?)\<\/tr', sourceListReg):
			if classId in row:
				mIndex = re.findall('data-rowindex="(.*?)"', row)
				if mIndex:
					return mIndex[0]					
		sleep(0.5)


	return ''

def process_register(classId):
	sess = login()

	if sess == '':
		return ''
	# check current
	if classId in sess.post(urlYourList).text:
		print classId, ': register successfully'
		return ''

	classIndex = get_class_index(classId, sess)
	if classId == '':
		return
	print classId, ': Trying to register...'

	while 1:
		sess.post(urlSelect + classIndex + '/1/1')
		sess.post(urlConfirm)
		if classId in sess.post(urlYourList).text:
			print classId, ': register successfully'
			return ''

# listClassId: danh sach ma lop mon hoc
def register(listClassId, multiproc=1):

	sess = login()
	if sess == '':
		return

	print "Start: You have", len( re.findall( '\<tr', sess.post(urlYourList).text) ), 'classes!\r\n'
	if multiproc:
		proc = Pool(processes=5)
		proc.map(process_register, listClassId)
		proc.close() # this means that no more tasks will be added to the pool
		proc.join() # this blocks the program till function is run on all the items

	else:
		for classId in listClassId:
			process_register(classId)

	if sess == '':
		return
	print "Finish: You have", len( re.findall( '\<tr', sess.post(urlYourList).text) ), 'classes!\r\n'


if __name__ == '__main__':
    main()