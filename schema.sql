create table reddit_posts (
  key text unique
  , subreddit text
  , first_seen date
  , posted_ind text
  , last_post_date date
);

create table reddit_bot_creds (
  client_id text unique
  , client_secret text
  , user_agent text unique
  , username text
  , password text
);