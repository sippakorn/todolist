#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
from google.appengine.ext import ndb

class Todo(ndb.Model):
	""" Todo list model ^_^ """
	description = ndb.StringProperty(indexed=False)
	completed = ndb.BooleanProperty()

	def put(self):
		self.description = self.description.replace("+"," ")
		super(Todo,self).put()
		return self.__dict()

	def get(self):
		return self.__dict()

	def __dict(self):
		todo_dict = dict();
		todo_dict['id'] = self.key.id()
		todo_dict['description'] = self.description
		todo_dict['completed'] = self.completed
		return todo_dict


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class TaskHandler(webapp2.RequestHandler):
	def put(self,id):
		todo = ndb.Key('Todo',int(id)).get()
		if todo == None:
			res_dict = dict()
			res_dict['error_code'] = 500
			res_dict['description'] = 'Try to delete not existed entity!'
			txt = json.dumps(res_dict)
			self.response.status_int = 500
			self.response.headers['Content-Type'] = 'application/json'
			self.response.write(txt)
		else:
			if self.request.get('description') != '':
				todo.description = self.request.get('description')

			if self.request.get('completed').lower() == 'false':
				todo.completed = False
			else:
				todo.completed = True

			todo_dict = todo.put()
			self.response.status_int = 200
			self.response.headers['Content-Type'] = 'application/json'
			self.response.write(json.dumps(todo_dict))

	def delete(self,id):
		todo_key = ndb.Key('Todo',int(id))
		if todo_key.get() != None:
			todo_key.delete()
			self.response.status_int = 200
		else:
			res_dict = dict()
			res_dict['error_code'] = 500
			res_dict['description'] = 'Try to delete not existed entity!'
			txt = json.dumps(res_dict)
			self.response.status_int = 500
			self.response.headers['Content-Type'] = 'application/json'
			self.response.write(txt)


class TasksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.status_int = 200
		self.response.headers['Content-Type'] = 'application/json'
		list_todo = list()
		for item in Todo.query().iter():
			list_todo.append(item.get())
			
		txt = json.dumps(list_todo)
		self.response.write(txt)

	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		if self.request.get('description') == "":
			self.response.status_int = 500
			res_dict = dict()
			res_dict['error_code'] = 500
			res_dict['description'] = 'User content not provided!'
			txt = json.dumps(res_dict)
			self.response.write(txt)
		else :
			self.response.status_int = 201
			des = self.request.get('description')
			# instantiate new todo
			todo = Todo()
			todo.description = des
			todo.completed = False
			todo_dict = todo.put()
			txt = json.dumps(todo_dict)
			self.response.write(txt)


		# self.response.write(des)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/tasks', TasksHandler),
    ('/task/(\d+)', TaskHandler)
], debug=True)
