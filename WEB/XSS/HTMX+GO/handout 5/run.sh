#!/bin/env sh
cat /dev/urandom | head | sha1sum | cut -d " " -f 1 > /app/jwt.secret

export JWT_SECRET_KEY=notsosecurekey
export ADMIN_FLAG=CSCTF{flag1} 
export POST_FLAG=CSCTF{flag2} 
export SUPERADMIN_FLAG=CSCTF{flag3} 
export REV_FLAG=CSCTF{flag4}
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=mysecretpassword
export POSTGRES_DB=devdb

uuid=$(cat /proc/sys/kernel/random/uuid)
user=$(cat /dev/urandom | head | md5sum | cut -d " " -f 1)
cat << EOF >> /docker-entrypoint-initdb.d/init.sql
	INSERT INTO users (username, password, role) VALUES ('superadmin', 'superadmin', 'superadmin');
    INSERT INTO posts (postid, username, title, data) VALUES ('$uuid', '$user', 'Welcome to the CTF!', '$ADMIN_FLAG');
EOF

docker-ensure-initdb.sh & 
GIN_MODE=release /app/chall & sleep 5
su postgres -c "postgres -D /var/lib/postgresql/data" &

nginx -g 'daemon off;' 