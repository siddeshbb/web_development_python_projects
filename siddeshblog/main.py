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
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return USER_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")   
def valid_email(email):
    return EMAIL_RE.match(email)

form = """

    <html>
        <head>
            <title>Sign In Page </title>
        <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
        </head>

    <body>
    <form method = post>

    <h3> Please enter your information below: </h3>
    <br>
    <br>

    <table>
    <tr><td class="userinput"> Username <input type="text" name="username" value=%(username)s></td><td id="error">%(error1)s</td></tr>

    <tr><td class="userinput"> Password <input type="text" name="password" value=%(password1)s></td><td id="error">%(error2)s</td></tr>

    <tr><td class="userinput"> Confirm Password <input type="text" name="verify" value=%(password2)s></td><td>%(error3)s</td></tr>

    <tr><td class="userinput"> Email (optional) <input type="text" name="email" value=%(email)s></td><td id="error">%(error4)s</td></tr>

    </table>
    <br>
    <br>
    <br>
    <div class="submit"> <input type="submit"> </div>
    </div>
    </body>
    </html>
"""

class SignUpPage(webapp2.RequestHandler):
#define form
    def write_form(self,error1="",error2="",error3="",error4="", username="",password1="",password2="",email=""):
        self.response.out.write(form %{"error1":error1,"error2":error2,
                                        "error3":error3,"error4":error4,
                                        "username":username,"password1":password1,
                                        "password2":password2,"email":email})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        error1=error2=error3=error4=""
#see if username is valid
        username=valid_username(user_username)
        password=valid_password(user_password)
        email=valid_email(user_email)

        if not username:
            error1 = "That is not a valid username."

#see if passwords match and are valid
        if password:
            if user_password != user_verify:
                error3 = "Passwords do not match."
        else: 
            error2 = "That is not a valid password."

#see if email is valid
        if not(email) and len(user_email)>0:
            error4 = "That is not a valid email."

#if all four inputs are good, redirect to welcome page
        if error1 == error2 == error3 == error4 == "":
            self.redirect('/welcome?username=%s'%user_username)
        else:
            password1 = password2 = "" 
            self.write_form(error1, error2, error3, error4, user_username, password1, password2, user_email)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user_username = self.request.get('username')
        self.response.out.write("Welcome " + str(user_username) + "!")

app = webapp2.WSGIApplication([('/', SignUpPage),('/welcome', WelcomeHandler)],
                              debug=True)
