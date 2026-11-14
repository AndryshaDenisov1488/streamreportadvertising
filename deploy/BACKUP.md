# Mainstream backup and restore

Production: `root@31.128.41.221:2222`. Install `mainstream-backup.sh` as
`/usr/local/sbin/mainstream-backup` (root:root, 0700), and the service/timer in
`/etc/systemd/system/`. Disable obsolete `judges-backup.timer` and any previous
backup timer before enabling this single `mainstream-backup.timer`; run
`systemctl daemon-reload`, start the service once and check its result before
enabling the timer with `systemctl enable --now mainstream-backup.timer`.

Daily at 03:30 Moscow, with a catch-up after downtime. Output is under
`/var/backups/mainstream` (root-only, 0700). No automatic retention deletion.
The archives contain credentials and account hashes: keep them outside Git and
copy completed backups to protected independent storage. Inspect failed units
and disk space regularly.

Required state includes Cursor agent runtime/config, `/root/cursor.conf`,
Cursor VPN tinyproxy/network-namespace configuration and AppArmor profiles.
Root SSH access is covered by `/root/.ssh/authorized_keys`; root private SSH keys
are not included. Review authorized keys before restoring access on another host.
`/etc/wireguard` is included when present. Missing required paths fail the backup,
so install the actual migrated runtime before the first run. PostgreSQL global
roles and grants are saved in protected `postgres-globals.sql`; it may contain
password hashes and must receive the same protection as `.env` and shadow files.

Only a directory with `VERIFIED` and a passing `sha256sum --check --strict
SHA256SUMS` is a completed backup. The checks cover PostgreSQL archive readability,
SQLite integrity, gzip/tar readability and file checksums. PostgreSQL restore
testing still requires an isolated database; a readable dump alone does not
prove a successful restore. Concurrent changes during tar fail the backup.
PostgreSQL, SQLite and files are individually captured, not one cross-service
transaction. Stop relevant writers for a coordinated migration snapshot.

## Restore

1. Select a completed backup, verify its manifest, and first restore into an
   isolated directory/database. Preserve a fresh verified backup of current
   state. Restoring over production needs an explicit decision because it can
   remove newer records. Do not automatically restore whole `/etc` or account
   files across hosts.
2. Inspect `streaming.contents` and `files.contents`. Restore PostgreSQL into an
   empty test database with `pg_restore --exit-on-error --no-owner --no-privileges
   --dbname=<test-db> streaming.dump`; verify tables and key counts. For a planned
   production restore, stop `streaming-backend` and use the established database
   owner/roles; never use `--clean` against a live database.
   Inspect `postgres-globals.sql` and restore only the required roles/grants into
   the isolated environment before database restore. Do not blindly replay global
   roles over another live cluster or replace existing credentials.
3. Extract `files.tar.gz` into a separate root-owned staging directory using
   `tar --acls --xattrs --numeric-owner -xzf ... -C <staging>`. Review configs,
   permissions and SFTP bind mount before copying selected paths into place.
   Never overwrite newer static results without comparison.
4. Stop judges/API writers before restoring judges SQLite. Use the checked copy
   in `sqlite/opt/judges_bot_v2/bot_database.db`, not a raw database from tar.
   For tshedule SQLite, checked copies under `sqlite/var/lib/tshedule/` take
   precedence over raw files in the archive. Preserve existing DB/WAL/SHM files
   together in recovery storage before replacement; check integrity and owner.
5. Start services, check journals, login/registration, uploads/results and HTTP
   health. Keep the pre-restore backup until the recovery is accepted.
