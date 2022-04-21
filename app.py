from flask import Flask,render_template, redirect, url_for , request, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os
import cv2

from EngagmentServer import api
from camera import VideoCamera
import numpy as np


from model import db, User, Courses, StudentsInCourses, Videosincourses,studentAnalysis

UPLOAD_FOLDER = 'C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/static/videos/'
# data base connections
app = Flask(__name__,static_folder='static')
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/education'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#db = SQLAlchemy()
#db = SQLAlchemy(app)
db.init_app(app= app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# def get_id(self):
#     """Return the email address to satisfy Flask-Login's requirements."""
#     return self.username


#from app import login_manager

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

with app.app_context():
    db.create_all()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    number = StringField('number', validators=[InputRequired()])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadvid', methods=['GET', 'POST'])
def uploadvid():
    coursename = session['courseName']
    vidname = request.form['vidname']
    # check if the post request has the file part
    file = request.files['file']
    filename = secure_filename(vidname)
    # if user does not select file, browser also
    # submit an empty part without filename
    #if file and allowed_file(file.filename):
    coursepath = app.config['UPLOAD_FOLDER']+'/'+coursename
    if not(os.path.isdir(coursepath)):
        os.mkdir(coursepath)

    file.save(os.path.join(coursepath, filename+'.mp4'))
    data = Videosincourses(coursename= coursename,vidName=vidname)
    db.session.add(data)
    db.session.commit()


    return redirect('/yourcourses')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inshomepage')
def inshomepage():
    return render_template('InstructorHomepage.html')

@app.route('/stuhomepage')
def stuhomepage():
    return render_template('StudentHomepage.html')



@app.route('/joincouse', methods=['GET', 'POST'])
def joincouse():
    username = session['username']
    coursename = request.form['courname']
    data = StudentsInCourses(coursename= coursename,Susername=username)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('Scourses'))
    #return render_template('Scourses.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                session['username'] = form.username.data
                if(user.type == 1):
                    return render_template('InstructorHomepage.html', name=session['username'])
                else:
                    return render_template('StudentHomepage.html', name=session['username'])
                #return redirect(url_for('dashboard'))
            else:

                return render_template('login.html', form=form)

        else:
            return render_template('login.html', form=form)
        #global name


        return render_template('InstructorHomepage.html', name=session['username'])

    return render_template('login.html', form=form)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        if form.number.data == "1":
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, type=form.number.data)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = form.username.data
            return Ihome(form)
            #return render_template('InstructorHomepage.html', form=form)
        else:
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, type=form.number.data)
            db.session.add(new_user)
            db.session.commit()
            return Shome(form)
            #return render_template('StudentHomepage.html', form=form)


    return render_template('register.html', form=form)

@app.route('/Shome', methods=['GET', 'POST'])
def Shome(form):
    return render_template('StudentHomepage.html', form=form)

@app.route('/Ihome', methods=['GET', 'POST'])
def Ihome(form):
    return render_template('InstructorHomepage.html', form=form)



@app.route('/profile')
@login_required
def dashboard():
    return render_template('InstructorHomepage.html', name=session['username'])





@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('index.html')



@app.route('/courses', methods=['GET', 'POST'])
def courses():
    data = []
    try:
        data = Courses.query.all()

    except:
        print ("I am unable to connect to the database")

    return render_template('courses.html',data = data)


# return your courses analysis
@app.route('/yourcoursesanalysis', methods=['GET', 'POST'])
def yourcoursesanalysis():
    username = session['username']
    try:
        data = Courses.query.filter_by(Iusername = username).all()

    except:
        print ("I am unable to connect to the database")

    return render_template('yourcoursesAnalysis.html',data = data)

# return videos in courses for analysis
@app.route('/Iyourcoursevidsanalysis', methods=['GET', 'POST'])
def Iyourcoursevidsanalysis():
    vidnames = []

    session['courseName'] = request.form['courname2']
    coursename = request.form['courname2']

    data = Videosincourses.query.filter_by(coursename = coursename).all()
    return render_template('yourcoursevidsanalysis.html',data = data)

# return video analysis
@app.route('/videoanalysis', methods=['GET', 'POST'])
def videoanalysis():
    vidnames = []

    courname = session['courseName']
    vidname = request.form['vidname']


    data = studentAnalysis.query.filter_by(courseName = courname,vidname=vidname).all()

    toteng =0
    totdis = 0
    #return str(d)
    for x in data:
        if x.engState == 1:
            toteng +=1
        else:
            totdis +=1

    total = totdis+toteng
    engpercent = toteng/total
    dispercent = totdis/total

    #data = {'diseng': totdis}
   # data['eng']=toteng
    data = {'Task': 'total disengaged students on this video','disengaged': totdis,'engaged': toteng}
    #data['task2']='total disengaged students on this video'
    #data['engaged']=engpercent
    #return str(courname)
    return render_template('analysisResult.html',data = data)


@app.route('/Scourses', methods=['GET', 'POST'])
def Scourses():
    data = []
    try:
        data = Courses.query.all()

    except:
        print ("I am unable to connect to the database")

    return render_template('Scourses.html',data = data)

@app.route('/Sincourses', methods=['GET', 'POST'])
def Sincourses():

    username = session['username']
    data = []
    try:
        data = StudentsInCourses.query.filter_by(Susername = username).all()

    except:
        print ("I am unable to connect to the database")

    return render_template('Sincourses.html',data = data)

@app.route('/yourcourses', methods=['GET', 'POST'])
def yourcourses():
    data = []
    username = session['username']
    try:
        data = Courses.query.filter_by(Iusername = username).all()

    except:
        print ("I am unable to connect to the database")

    return render_template('yourcourses.html',data = data)

data=[]
state = 1
frames=[]

def preprocessframes():
    frames=[]
    framefolder = 'H:/GP/GP_PROJECT/faces/'
    for frame in os.listdir(framefolder):
        framepath = framefolder+frame
        frame = cv2.imread(framepath,cv2.IMREAD_GRAYSCALE)
        frames.append(frame)
    frames = np.array(frames)
    frames = frames.reshape(frames.shape[0],48,48,1)
    return str(frames.shape)

@app.route('/finish', methods=['GET', 'POST'])
def finish():

    global state
    state = 0

    result = api('C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/faces')

    coursename = session['courseName']
    vidname = session['vidName']
    username = session['username']

    analysis = studentAnalysis(vidname=vidname, courseName=coursename, Susername=username, engState=result)
    db.session.add(analysis)
    db.session.commit()
    state = 1
    return Sincourses()


@app.route('/record', methods=['GET', 'POST'])
def record():
    global frames
    global state
    camera = VideoCamera()
    while state == 1:
        camera.get_frame()
    camera.end()




# return video path for specific course
@app.route('/yourcoursevids', methods=['GET', 'POST'])
def yourcoursevids():
    coursefolder = ''
    vidpaths = ''

    courfolder = "C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/static/videos/"
    stpath = "videos/"

    coursename = session['courseName']
    vidname = request.form['vidname']
    session['vidName'] = vidname

    for folder in os.listdir(courfolder):
        if (folder == coursename):
            coursefolder = courfolder + folder
            stfolder = stpath + folder
            for video in os.listdir(coursefolder):
                if(video == vidname+'.mp4'):
                    video_path = coursefolder +'/'+ video
                    stvideo = stfolder + '/' + video
                    vidpaths=stvideo
    #gen(VideoCamera())
    #return str(stvideo)
    return render_template('showVideo.html',data=stvideo)


# return videos names in specific course
@app.route('/yourcoursevidsnames', methods=['GET', 'POST'])
def yourcoursevidsnames():
    vidnames = []

    session['courseName'] = request.form['coursename']
    coursename = request.form['coursename']

    data = Videosincourses.query.filter_by(coursename = coursename).all()

    return render_template('showVideosnames.html',data = data)




@app.route('/Iyourcoursevids', methods=['GET', 'POST'])
def Iyourcoursevids():


    coursename = request.form['courname2']
    session['courseName'] = coursename
    data = Videosincourses.query.filter_by(coursename = coursename).all()

    return render_template('yourcoursevids.html',data = data)


@app.route('/addcourse', methods=['GET', 'POST'])
def addcourse():

    return render_template('addcourse.html')


@app.route('/addcourse2', methods=['GET', 'POST'])
def addcourse2():
    error=None;
    username = session['username']
    coursename = request.form['couname']
    coursedesc = request.form['coudes']
    coursetype = request.form['coutype']
    samecourname = Courses.query.filter_by(CourseName =coursename).all()

    if( len(samecourname) == 0):
        try:

            data = Courses(CourseName= coursename,coursecategory=coursetype,coursedescription=coursedesc,Iusername=username)
            db.session.add(data)
            db.session.commit()
        except:
            print ("I am unable to connect to the database")

    else:
        error = "the course name allready exists"
        return render_template('addcourse.html', error=error)


    return redirect('/courses')



@app.route('/profile', methods=['GET', 'POST'])
def cambtn():
    #name = form.username.data
    #print(UserMixin.current_user.username)
    filename = 'video_'+session['username']+'.avi'
    #print(session['username'])
    #filename = 'video.avi'
    #print(filename)
    frames_per_second = 24.0
    res = '720p'

    # Set resolution for the video capture
    # Function adapted from https://kirr.co/0l6qmh
    def change_res(cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    # Standard Video Dimensions Sizes
    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }

    # grab resolution dimensions and set video capture to it.
    def get_dims(cap, res='1080p'):
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width, height = STD_DIMENSIONS[res]
        ## change the current caputre device
        ## to the resulting resolution
        change_res(cap, width, height)
        return width, height

    # Video Encoding, might require additional installs
    # Types of Codes: http://www.fourcc.org/codecs.php
    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))



    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return render_template('profile_test.html')

    cap.release()
    out.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    app.run(debug=True)

