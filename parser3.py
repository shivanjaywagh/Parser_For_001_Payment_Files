import re
import pandas as pd
from re import finditer




def nextword(target, source):
	for i, w in enumerate(source):
		if w == target:
			return source[i+1]









def fetchvalue(searchregex , block):
	sll1 = ""
	splitblock = re.split(searchregex,  block, flags=re.M)
	print("*************************************************************************")
	search_regex_present = re.search(searchregex, block)
	if bool(search_regex_present):
		aftersearchstr=str(splitblock[1])
		sll = aftersearchstr.split()
		sll1 = str(sll[0])
		print(searchregex)
		print(sll1)
		return sll1

	return sll1



def tabletype(block):


	varrr = re.search("CLEARING CYCLE 004 - ACKNOWLEDGEMENT", block)
	if bool(varrr):
		temp = re.search("NO DATA TO REPORT", block)
		if bool(temp):
			return 1 , 1

		return 1, 0

	varrr = re.search("CLEARING CYCLE 004 - NOTIFICATION", block)
	if bool(varrr):
		temp = re.search("NO DATA TO REPORT", block)
		if bool(temp):
			return 2 , 1

		return 2, 0
	
	
	varrr = re.search("CLEARING CYCLE 004 SUMMARY", block)
	if bool(varrr):
		temp = re.search("NO DATA TO REPORT", block)
		if bool(temp):
			return 4 , 1

		return 4, 0
	
	varrr = re.search("CLEARING DAY TOTAL", block)
	if bool(varrr):
		temp = re.search("NO DATA TO REPORT", block)
		if bool(temp):
			return 5 , 1

		return 5, 0

	varrr = re.search("CLEARING CYCLE 004", block)
	if bool(varrr):
		temp = re.search("NO DATA TO REPORT", block)
		if bool(temp):
			return 3 , 1

		return 3, 0

	


def table_processing(table_type, block, result_dict):
	dicttt = result_dict
	search_empty_line = r'[\s]+[\n]'
	regex_empty_line=r'^[\s]+$'
	searchcols = r'[-]{2,}|[_]{2,}'


	span_list = []
	empty_line_index = []
	table_start_line_index = [99]
	col_start_line_index = [99]
	table_end_line_index = [99]
	linenumbers = []
	no_of_cols = 0



	if table_type==2:    
		print("kjhkjhfskdddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkkksssssssssssssssssss")          #CLEARING CYCLE 004 - NOTIFICATION
		linesrows = block.split('\n')	#split block into lines

		for i in range(len(linesrows)):
			varr = re.search(regex_empty_line,str(linesrows[i]) , flags=re.M)      #this regex works for empty line
			if bool(varr):
				empty_line_index.append(i)

		print(empty_line_index , "empty lines indexes")



		#finding hiphen line indexes
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
				linenumbers.append(i) 
		#finding empty line through 4 diff with linenumbers[0] 
		print(linenumbers[0], "linenumbers")
		for i in range(len(empty_line_index)):
			if (linenumbers[0]-empty_line_index[i]) < 5 and (linenumbers[0]-empty_line_index[i]) > 0:
				table_start_line_index[0] = empty_line_index[i] 
				break  #
		# if two hiphen lines found then do this
		if len(linenumbers) ==2:
			col_start_line_index[0]  = linenumbers[0] #
			table_end_line_index[0] =linenumbers[1]    #
		#if only one hiphen line found then keep searching for empty line for table end
		elif len(linenumbers) ==1:
			col_start_line_index[0]  = linenumbers[0]
			for i in range(len(empty_line_index)):
				if (empty_line_index[i] > linenumbers[0]):
					table_end_line_index[0] = empty_line_index[i]

		print(table_start_line_index , col_start_line_index , table_end_line_index)

		#now span list
		
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
			
				for match in finditer(searchcols, str(linesrows[i])):
					print(match.span(), match.group())
					span_list.append(match.span())
					no_of_cols = no_of_cols + 1
		if len(linenumbers) ==2:
			span_list = span_list[:int(len(span_list)/2)]
			no_of_cols = int(no_of_cols/2)

			print(span_list, "span list")

		elif len(linenumbers) ==1:
			span_list = span_list
			no_of_cols = no_of_cols
			print(span_list, "span list")

		print(no_of_cols)

		col_names = []
		for i in range(no_of_cols):
			col_names.append("")

		for j in range(no_of_cols):
			for i in range(table_start_line_index[0] , col_start_line_index[0]):
				col_names[j] = col_names[j] + linesrows[i][int(span_list[j][0]):int(span_list[j][1])]
				print("colname1", col_names[j])

		for i in range(no_of_cols):
			col_names[i]= re.sub(r'[\s]',"", col_names[i])

		for i in range(no_of_cols):
			dicttt[col_names[i]] = {}

		for j in range(no_of_cols):
			for i in range(col_start_line_index[0]+1,table_end_line_index[0]):
				dicttt[col_names[j]][i] = linesrows[i][int(span_list[j][0]):int(span_list[j][1])]

		return dicttt












		




				

		





















































		'''
		searchtable = "MEMBER ID: 00000016987"
		tableblock = re.split(r"\b" + searchtable + r"\b", block)				
		#string			blocks[2] has the one block
		print("table block below:")
		print(tableblock[1])
		tableblock = tableblock[1]


		#finding number of cols
		searchcols = r'[-]{2,}|[_]{2,}'
		colsresult = re.findall(searchcols, block)
		#print(colsresult.span())
		print("len of colsresult",len(colsresult))	
		no_of_cols = int(len(colsresult)/2)	
		print(no_of_cols)


		span_list = []
		linenumbers = []


		linesrows = tableblock.split('\n')
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
				linenumbers.append(i)
				for match in finditer(searchcols, str(linesrows[i])):
					print(match.span(), match.group())
					span_list.append(match.span())





		print(span_list)
		span_list = span_list[:int(len(span_list))]
		print(span_list)
		# print(span_list[0][1])
		print("linenumbers =" , linenumbers)



		col_names = []
		for i in range(no_of_cols):
			col_names.append("")

		k=0
		for j in range(no_of_cols):
			for i in range(0,linenumbers[0]):
				col_names[j] = col_names[j] + linesrows[i][int(span_list[j][0]):int(span_list[j][1])]
				print("colname1", col_names[j])
				



		for i in range(no_of_cols):
			col_names[i]= re.sub(r'[\s]',"", col_names[i])






		for i in range(no_of_cols):
			dicttt[col_names[i]] = {}




		j = 0
		k=0

		for j in range(no_of_cols):
			for i in range(linenumbers[0]+1,linenumbers[1]):
				dicttt[col_names[j]][i] = linesrows[i][int(span_list[j][0]):int(span_list[j][1])]

		return dicttt
		'''



	elif table_type==3:    # CLEARING CYCLE 004

		print("kjhkjhfskdddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkkksssssssssssssssssss")          #CLEARING CYCLE 004 - NOTIFICATION
		linesrows = block.split('\n')	#split block into lines

		for i in range(len(linesrows)):
			varr = re.search(regex_empty_line,str(linesrows[i]) , flags=re.M)      #this regex works for empty line
			if bool(varr):
				empty_line_index.append(i)

		print(empty_line_index , "empty lines indexes")



		#finding hiphen line indexes
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
				linenumbers.append(i) 
		#finding empty line through 4 diff with linenumbers[0] 
		print(linenumbers[0], "linenumbers")
		for i in range(len(empty_line_index)):
			if (linenumbers[0]-empty_line_index[i]) < 5 and (linenumbers[0]-empty_line_index[i]) > 0:
				table_start_line_index[0] = empty_line_index[i] 
				break  #
		# if two hiphen lines found then do this
		if len(linenumbers) ==2:
			col_start_line_index[0]  = linenumbers[0] #
			table_end_line_index[0] =linenumbers[1]    #
		#if only one hiphen line found then keep searching for empty line for table end
		elif len(linenumbers) ==1:
			col_start_line_index[0]  = linenumbers[0]
			for i in range(len(empty_line_index)):
				if (empty_line_index[i] > linenumbers[0]):
					table_end_line_index[0] = empty_line_index[i]

		print(table_start_line_index , col_start_line_index , table_end_line_index)

		#now span list
		
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
			
				for match in finditer(searchcols, str(linesrows[i])):
					print(match.span(), match.group())
					span_list.append(match.span())
					no_of_cols = no_of_cols + 1
		if len(linenumbers) ==2:
			span_list = span_list[:int(len(span_list)/2)]
			no_of_cols = int(no_of_cols/2)

			print(span_list, "span list")

		elif len(linenumbers) ==1:
			span_list = span_list
			no_of_cols = no_of_cols
			print(span_list, "span list")

		print(no_of_cols)

		col_names = []
		for i in range(no_of_cols):
			col_names.append("")

		for j in range(no_of_cols):
			for i in range(table_start_line_index[0] , col_start_line_index[0]):
				col_names[j] = col_names[j] + linesrows[i][int(span_list[j][0]):int(span_list[j][1])]
				print("colname1", col_names[j])

		for i in range(no_of_cols):
			col_names[i]= re.sub(r'[\s]',"", col_names[i])

		for i in range(no_of_cols):
			dicttt[col_names[i]] = {}

		for j in range(no_of_cols):
			for i in range(col_start_line_index[0]+1,table_end_line_index[0]):
				dicttt[col_names[j]][i] = linesrows[i][int(span_list[j][0]):int(span_list[j][1])]

		return dicttt



	elif table_type ==4:        #CLEARING CYCLE 004 SUMMARY
		print("kjhkjhfskdddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkkksssssssssssssssssss")          #CLEARING CYCLE 004 - NOTIFICATION
		linesrows = block.split('\n')	#split block into lines

		for i in range(len(linesrows)):
			varr = re.search(regex_empty_line,str(linesrows[i]) , flags=re.M)      #this regex works for empty line
			if bool(varr):
				empty_line_index.append(i)

		print(empty_line_index , "empty lines indexes")



		#finding hiphen line indexes
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
				linenumbers.append(i) 
		#finding empty line through 4 diff with linenumbers[0] 
		print(linenumbers[0], "linenumbers")
		for i in range(len(empty_line_index)):
			if (linenumbers[0]-empty_line_index[i]) < 5 and (linenumbers[0]-empty_line_index[i]) > 0:
				table_start_line_index[0] = empty_line_index[i] 
				break  #
		# if two hiphen lines found then do this
		if len(linenumbers) ==2:
			col_start_line_index[0]  = linenumbers[0] #
			table_end_line_index[0] =linenumbers[1]    #
		#if only one hiphen line found then keep searching for empty line for table end
		elif len(linenumbers) ==1:
			col_start_line_index[0]  = linenumbers[0]
			for i in range(len(empty_line_index)):
				if (empty_line_index[i] > linenumbers[0]):
					table_end_line_index[0] = empty_line_index[i]

		print(table_start_line_index , col_start_line_index , table_end_line_index)

		#now span list
		
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
			
				for match in finditer(searchcols, str(linesrows[i])):
					print(match.span(), match.group())
					span_list.append(match.span())
					no_of_cols = no_of_cols + 1
		if len(linenumbers) ==2:
			span_list = span_list[:int(len(span_list)/2)]
			no_of_cols = int(no_of_cols/2)

			print(span_list, "span list")

		elif len(linenumbers) ==1:
			span_list = span_list
			no_of_cols = no_of_cols
			print(span_list, "span list")

		print(no_of_cols)

		col_names = []
		for i in range(no_of_cols):
			col_names.append("")

		for j in range(no_of_cols):
			for i in range(table_start_line_index[0] , col_start_line_index[0]):
				col_names[j] = col_names[j] + linesrows[i][int(span_list[j][0]):int(span_list[j][1])]
				print("colname1", col_names[j])

		for i in range(no_of_cols):
			col_names[i]= re.sub(r'[\s]',"", col_names[i])

		for i in range(no_of_cols):
			dicttt[col_names[i]] = {}

		for j in range(no_of_cols):
			for i in range(col_start_line_index[0]+1,table_end_line_index[0]):
				dicttt[col_names[j]][i] = linesrows[i][int(span_list[j][0]):int(span_list[j][1])]

		return dicttt
		

			#pura tableblock iterate till end


		

	elif table_type == 1:
		print("kjhkjhfskdddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkkksssssssssssssssssss")          #CLEARING CYCLE 004 - NOTIFICATION
		linesrows = block.split('\n')	#split block into lines

		for i in range(len(linesrows)):
			varr = re.search(regex_empty_line,str(linesrows[i]) , flags=re.M)      #this regex works for empty line
			if bool(varr):
				empty_line_index.append(i)

		print(empty_line_index , "empty lines indexes")



		#finding hiphen line indexes
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
				linenumbers.append(i) 
		#finding empty line through 4 diff with linenumbers[0] 
		print(linenumbers[0], "linenumbers")
		for i in range(len(empty_line_index)):
			if (linenumbers[0]-empty_line_index[i]) < 5 and (linenumbers[0]-empty_line_index[i]) > 0:
				table_start_line_index[0] = empty_line_index[i] 
				break  #
		# if two hiphen lines found then do this
		if len(linenumbers) ==2:
			col_start_line_index[0]  = linenumbers[0] #
			table_end_line_index[0] =linenumbers[1]    #
		#if only one hiphen line found then keep searching for empty line for table end
		elif len(linenumbers) ==1:
			col_start_line_index[0]  = linenumbers[0]
			for i in range(len(empty_line_index)):
				if (empty_line_index[i] > linenumbers[0]):
					table_end_line_index[0] = empty_line_index[i]

		print(table_start_line_index , col_start_line_index , table_end_line_index)

		#now span list
		
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
			
				for match in finditer(searchcols, str(linesrows[i])):
					print(match.span(), match.group())
					span_list.append(match.span())
					no_of_cols = no_of_cols + 1
		if len(linenumbers) ==2:
			span_list = span_list[:int(len(span_list)/2)]
			no_of_cols = int(no_of_cols/2)

			print(span_list, "span list")

		elif len(linenumbers) ==1:
			span_list = span_list
			no_of_cols = no_of_cols
			print(span_list, "span list")

		print(no_of_cols)

		col_names = []
		for i in range(no_of_cols):
			col_names.append("")

		for j in range(no_of_cols):
			for i in range(table_start_line_index[0] , col_start_line_index[0]):
				col_names[j] = col_names[j] + linesrows[i][int(span_list[j][0]):int(span_list[j][1])]
				print("colname1", col_names[j])

		for i in range(no_of_cols):
			col_names[i]= re.sub(r'[\s]',"", col_names[i])

		for i in range(no_of_cols):
			dicttt[col_names[i]] = {}

		for j in range(no_of_cols):
			for i in range(col_start_line_index[0]+1,table_end_line_index[0]):
				dicttt[col_names[j]][i] = linesrows[i][int(span_list[j][0]):int(span_list[j][1])]

		return dicttt


	elif table_type == 5:
		print("kjhkjhfskdddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkkksssssssssssssssssss")          #CLEARING CYCLE 004 - NOTIFICATION
		linesrows = block.split('\n')	#split block into lines

		for i in range(len(linesrows)):
			varr = re.search(regex_empty_line,str(linesrows[i]) , flags=re.M)      #this regex works for empty line
			if bool(varr):
				empty_line_index.append(i)

		print(empty_line_index , "empty lines indexes")



		#finding hiphen line indexes
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
				linenumbers.append(i) 
		#finding empty line through 4 diff with linenumbers[0] 
		print(linenumbers[0], "linenumbers")
		for i in range(len(empty_line_index)):
			if (linenumbers[0]-empty_line_index[i]) < 5 and (linenumbers[0]-empty_line_index[i]) > 0:
				table_start_line_index[0] = empty_line_index[i] 
				break  #
		# if two hiphen lines found then do this
		if len(linenumbers) ==2:
			col_start_line_index[0]  = linenumbers[0] #
			table_end_line_index[0] =linenumbers[1]    #
		#if only one hiphen line found then keep searching for empty line for table end
		elif len(linenumbers) ==1:
			col_start_line_index[0]  = linenumbers[0]
			for i in range(len(empty_line_index)):
				if (empty_line_index[i] > linenumbers[0]):
					table_end_line_index[0] = empty_line_index[i]

		print(table_start_line_index , col_start_line_index , table_end_line_index)

		#now span list
		
		for i in range(len(linesrows)):
			temp = re.search(searchcols, str(linesrows[i]))
			if bool(temp):
			
				for match in finditer(searchcols, str(linesrows[i])):
					print(match.span(), match.group())
					span_list.append(match.span())
					no_of_cols = no_of_cols + 1
		if len(linenumbers) ==2:
			span_list = span_list[:int(len(span_list)/2)]
			no_of_cols = int(no_of_cols/2)

			print(span_list, "span list")

		elif len(linenumbers) ==1:
			span_list = span_list
			no_of_cols = no_of_cols
			print(span_list, "span list")

		print(no_of_cols)

		col_names = []
		for i in range(no_of_cols):
			col_names.append("")

		for j in range(no_of_cols):
			for i in range(table_start_line_index[0] , col_start_line_index[0]):
				col_names[j] = col_names[j] + linesrows[i][int(span_list[j][0]):int(span_list[j][1])]
				print("colname1", col_names[j])

		for i in range(no_of_cols):
			col_names[i]= re.sub(r'[\s]',"", col_names[i])

		for i in range(no_of_cols):
			dicttt[col_names[i]] = {}

		for j in range(no_of_cols):
			for i in range(col_start_line_index[0]+1,table_end_line_index[0]):
				dicttt[col_names[j]][i] = linesrows[i][int(span_list[j][0]):int(span_list[j][1])]

		return dicttt













		










def parse_doc(filename):
	f = open(filename, "r")
	count = 0
	lines = f.read()

	search="MASTERCARD WORLDWIDE"

	result_dict = {}
	blocks = re.split(r"\b" + search + r"\b", lines)	#the whole file is now split into blocks, where the seperator is the keyword 'MASTERCARD WORLDWIDE'			
	#string			blocks[2] has the one block
	block = blocks[1]   #each block corresponds to one table and its meta data like mcc etc , so if you want to run this for the whole file , put a for loop with block[i] and iteratively pass the block[i] to the below code routine. here i have implemented it only for one block

	print("block :::::::", block)
	table_type, noreport_yes = tabletype(block)
	print("table_type =", table_type)
	if noreport_yes==1:  #means no data to report
		dictt['NO data to report'][0] = "NO DATA TO REPORT"
		data = pd.DataFrame(dictt) 
		data.to_excel("outputtttt8.xlsx")












	# tt = re.search(r'[\s]+[\n]',str(block) , flags=re.M)
	# if bool(tt):
	# 	print("********************yes my all space line regex works")


	#meta values finding func here

	searcharr = []
	searcharr.append("BUSINESS SERVICE ID:")
	searcharr.append("FILE ID:")
	searcharr.append("MEMBER ID:")
	searcharr.append("PAGE NO:")
	searcharr.append("RUN DATE:")
	searcharr.append("ACCEPTANCE BRAND:")
	searcharr.append("BUSINESS SERVICE LEVEL:")
	searcharr.append("RUN TIME:")
	searcharr.append("CURRENCY CODE :")
	searcharr.append("PAGE NO:")




	dicttt={}

	for i in range(1,len(searcharr)):
		result_dict[searcharr[i]] = {}
		result_dict[str(searcharr[i])]['0'] = fetchvalue(searcharr[i], block)
		print("i=" , i)
		print(result_dict)


	result_dict2 = table_processing(table_type, block , result_dict)

	data = pd.DataFrame(result_dict2) 
	data.to_excel("outputtttt1.xlsx")
	


if __name__ == '__main__':
	filename = "TT140T0.2018-05-26-15-58-26"

	parse_doc(filename)













