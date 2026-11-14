#!/usr/bin/env bash
# Root-only, fail-closed backup of the Mainstream production host.
set -Eeuo pipefail
umask 077
export LC_ALL=C
[[ $EUID -eq 0 ]] || { echo 'Run as root' >&2; exit 1; }
for command in flock runuser pg_dump pg_dumpall pg_restore python3 tar gzip sha256sum; do
    command -v "$command" >/dev/null
done
exec 9>/run/lock/mainstream-backup.lock
flock -n 9 || { echo 'Another backup is running' >&2; exit 1; }
backup_root=/var/backups/mainstream
install -d -m 700 "$backup_root"
backup_dir=$(mktemp -d "$backup_root/$(date -u +%Y%m%dT%H%M%SZ)-XXXXXX")
trap 'echo "Backup FAILED (no VERIFIED marker): $backup_dir" >&2' ERR
mkdir -m 700 "$backup_dir/sqlite"

# PostgreSQL uses its own transaction-consistent snapshot; never copy PGDATA.
runuser -u postgres -- pg_dump --format=custom --dbname=streaming > "$backup_dir/streaming.dump"
test -s "$backup_dir/streaming.dump"
pg_restore --list "$backup_dir/streaming.dump" > "$backup_dir/streaming.contents"
grep -q 'TABLE DATA' "$backup_dir/streaming.contents"
runuser -u postgres -- pg_dumpall --globals-only > "$backup_dir/postgres-globals.sql"
test -s "$backup_dir/postgres-globals.sql"
grep -q 'PostgreSQL database cluster dump' "$backup_dir/postgres-globals.sql"

# SQLite online backup includes committed WAL contents. Check the destination.
python3 - "$backup_dir" <<'PY'
import pathlib
import sqlite3
import sys

destination = pathlib.Path(sys.argv[1]) / 'sqlite'
required = pathlib.Path('/opt/judges_bot_v2/bot_database.db')
if not required.is_file():
    raise SystemExit(f'Missing required database: {required}')
databases = [required]
for path in pathlib.Path('/var/lib/tshedule').rglob('*'):
    if path.is_file() and not path.is_symlink():
        with path.open('rb') as handle:
            if handle.read(16) == b'SQLite format 3\x00':
                databases.append(path)
for source in databases:
    target = destination / source.relative_to('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True, timeout=30) as src:
        with sqlite3.connect(target) as dst:
            src.backup(dst, pages=256, sleep=0.1)
            rows = dst.execute('PRAGMA integrity_check').fetchall()
            if rows != [('ok',)]:
                raise SystemExit(f'SQLite integrity check failed: {source}')
PY

# Every required source must exist. No ignored tar failures or missing paths.
sources=(
    opt/streaming/backend/uploads
    opt/streaming/backend/.env
    opt/judges_bot_v2/.env
    var/lib/tshedule
    var/www/html
    etc/nginx
    etc/systemd/system
    etc/ssh
    etc/letsencrypt
    etc/tinyproxy/cursorvpn.conf
    etc/netns/cursorvpn/resolv.conf
    etc/apparmor.d
    etc/apparmor.d/local/tinyproxy
    etc/fstab
    etc/passwd
    etc/shadow
    etc/group
    etc/gshadow
    usr/local/sbin
    root/cursor.conf
    root/.local/share/cursor-agent
    root/.local/bin/agent
    root/.local/bin/cursor-agent
    root/.config/cursor
    root/.cursor/cli-config.json
)
# Include deployment configs, additional uploads and service scripts if present.
for optional in opt/tshedule/.env opt/judges_bot_v2/uploads \
    opt/streaming/deploy opt/tshedule/deploy usr/local/bin etc/default \
    etc/cron.d etc/crontab etc/sudoers.d etc/subuid etc/subgid etc/wireguard; do
    if [[ -e /$optional ]]; then sources+=("$optional"); fi
done
for source in "${sources[@]}"; do test -e "/$source"; done
printf '%s\n' "${sources[@]}" > "$backup_dir/files.sources"
# A concurrently modified file causes a failed backup, never a success marker.
tar --acls --xattrs --numeric-owner -czf "$backup_dir/files.tar.gz" -C / "${sources[@]}"
gzip --test "$backup_dir/files.tar.gz"
tar -tzf "$backup_dir/files.tar.gz" > "$backup_dir/files.contents"
test -s "$backup_dir/files.contents"

(
    cd "$backup_dir"
    find . -type f ! -name SHA256SUMS ! -name VERIFIED -print0 \
        | sort -z | xargs -0 sha256sum > SHA256SUMS
    sha256sum --check --strict SHA256SUMS
    printf 'Verified UTC: %s\n' "$(date -u +%FT%TZ)" > VERIFIED
)
echo "Backup verified: $backup_dir"
