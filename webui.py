#!/usr/bin/env python
# -*- coding:utf-8 -*- 

# Require: flask jinja2 Werkzeug itsdangerous
from flask import Flask, url_for
app = Flask(__name__)

### Preset ###
# Info that may be included in the header of webpage.
LANGUAGE_PREFIX = "en"
DEBUG_MODE = False

# HOW TO SECURE THE LOCAL ENVIRONMENT USING COCOA/SYSTEM-LEVEL TOOL

class Page:
    title=""
    content=""
    def set(self, title, content):
        self.title=title
        self.content=content
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

print url_for('post', post_id=2)
print url_for('static', filename='page.html')

# template


def hello(name=None):
    return render_template('hello.html', name=name)








if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)


### Simple Function ###
# that directly make a new class inside.



