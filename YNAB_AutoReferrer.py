import datetime, os, praw, sqlite3, sys

database_path = os.path.expanduser("~") + '/world.db'

con = sqlite3.connect(database_path)
cur = con.cursor()

referral_link = 'https://ynab.com/referral/?ref=BV8h5Y76iGsZXXdl&utm_source=customer_referral'

try:
	qry = 'select client_id, client_secret, user_agent, username, password from reddit_bot_creds;'
	row = cur.execute(qry).fetchone()

	reddit = praw.Reddit(
		client_id=row[0]
		, client_secret=row[1]
		, user_agent=row[2]
		, username=row[3]
		, password=row[4]
	)
except:
	print('Error connecting to Reddit')
	sys.exit(1)

subreddit_ynab = reddit.subreddit('YNAB')

for submission in subreddit_ynab.search('Promo', sort='new'):
	check_qry = 'select key from reddit_posts where key = ?;'
	cur.execute(check_qry, (submission.id,))

	res = cur.fetchall()
	if len(res) == 0:
		reply_str = 'Here\'s a referral from Oregon, good luck with YNAB! {0}'
		submission.reply(reply_str.format(referral_link))
		
		log_qry = 'insert into reddit_posts(key, subreddit, first_seen, posted_ind, last_post_date) values (?,?,?,?,?)'
		now     = datetime.datetime.now()
		now_str = now.strftime('%Y-%m-%d %H:%M')

		cur.execute(log_qry, (submission.id, 'YNAB', now_str, 'Y', now_str,))
		con.commit()
