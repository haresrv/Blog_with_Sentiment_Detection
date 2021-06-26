docker build -t app .
docker tag app:latest registry.heroku.com/senti-talk/web
docker push registry.heroku.com/senti-talk/web
heroku container:release web --app senti-talk