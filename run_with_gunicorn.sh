echo "starting the astrology site with gunicorn"
gunicorn --bind 0.0.0.0:8080 getsign:za --workers=4 --access-logfile astro.log
