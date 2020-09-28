
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
import cgi

def rot13(a):
    list1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    list2 = 'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
    result = ''
    for e in a:
        if e in list1:
            result = result + list2[list1.find(e)]
        else:
            result = result + e
    return result

def escape_html(s):
        return cgi.escape(s, quote = True)

form ='''
<form method= "post">
        Enter some text here to ROT
        <br>
        <textarea input type="text" name="text">%(text)s</textarea>
        <br>
        <input type="submit" value='Submit'>
</form>
'''
class MainHandler(webapp2.RequestHandler):
    def write_form(self,text=""):
        self.response.write(form % {"text" : escape_html(text)})
    def get(self):
        self.write_form()
    def post(self):
        stringtoconvert = self.request.get('text')
        convertedstring = rot13(stringtoconvert)
        self.write_form(convertedstring)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
