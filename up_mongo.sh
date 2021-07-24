#!/bin/bash
docker exec -it mongo bash -c 'echo "use ugcDb" | mongo';

docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.movie_ratingCollection\")" | mongo -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD"';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.movie_reviewCollection\")" | mongo -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD"';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.movie_bookmarkCollection\")" | mongo -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD"';

