# Restore

Geonode have a routine backup stored. Backup volumes were for:

- Postgis data
- Media data


## Postgis data

Postgis history data were maintained by `dbbackup` service. It was stored
on `postgis-history-data` and maintained in `/backups` folder.

To restore a data snapshot, go into `dbbackup` service and restore the snapshot
the chosen snapshot

Input:

```
[backup-snapshot]: the name/path of the backup snapshot to restore
```

Restoring:

Then, mount your pg backup snapshot volume to `postgis` service. For example, using
rancher, add another volume in `postgis` with the entry `postgis-history-data:/db_backup`.
After it is done, go into the new `postgis` shell:

```
su - postgres -c "dropdb gis"
su - postgres -c "createdb -O docker -T template_postgis gis"
pg_restore [backup-snapshot] | su - postgres -c "psql -d gis"
```

## Media data

Media history data were maintained by `mediabackup` service. It was stored
on `media-history-data` and maintained in `/backups` folder.
The target folder to backup is on `django-media-data` in `/media_backup`.

To restore a data snapshot, go into `mediabackup` service's shell.

Input:

```
[backup-snapshot]: the name of the backup snapshot to restore
```

Restoring:

Make sure you understand, that this will delete target folder content, so save
any data before you execute this command.

```
/restore.sh [backup-snapshot]
```

or manually (in case using old version of `kartoza/sftp-backup`)

```
# Clean up Target folder
rm -rf ${TARGET_FOLDER}/*
tar -xf [backup-snapshot] -C ${TARGET_FOLDER}
```

This will delete entire target folder and populate it with backup data.

In case the extracted directory structure is different, please manually adjust
the structure.

## QGIS Server Media data

Media history data were maintained by `qgisservermediabackup` service. It was stored
on `qgis-server-qgis-layer-history-data` and maintained in `/backups` folder.
The target folder to backup is on `qgis-server-qgis-layer-data` in `/media_backup`.

To restore a data snapshot, go into `qgisservermediabackup` service's shell.

Input:

```
[backup-snapshot]: the name of the backup snapshot to restore
```

Restoring:

Make sure you understand, that this will delete target folder content, so save
any data before you execute this command.

```
/restore.sh [backup-snapshot]
```

or manually (in case using old version of `kartoza/sftp-backup`)

```
# Clean up Target folder
rm -rf ${TARGET_FOLDER}/*
tar -xf [backup-snapshot] -C ${TARGET_FOLDER}
```

This will delete entire target folder and populate it with backup data.

In case the extracted directory structure is different, please manually adjust
the structure.


