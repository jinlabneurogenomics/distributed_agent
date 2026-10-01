#!/usr/bin/env bash
set -euo pipefail

INSTANCE_NAME="${BIOKG_NEO4J_INSTANCE:-biokg-neo4j}"
LOCAL_IMAGE="${BIOKG_NEO4J_LOCAL_IMAGE:?BIOKG_NEO4J_LOCAL_IMAGE is required}"
IMAGE="${BIOKG_NEO4J_IMAGE:-$LOCAL_IMAGE}"
SOURCE_IMAGE="${BIOKG_NEO4J_SOURCE_IMAGE:-docker://neo4j:5.26.30-community}"
DATA_DIR="${BIOKG_NEO4J_DATA_DIR:?BIOKG_NEO4J_DATA_DIR is required}"
DUMP_FILE="${BIOKG_NEO4J_DUMP_FILE:?BIOKG_NEO4J_DUMP_FILE is required}"
LOG_DIR="${BIOKG_NEO4J_LOG_DIR:?BIOKG_NEO4J_LOG_DIR is required}"
OFFLINE_CONFIG="${BIOKG_NEO4J_OFFLINE_CONFIG:?BIOKG_NEO4J_OFFLINE_CONFIG is required}"
PLUGIN_DIR="${BIOKG_NEO4J_PLUGIN_DIR:?BIOKG_NEO4J_PLUGIN_DIR is required}"
HTTP_PORT="${BIOKG_NEO4J_HTTP_PORT:-7474}"
BOLT_PORT="${BIOKG_NEO4J_BOLT_PORT:-7687}"
PASSWORD="${BIOKG_NEO4J_PASSWORD:-biokgpassword}"
STOP_TIMEOUT="${BIOKG_NEO4J_STOP_TIMEOUT:-120}"

BIOKG_APPTAINER_RUNTIME_HOME="${BIOKG_APPTAINER_HOME:-/tmp/biokg-apptainer-home}"
export HOME="$BIOKG_APPTAINER_RUNTIME_HOME"
export APPTAINER_CACHEDIR="${APPTAINER_CACHEDIR:-/tmp/biokg-apptainer-cache}"
export APPTAINER_TMPDIR="${APPTAINER_TMPDIR:-/tmp/biokg-apptainer-tmp}"

prepare_transient_dirs() {
  mkdir -p \
    "$BIOKG_APPTAINER_RUNTIME_HOME" \
    "$APPTAINER_CACHEDIR" \
    "$APPTAINER_TMPDIR"
}

prepare_runtime_dirs() {
  prepare_transient_dirs
  mkdir -p \
    "$DATA_DIR" \
    "$LOG_DIR" \
    "$(dirname "$LOCAL_IMAGE")"
  if [[ ! -d "$PLUGIN_DIR" ]]; then
    echo "BioKG Neo4j plugin directory is missing: $PLUGIN_DIR" >&2
    exit 1
  fi
}

ensure_image() {
  if [[ ! -e "$IMAGE" && "$IMAGE" == "$LOCAL_IMAGE" ]]; then
    echo "Local Neo4j SIF not found at $LOCAL_IMAGE; pulling $SOURCE_IMAGE."
    apptainer pull --force "$LOCAL_IMAGE" "$SOURCE_IMAGE"
  fi
  if [[ ! -f "$IMAGE" ]]; then
    echo "BioKG Neo4j image is missing: $IMAGE" >&2
    exit 1
  fi
}

http_ready() {
  curl -fsS --max-time 2 "http://127.0.0.1:$HTTP_PORT" >/dev/null 2>&1
}

instance_pids() {
  ps -o pid=,cmd= -u "$USER" \
    | awk -v name="[$INSTANCE_NAME]" \
      '$0 ~ /^[[:space:]]*[0-9]+[[:space:]]+Apptainer instance:/ && index($0, name) {print $1}'
}

instance_pid() {
  apptainer instance list "$INSTANCE_NAME" \
    | awk -v name="$INSTANCE_NAME" '$1 == name {print $2; exit}'
}

expected_data_mount_root() {
  local mount_target fs_root relative
  mount_target="$(findmnt -n -o TARGET -T "$DATA_DIR")"
  fs_root="$(findmnt -n -o FSROOT -T "$DATA_DIR")"
  relative="${DATA_DIR#"$mount_target"}"
  if [[ "$fs_root" == "/" ]]; then
    printf '/%s\n' "${relative#/}"
  else
    printf '%s/%s\n' "${fs_root%/}" "${relative#/}"
  fi
}

assert_data_bind() {
  local pid="$1" actual_root expected_root
  actual_root="$(awk '$5 == "/data" {print $4; exit}' "/proc/$pid/mountinfo" 2>/dev/null || true)"
  expected_root="$(expected_data_mount_root)"
  if [[ "$actual_root" != "$expected_root" ]]; then
    echo "Neo4j instance '$INSTANCE_NAME' does not use the release data directory." >&2
    echo "Expected /data source: $expected_root" >&2
    echo "Actual /data source:   ${actual_root:-<unavailable>}" >&2
    return 1
  fi
}

print_status() {
  apptainer instance list --logs "$INSTANCE_NAME" || true
  if http_ready; then
    echo "Neo4j HTTP is reachable at http://127.0.0.1:$HTTP_PORT/"
  else
    echo "Neo4j HTTP is not reachable at http://127.0.0.1:$HTTP_PORT/"
  fi
  local pids
  pids="$(instance_pids || true)"
  if [[ -n "$pids" ]]; then
    echo "Matching Apptainer instance process groups:"
    ps -o pid,ppid,pgid,sid,stat,cmd -p "$(echo "$pids" | paste -sd, -)" || true
  fi
}

stop_process_groups() {
  local pids="$1"
  [[ -n "$pids" ]] || return 0
  while IFS= read -r pid; do
    [[ -n "$pid" ]] || continue
    kill -TERM "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
  done <<< "$pids"
  sleep 2
  while IFS= read -r pid; do
    [[ -n "$pid" ]] || continue
    if kill -0 "$pid" 2>/dev/null; then
      kill -KILL "-$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null || true
    fi
  done <<< "$pids"
}

case "${1:-}" in
  pull)
    prepare_runtime_dirs
    apptainer pull --force "$LOCAL_IMAGE" "$SOURCE_IMAGE"
    ;;
  restore)
    prepare_runtime_dirs
    ensure_image
    if [[ ! -f "$DUMP_FILE" ]]; then
      echo "BioKG Neo4j dump is missing: $DUMP_FILE" >&2
      echo "Run git lfs pull for the release data/graph artifact." >&2
      exit 1
    fi
    if [[ ! -f "$OFFLINE_CONFIG" ]]; then
      echo "BioKG Neo4j offline config is missing: $OFFLINE_CONFIG" >&2
      exit 1
    fi
    if http_ready \
      || [[ -n "$(instance_pid || true)" ]] \
      || [[ -n "$(instance_pids || true)" ]]; then
      echo "Stop the '$INSTANCE_NAME' instance before restoring the BioKG dump." >&2
      exit 1
    fi
    if [[ "$(basename "$DUMP_FILE")" != "neo4j.dump" ]]; then
      echo "BioKG dump must be named neo4j.dump: $DUMP_FILE" >&2
      exit 1
    fi
    apptainer exec \
      --cleanenv \
      --bind "$DATA_DIR:/data" \
      --bind "$(dirname "$DUMP_FILE"):/backups:ro" \
      --bind "$OFFLINE_CONFIG:/etc/biokg-neo4j-offline.conf:ro" \
      "$IMAGE" \
      sh -c 'exec /var/lib/neo4j/bin/neo4j-admin database load neo4j \
        --additional-config=/etc/biokg-neo4j-offline.conf \
        --from-path=/backups --overwrite-destination=true'
    echo "Restored BioKG Neo4j dump from $DUMP_FILE"
    ;;
  up)
    prepare_runtime_dirs
    ensure_image
    if http_ready; then
      running_pid="$(instance_pid || true)"
      if [[ -z "$running_pid" ]]; then
        echo "Neo4j is reachable on port $HTTP_PORT, but it is not the registered '$INSTANCE_NAME' instance." >&2
        echo "Stop the conflicting service before starting the release runtime." >&2
        exit 1
      fi
      assert_data_bind "$running_pid"
      echo "Neo4j is already reachable at http://127.0.0.1:$HTTP_PORT/"
      print_status
      exit 0
    fi
    stale_pids="$(instance_pids || true)"
    if [[ -n "$stale_pids" ]]; then
      echo "Stopping stale Apptainer process groups for '$INSTANCE_NAME'."
      stop_process_groups "$stale_pids"
    fi
    if apptainer instance list "$INSTANCE_NAME" | awk 'NR > 1 {print $1}' | grep -qx "$INSTANCE_NAME"; then
      echo "Apptainer instance '$INSTANCE_NAME' is already running."
      exit 0
    fi
    apptainer instance run \
      --cleanenv \
      --writable-tmpfs \
      --bind "$DATA_DIR:/data" \
      --bind "$LOG_DIR:/logs" \
      --bind "$PLUGIN_DIR:/var/lib/neo4j/plugins:ro" \
      --env "NEO4J_AUTH=neo4j/$PASSWORD" \
      --env "NEO4J_dbms_security_procedures_unrestricted=apoc.*" \
      --env "NEO4J_dbms_security_procedures_allowlist=apoc.*" \
      --env "NEO4J_server_default__listen__address=0.0.0.0" \
      --env "NEO4J_server_http_listen__address=0.0.0.0:$HTTP_PORT" \
      --env "NEO4J_server_bolt_listen__address=0.0.0.0:$BOLT_PORT" \
      --env "NEO4J_server_memory_heap_initial__size=512m" \
      --env "NEO4J_server_memory_heap_max__size=2G" \
      "$IMAGE" "$INSTANCE_NAME"
    running_pid="$(instance_pid || true)"
    if [[ -z "$running_pid" ]]; then
      echo "Apptainer started without registering instance '$INSTANCE_NAME'." >&2
      exit 1
    fi
    if ! assert_data_bind "$running_pid"; then
      apptainer instance stop --timeout "$STOP_TIMEOUT" "$INSTANCE_NAME" >/dev/null 2>&1 || true
      exit 1
    fi
    for _ in $(seq 1 30); do
      if http_ready; then
        print_status
        exit 0
      fi
      sleep 2
    done
    echo "Neo4j did not become reachable on http://127.0.0.1:$HTTP_PORT/ within 60 seconds." >&2
    print_status >&2
    exit 1
    ;;
  down)
    prepare_transient_dirs
    # Neo4j can need slightly more than Apptainer's ten-second default to
    # checkpoint a large graph. A forced stop leaves active transaction logs
    # and prevents an immediate offline dump.
    apptainer instance stop --timeout "$STOP_TIMEOUT" "$INSTANCE_NAME" >/dev/null 2>&1 || true
    stop_process_groups "$(instance_pids || true)"
    ;;
  list)
    prepare_transient_dirs
    print_status
    ;;
  logs)
    prepare_transient_dirs
    if compgen -G "$HOME/.apptainer/instances/logs/*/$INSTANCE_NAME.err" > /dev/null; then
      tail -n "${2:-120}" "$HOME"/.apptainer/instances/logs/*/"$INSTANCE_NAME".err
    fi
    if compgen -G "$HOME/.apptainer/instances/logs/*/$INSTANCE_NAME.out" > /dev/null; then
      tail -n "${2:-120}" "$HOME"/.apptainer/instances/logs/*/"$INSTANCE_NAME".out
    fi
    if [[ -d "$LOG_DIR" ]]; then
      find "$LOG_DIR" -maxdepth 1 -type f -print -exec tail -n "${2:-120}" {} \;
    fi
    ;;
  *)
    cat >&2 <<EOF
Usage: $0 {pull|restore|up|down|list|logs [lines]}

Paths are supplied by python -m distributed_agents.corpus.launch biokg.host and may be overridden
with BIOKG_WORK_ROOT or the BIOKG_NEO4J_* variables.
EOF
    exit 2
    ;;
esac
