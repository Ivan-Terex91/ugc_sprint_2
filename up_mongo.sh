#!/bin/bash

# Настроим серверы конфигурации
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongo';
sleep 5;
# Собираем набор реплик первого шарда
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongo';
sleep 5;
# Добавляем шард в маршрутизатор
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongo';
sleep 5;
# Делаем всё тоже самое для второго шарда
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongo';
sleep 5;
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongo';
sleep 5;
# Создаем БД
docker exec -it mongors1n1 bash -c 'echo "use ugcDb" | mongo';
sleep 5;
# Включаем шардирование
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugcDb\")" | mongo';
sleep 5;
# Создаем коллекцию
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcDb.movie_ratingCollection\")" | mongo';
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcDb.movie_reviewCollection\")" | mongo';
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcDb.movie_bookmarkCollection\")" | mongo';
sleep 5;
# Добавляем шардирование по полю movie_id
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcDb.movie_ratingCollection\", {\"movie_id\": \"hashed\"})" | mongo';
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcDb.movie_reviewCollection\", {\"movie_id\": \"hashed\"})" | mongo';
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcDb.movie_bookmarkCollection\", {\"movie_id\": \"hashed\"})" | mongo';
echo 'MongoDB ready to work';