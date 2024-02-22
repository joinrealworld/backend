from channel.models import *
import json
import os
import re
import uuid


def format_section_data_obj(data, counter):
	if "image_path" not in data.keys():
		data["image_path"] = ""
	if "section_url" not in data.keys():
		data["section_url"] = ""
	if data["section"] == "quiz":
		data['quiz_id'] = counter
		counter += 1
	data["is_favourite"] = False
	data["uuid"] = str(uuid.uuid4())
	return data, counter
	
def format_jsondata(json_data):
	section_data = json_data["sections"]
	counter = 1
	updated_section_data = []
	for data in section_data:
		data, counter = format_section_data_obj(data, counter)
		updated_section_data.append(data)
	return updated_section_data

def add_quiz_data(quiz_json_data, dir_name):
	course = Courses.objects.filter(name = dir_name)
	for key, value in quiz_json_data.items():
		match = re.match(r'^que(\d+)$', key)
		index = 0
		if match:
			digit = match.group(1)
			index = int(digit)+1
			CourseQuiz.objects.create(course = course.last(), data = value, index = index)
		
def get_channel_data():
	""" formating the bot data """
	channels_dict = {}
	added_data = []
	# Iterate through the directory tree starting from 'channel/data/attachments'
	for root, dirs, files in os.walk('channel/attachments'):
		for d in dirs:
			added_data.append(d)
			for root, dirs, files in os.walk(f'channel/attachments/{d}'):
				for filename in files: # for channel data except quiz
					if filename == 'messages.json':
						message_json_path = os.path.join(root, filename)
						with open(message_json_path, 'r') as file:
							json_data = json.load(file)
							Courses.objects.create(data = format_jsondata(json_data), category = Category.objects.last(), name=d)
					if filename == "quiz4.json": # for quiz data
						quiz_json_path = os.path.join(root, filename)
						with open(quiz_json_path, 'r') as file:
							quiz_json_data = json.load(file)
							add_quiz_data(quiz_json_data, d)

	return channels_dict

def count_completed_course(user, course):
	try:
		course_data = course.data
		data_len = len(course_data)
		completed_content = CompleteContent.objects.filter(course = course, user = user)
		len_compeleted_content =  len(completed_content)
		return round((100*len_compeleted_content)/data_len,2)
	except Exception as e:
		return 0

def count_completed_category(user, category):
	courses = Courses.objects.filter(category = category)
	compeleted_cat = 0
	for course in courses:
		compeleted_cat = compeleted_cat +count_completed_course(user, course)
	return round(compeleted_cat/len(courses),2)






