from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from random import randint
import time
import getVids
app = Flask(__name__)

vids=[]
@app.route('/youtube')
def homeForYoutube():
	return render_template("you/index.html")
@app.route('/youtube/topic')
def topicHome():
	return render_template('you/indexTopic.html')
@app.route('/youtube/youtuber')
def youtuber():
	return render_template("you/indexYou.html")
@app.route('/youtube/videoUser/',  methods=['POST'])
def getUser(quizType = None, name = None, vids=[],message = None,length=None):
	quizType=request.form['quizType']
	vids=[]
	name=request.form['name']
	vids = getVids.getVidsFromUser(name)
	if int(quizType)>len(vids):
		message = "Not Enough Videos Found for Quiz try another topic"
		return render_template("you/makeSure.html",quizType=quizType,message=message)
	vids = vids[0:int(quizType)]
	length=str(len(vids))
	return render_template("you/test.html",quizType=quizType,vids=vids,length=length)
@app.route('/youtube/video/',  methods=['POST'])
def quizStart(quizType = None, topic = None, vids=[],message = None,length=None):
	quizType=request.form['quizType']
	vids=[]
	
	topic=request.form['topic']
	vids = getVids.getVideoSearch(topic)
	if int(quizType)>len(vids):
		message = "Not Enough Videos Found for Quiz try another topic"
		return render_template("you/makeSure.html",quizType=quizType,topic=topic,message=message)
	vids = vids[0:int(quizType)]
	length=str(len(vids))
	return render_template("you/test.html",quizType=quizType,topic=topic,vids=vids,length=length)
@app.route('/youtube/videoQuiz/',  methods=['POST'])
def grade(answers=[],length=None, vids=[],points=[],sumA=0,videos=[],total=0):
	try:
		vids=[]
		length = request.form['length']
		total=0
		sumA=0
		total = int(length)*10
		answers=[]
		points=[]
		for i in range(0,int(length)):
			answers.append(request.form['A'+str(i)])
			vids.append(request.form['V'+str(i)])
		for i in range(0,len(vids)):
			points.append(getVids.GradeYouQuiz(answers[i],vids[i]))
		for item in points:
			sumA = sumA + item
		video=[]
		for video in vids:
			videos.append(getVids.crawlTitle("https://www.youtube.com/watch?v="+str(video)))

	except Exception as e: print(e)
	return render_template("you/grade.html",answers=answers,videos=videos,points=points,sumA=sumA,total=total,vids=vids)








if __name__ == '__main__':
    app.run()

