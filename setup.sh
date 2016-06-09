git add .
git reset setup.sh
git commit -m "Attempt"
git push heroku master
heroku ps:scale web=1
