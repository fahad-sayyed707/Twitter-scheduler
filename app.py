from flask import Flask, render_template,request, redirect 
import gspread
from datetime import datetime, timedelta
app = Flask(__name__)

gc=gspread.service_account(filename='new_credentials.json')

sh=gc.open_by_key('1rXe2atb2KcYLx-iCji82ehha6Sq_xLwKx35ppQqur8I')
worksheet=sh.sheet1

class Tweet:
    def __init__(self,message,time,done,row_idx):
        self.message=message
        self.time=time
        self.done=done
        self.row_idx=row_idx
        
def get_date_time(date_time_str):
    date_time_obj = None
    error_code= None
    try:
        date_time_obj = datetime.strptime(date_time_str,'%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        error_code= f'Error! {e}'
        
    if date_time_obj is not None:
        now_time_cet = datetime.utcnow()  +  timedelta (hours=2)
        if not date_time_obj > now_time_cet:
            error_code = "error! time must be in the future"
            
    return date_time_obj, error_code
        
    

@app.route('/')
def tweet_list():
    tweet_records = worksheet.get_all_records()
    tweets = []
    for idx, tweet in enumerate(tweet_records, start=2):
        tweet = Tweet(**tweet, row_idx=idx)
        tweets.append(tweet)
    
    tweets.reverse()    
    n_open_tweets=sum(1 for tweet in tweets if not tweet.done)    
    return render_template('base.html',tweets=tweets, n_open_tweets=n_open_tweets)


@app.route('/tweet',methods=['POST'])
def add_tweet():
    message = request.form['message']
    if not message:
        return "error! no message"
    time = request.form['time']
    if not time:
        return "error! no time"
    pw= request.form['pw']
    if not pw or pw != "12345":
        return "error! wrong password"
    
    if len(message)>280:
        return "error! message too long"
    
    date_time_obj, error_code = get_date_time(time)
    if error_code is not None:
        return error_code
    
    tweet = [str(date_time_obj), message, 0]
    worksheet.append_row(tweet)
    return redirect('/')

@app.route('/delete/<int:row_idx>')
def delete_tweet(row_idx):
    worksheet.delete_rows(row_idx)
    return redirect('/')
    
    
    
if __name__=="__main__":
    app.run(debug=True)