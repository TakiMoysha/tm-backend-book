usermod -o -u "$UID" worker
groupmod -o -g "$GID" worker

echo 'worker: $(id -u worker/ - $(id -g worker)'

chown -R worker:worker /data
su worker -c "python -m app_protocols -H 0.0.0.0 -c /data/data.json "

if [ "$DEBUG" = "true" ]; then python; fi
