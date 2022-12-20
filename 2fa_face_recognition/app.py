from flask import Flask,redirect,url_for,render_template,request,Response,session,flash
import face_recognition
import cv2
import mysql.connector
import numpy as np
from PIL import Image
import io 
import base64
from cryptography.fernet import Fernet
import urllib.request as ur
import re

err=''
# camera=cv2.VideoCapture(0)
key=Fernet.generate_key()
f = Fernet(key)

app=Flask(__name__)

#key for session
app.secret_key = '1234'

#connection to sql and creating object
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="facerec" 
)
cursor = mydb.cursor()

#un='admin'
#pa='pass'
err=' '

@app.route('/')
def index():
    session.pop('login', None)
    session.pop('un', None)
    session.pop('name',None)
    session.pop('signedin',None)
    session.pop('funame', None)
    session.pop('fupass', None)
    session.pop('fnname',None)

    return render_template('index.html') 


@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method=='POST':
        fun=request.form['uname']
        print(type(fun))
        fpa=request.form['pwd']
        efun=f.encrypt(b'{fun}')
        print(efun)

        query='select uname,upass,name from user where uname=%s AND upass=%s'
        cursor.execute(query,(fun,fpa))
        account=cursor.fetchone()

        if account:
            session['login']=True
            #0 is for uname and 2 is for name in our db 
            session['un']=account[0]
            session['name']=account[2]
            return redirect(url_for('cam'))

        else:
            err='Invalid Credentials'
            flash(err)
            return render_template('index.html',error=err)
    
    return render_template('index.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        fun1=request.form['suname']
        fpa1=request.form['spwd']
        fna1=request.form['snname']

        # query='insert into user(uname,upass,name) values (%s,%s,%s)'
        # cursor.execute(query,(fun,fpa,fna))
        # mydb.commit()

        session['signedin']=True
        session['funame']=fun1
        session['fupass']=fpa1
        session['fnname']=fna1

        query='select uname from user where uname=%s'
        cursor.execute(query,(fun1,))
        account=cursor.fetchone()

        if account:
            session['login']=True
            #0 is for uname and 2 is for name in our db 
            return redirect(url_for('index'))
        else:
            return redirect(url_for('camreg'))

    elif request.method=='GET':
        print('sent')
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/camreg',methods=['POST','GET'])
def camreg():
    if 'signedin' in session:
        global status
        status=""

        if request.method=='POST':
            # image_b64 = request.values['imageBase64']
            # image_data = re.sub('^data:image/.+;base64,', '',image_b64)
            getdata=request.get_json(force=True)
            # print(type(getdata))
            # image_data = re.sub('^data:image/png.+;base64,', '', getdata['image'])
            image_data=getdata['image'].index(',')
            image_data=getdata['image'][image_data+1::]
            # print(image_data)
            im = Image.open(io.BytesIO(base64.b64decode(image_data))).tobytes()
            file = base64.b64encode(im)

            # print(im)
            # print(type(im))

            print(session['funame'],session['fupass'],session['fnname'])
            # im.show()
            # im=im.tobytes()
           
            runsql=False

            query1="insert into user values(%s,%s,%s,%s)"
            sd=(session['funame'],session['fupass'],session['fnname'],image_data)
            try:
                cursor.execute(query1,sd)
                mydb.commit()
                runsql=True
                # flash("Registerd successfully")


            except:
                runsql=False

            if runsql:
                status='Registerd successfully'

            else:
                session.pop('funame', None)
                session.pop('fupass', None)
                session.pop('fnname',None)
                session.pop('signedin',None)
                err='registration not successful'
                print(err)
                status='Registration Failed'
        flash(status)
        return render_template('camreg.html')

    else:
        return redirect(url_for('index'))
    
    
@app.route('/cam')
def cam():
    if 'login' in session:
        # if name1==session['name']:
        #     redirect(url_for('final')) 
        return render_template('cam.html')
        
    return redirect(url_for('index'))    

@app.route('/final')
def final():
    if request.method=='GET':
        return render_template('final.html')

@app.route('/vfeed')
def vfeed():
    if 'login' in session: 
        una=session['un']
        query=f"select pic1 from user where uname = '{una}'"
        cursor.execute(query)
        data = cursor.fetchall()
        print(type(data))

        # Himage = data[0][0]
        # print(type(Himage))
        # pic = Image.open(io.BytesIO(Himage))
        # print(pic)

        Himage = data[0][0]
        # print(Himage)
        # decoded= ur.urlopen(Himage)
        # print(decoded)

        binary_data = base64.b64decode(Himage)
        # print(binary_data)                                    
        pic = Image.open(io.BytesIO(binary_data))
        #print(pic)
        pic.show()

        # pix = np.array(pic) 
        # print(pix)
        imagedb = face_recognition.load_image_file(io.BytesIO(base64.b64decode(Himage)))
        face_encoding = face_recognition.face_encodings(imagedb)[0]
        known_face_encodings = [face_encoding]
        known_face_names = [session['name']]
        
        global camera
        camera=cv2.VideoCapture(0)
        return Response(generate_frames(known_face_encodings,known_face_names),mimetype='multipart/x-mixed-replace; boundary=frame')

    else:
        return redirect(url_for('index'))    

def generate_frames(known_face_encodings,known_face_names):
        while True:
                
            ## read the camera frame
            
            success,frame=camera.read()
            if not success:
                break
            else:
                model='hog'
                TOLERANCE=0.4

                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                # rgb_small_frame=frame
                face_locations = face_recognition.face_locations(rgb_small_frame,model=model)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding,TOLERANCE)
                    name='unknown'
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name=known_face_names[best_match_index]

                    face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()            
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('un', None)
    session.pop('name',None)
    session.pop('signedin',None)
    session.pop('funame', None)
    session.pop('fupass', None)
    session.pop('fnname',None)
    camera.release()
    # cursor.close()
    # mydb.close()

    return redirect(url_for('index'))
    
@app.route('/logoutr')
def logoutr():
    session.pop('login', None)
    session.pop('un', None)
    session.pop('name',None)
    session.pop('signedin',None)
    session.pop('funame', None)
    session.pop('fupass', None)
    session.pop('fnname',None)
    # camera.release()
    # cursor.close()
    # mydb.close()

    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)