#!/usr/bin/env bash
set -euo pipefail

BIOKG_HOST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIOKG_PROJECTION_ROOT="$(cd "$BIOKG_HOST_DIR/.." && pwd)"
BIOKG_WORK_ROOT="${BIOKG_WORK_ROOT:-$BIOKG_PROJECTION_ROOT/_work}"
BIOKG_NEO4J_WORK_ROOT="$BIOKG_WORK_ROOT/neo4j"

NEO4J_VERSION="${BIOKG_NEO4J_VERSION:-5.26.27}"
RUNTIME_ROOT="${BIOKG_NEO4J_NATIVE_ROOT:-$BIOKG_NEO4J_WORK_ROOT/native}"
DIST_ROOT="${BIOKG_NEO4J_DIST_ROOT:-$RUNTIME_ROOT/dist}"
DEFAULT_NEO4J_HOME="$DIST_ROOT/neo4j-community-$NEO4J_VERSION"
NEO4J_HOME_IS_CUSTOM=0
if [[ -n "${BIOKG_NEO4J_HOME+x}" ]]; then
  NEO4J_HOME_IS_CUSTOM=1
fi
NEO4J_HOME="${BIOKG_NEO4J_HOME:-$DEFAULT_NEO4J_HOME}"

CONF_DIR="${BIOKG_NEO4J_CONF_DIR:-$RUNTIME_ROOT/conf}"
DATA_DIR="${BIOKG_NEO4J_DATA_DIR:-$BIOKG_NEO4J_WORK_ROOT/data}"
LOG_DIR="${BIOKG_NEO4J_LOG_DIR:-$BIOKG_NEO4J_WORK_ROOT/logs}"
RUN_DIR="${BIOKG_NEO4J_RUN_DIR:-$RUNTIME_ROOT/run}"
PLUGIN_DIR="${BIOKG_NEO4J_PLUGIN_DIR:-$BIOKG_HOST_DIR/plugins}"
IMPORT_DIR="${BIOKG_NEO4J_IMPORT_DIR:-$BIOKG_WORK_ROOT/build/graph}"

LISTEN_ADDRESS="${BIOKG_NEO4J_LISTEN_ADDRESS:-127.0.0.1}"
ADVERTISED_ADDRESS="${BIOKG_NEO4J_ADVERTISED_ADDRESS:-127.0.0.1}"
HTTP_PORT="${BIOKG_NEO4J_HTTP_PORT:-7474}"
BOLT_PORT="${BIOKG_NEO4J_BOLT_PORT:-7687}"
HEAP_INITIAL="${BIOKG_NEO4J_HEAP_INITIAL:-512m}"
HEAP_MAX="${BIOKG_NEO4J_HEAP_MAX:-2G}"
PASSWORD="${BIOKG_NEO4J_PASSWORD:-biokgpassword}"

ARCHIVE_NAME="neo4j-community-$NEO4J_VERSION-unix.tar.gz"
ARCHIVE_PATH="$DIST_ROOT/$ARCHIVE_NAME"
DIST_URL="${BIOKG_NEO4J_DIST_URL:-https://dist.neo4j.org/$ARCHIVE_NAME}"
DIST_SHA256="${BIOKG_NEO4J_DIST_SHA256:-}"

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

validate_port() {
  local name="$1"
  local value="$2"
  if [[ ! "$value" =~ ^[0-9]+$ ]] || (( value < 1 || value > 65535 )); then
    die "$name must be an integer from 1 to 65535 (got '$value')"
  fi
}

validate_settings() {
  validate_port BIOKG_NEO4J_HTTP_PORT "$HTTP_PORT"
  validate_port BIOKG_NEO4J_BOLT_PORT "$BOLT_PORT"
  [[ "$HTTP_PORT" != "$BOLT_PORT" ]] || die "HTTP and Bolt ports must differ"
  [[ "$LISTEN_ADDRESS" != *$'\n'* ]] || die "listen address must be one line"
  [[ "$ADVERTISED_ADDRESS" != *$'\n'* ]] || die "advertised address must be one line"
}

neo4j_cmd() {
  env NEO4J_HOME="$NEO4J_HOME" NEO4J_CONF="$CONF_DIR" \
    "$NEO4J_HOME/bin/neo4j" "$@"
}

neo4j_admin_cmd() {
  env NEO4J_HOME="$NEO4J_HOME" NEO4J_CONF="$CONF_DIR" \
    "$NEO4J_HOME/bin/neo4j-admin" "$@"
}

neo4j_is_running() {
  [[ -x "$NEO4J_HOME/bin/neo4j" ]] && neo4j_cmd status >/dev/null 2>&1
}

http_ready() {
  curl -fsS --max-time 2 "http://127.0.0.1:$HTTP_PORT/" >/dev/null 2>&1
}

install_distribution() {
  if [[ -x "$NEO4J_HOME/bin/neo4j" && -x "$NEO4J_HOME/bin/neo4j-admin" ]]; then
    printf 'Neo4j %s is installed at %s\n' "$NEO4J_VERSION" "$NEO4J_HOME"
    return 0
  fi

  if (( NEO4J_HOME_IS_CUSTOM )); then
    die "BIOKG_NEO4J_HOME does not contain bin/neo4j and bin/neo4j-admin: $NEO4J_HOME"
  fi

  require_command curl
  require_command tar
  mkdir -p "$DIST_ROOT"

  if [[ ! -f "$ARCHIVE_PATH" ]]; then
    local partial_archive="$ARCHIVE_PATH.part.$$"
    printf 'Downloading %s\n' "$DIST_URL"
    if ! curl --fail --location --retry 3 --output "$partial_archive" "$DIST_URL"; then
      rm -f -- "$partial_archive"
      die "failed to download Neo4j from $DIST_URL"
    fi
    mv "$partial_archive" "$ARCHIVE_PATH"
  fi

  if [[ -n "$DIST_SHA256" ]]; then
    require_command sha256sum
    printf '%s  %s\n' "$DIST_SHA256" "$ARCHIVE_PATH" | sha256sum --check --status \
      || die "Neo4j archive checksum mismatch: $ARCHIVE_PATH"
  else
    printf 'No BIOKG_NEO4J_DIST_SHA256 set; relying on the HTTPS download.\n' >&2
  fi

  printf 'Extracting %s into %s\n' "$ARCHIVE_PATH" "$DIST_ROOT"
  tar -xzf "$ARCHIVE_PATH" -C "$DIST_ROOT"
  [[ -x "$NEO4J_HOME/bin/neo4j" && -x "$NEO4J_HOME/bin/neo4j-admin" ]] \
    || die "archive did not create the expected Neo4j home: $NEO4J_HOME"
  neo4j_cmd version
}

render_config() {
  local source_config="$NEO4J_HOME/conf/neo4j.conf"
  local target_config="$CONF_DIR/neo4j.conf"
  local temporary_config="$target_config.tmp.$$"
  local dropped_keys

  [[ -f "$source_config" ]] || die "Neo4j configuration template not found: $source_config"
  mkdir -p "$CONF_DIR" "$DATA_DIR" "$LOG_DIR" "$RUN_DIR" "$PLUGIN_DIR" "$IMPORT_DIR"

  dropped_keys="server.directories.data,server.directories.plugins,server.directories.logs,"
  dropped_keys+="server.directories.run,server.directories.import,"
  dropped_keys+="server.directories.transaction.logs.root,server.default_listen_address,"
  dropped_keys+="server.default_advertised_address,server.bolt.listen_address,"
  dropped_keys+="server.bolt.advertised_address,server.http.listen_address,"
  dropped_keys+="server.http.advertised_address,server.memory.heap.initial_size,"
  dropped_keys+="server.memory.heap.max_size,dbms.security.procedures.unrestricted,"
  dropped_keys+="dbms.security.procedures.allowlist,dbms.usage_report.enabled"

  awk -v dropped_keys="$dropped_keys" '
    BEGIN {
      count = split(dropped_keys, keys, ",")
      for (i = 1; i <= count; i++) {
        drop[keys[i]] = 1
      }
    }
    {
      normalized = $0
      sub(/^[[:space:]]*/, "", normalized)
      sub(/^#+[[:space:]]*/, "", normalized)
      key = normalized
      sub(/[[:space:]]*=.*/, "", key)
      if (!(key in drop)) {
        print
      }
    }
  ' "$source_config" > "$temporary_config"

  printf '\n# BioKG native launcher settings (regenerated by %s)\n' "$0" >> "$temporary_config"
  printf 'server.directories.data=%s\n' "$DATA_DIR" >> "$temporary_config"
  printf 'server.directories.plugins=%s\n' "$PLUGIN_DIR" >> "$temporary_config"
  printf 'server.directories.logs=%s\n' "$LOG_DIR" >> "$temporary_config"
  printf 'server.directories.run=%s\n' "$RUN_DIR" >> "$temporary_config"
  printf 'server.directories.import=%s\n' "$IMPORT_DIR" >> "$temporary_config"
  printf 'server.directories.transaction.logs.root=%s/transactions\n' "$DATA_DIR" \
    >> "$temporary_config"
  printf 'server.default_listen_address=%s\n' "$LISTEN_ADDRESS" >> "$temporary_config"
  printf 'server.default_advertised_address=%s\n' "$ADVERTISED_ADDRESS" \
    >> "$temporary_config"
  printf 'server.bolt.listen_address=%s:%s\n' "$LISTEN_ADDRESS" "$BOLT_PORT" \
    >> "$temporary_config"
  printf 'server.bolt.advertised_address=%s:%s\n' "$ADVERTISED_ADDRESS" "$BOLT_PORT" \
    >> "$temporary_config"
  printf 'server.http.listen_address=%s:%s\n' "$LISTEN_ADDRESS" "$HTTP_PORT" \
    >> "$temporary_config"
  printf 'server.http.advertised_address=%s:%s\n' "$ADVERTISED_ADDRESS" "$HTTP_PORT" \
    >> "$temporary_config"
  printf 'server.memory.heap.initial_size=%s\n' "$HEAP_INITIAL" >> "$temporary_config"
  printf 'server.memory.heap.max_size=%s\n' "$HEAP_MAX" >> "$temporary_config"
  printf 'dbms.security.procedures.unrestricted=apoc.*\n' >> "$temporary_config"
  printf 'dbms.security.procedures.allowlist=apoc.*\n' >> "$temporary_config"
  printf 'dbms.usage_report.enabled=false\n' >> "$temporary_config"
  mv "$temporary_config" "$target_config"

  local config_asset
  for config_asset in neo4j-admin.conf server-logs.xml user-logs.xml; do
    if [[ -f "$NEO4J_HOME/conf/$config_asset" ]]; then
      cp -f "$NEO4J_HOME/conf/$config_asset" "$CONF_DIR/$config_asset"
    fi
  done
}

initialize_password() {
  if [[ -s "$DATA_DIR/dbms/auth.ini" ]]; then
    return 0
  fi
  printf "Initializing password for Neo4j user 'neo4j'.\n"
  neo4j_admin_cmd dbms set-initial-password "$PASSWORD"
}

configure_runtime() {
  validate_settings
  require_command java
  install_distribution
  render_config
  neo4j_admin_cmd server validate-config
}

prepare_runtime() {
  configure_runtime
  initialize_password
  if ! compgen -G "$PLUGIN_DIR/apoc-*.jar" >/dev/null; then
    printf 'warning: no APOC jar found under %s; core BioKG loads still work without it.\n' \
      "$PLUGIN_DIR" >&2
  fi
}

print_status() {
  printf 'Neo4j home: %s\n' "$NEO4J_HOME"
  printf 'Config:     %s\n' "$CONF_DIR/neo4j.conf"
  printf 'Data:       %s\n' "$DATA_DIR"
  printf 'Logs:       %s\n' "$LOG_DIR"
  if [[ ! -x "$NEO4J_HOME/bin/neo4j" ]]; then
    printf 'Process:    not installed\n'
  elif neo4j_is_running; then
    neo4j_cmd status || true
  else
    printf 'Process:    not running\n'
  fi
  if http_ready; then
    printf 'HTTP:       reachable at http://127.0.0.1:%s/\n' "$HTTP_PORT"
  else
    printf 'HTTP:       not reachable at http://127.0.0.1:%s/\n' "$HTTP_PORT"
  fi
  printf 'Bolt:       bolt://127.0.0.1:%s\n' "$BOLT_PORT"
}

start_native() {
  require_command curl
  prepare_runtime
  if neo4j_is_running; then
    printf 'Neo4j is already running.\n'
    print_status
    return 0
  fi
  if http_ready; then
    die "HTTP port $HTTP_PORT is already in use by a process not owned by this launcher"
  fi

  neo4j_cmd start
  local attempt
  for attempt in $(seq 1 60); do
    if http_ready; then
      print_status
      return 0
    fi
    if ! neo4j_is_running; then
      show_logs 120 >&2
      die "Neo4j exited before its HTTP endpoint became ready"
    fi
    sleep 1
  done
  show_logs 120 >&2
  die "Neo4j did not become ready at http://127.0.0.1:$HTTP_PORT/ within 60 seconds"
}

run_console() {
  require_command curl
  prepare_runtime
  if neo4j_is_running; then
    die "Neo4j is already running; stop it before launching console mode"
  fi
  if http_ready; then
    die "HTTP port $HTTP_PORT is already in use by a process not owned by this launcher"
  fi
  exec env NEO4J_HOME="$NEO4J_HOME" NEO4J_CONF="$CONF_DIR" \
    "$NEO4J_HOME/bin/neo4j" console
}

stop_native() {
  if [[ ! -x "$NEO4J_HOME/bin/neo4j" ]]; then
    printf 'Neo4j is not installed at %s\n' "$NEO4J_HOME"
    return 0
  fi
  if [[ ! -f "$CONF_DIR/neo4j.conf" ]]; then
    printf 'Neo4j has no launcher configuration at %s\n' "$CONF_DIR/neo4j.conf"
    return 0
  fi
  if neo4j_is_running; then
    neo4j_cmd stop
  else
    printf 'Neo4j is not running.\n'
  fi
}

show_logs() {
  local lines="${1:-120}"
  [[ "$lines" =~ ^[1-9][0-9]*$ ]] || die "log line count must be a positive integer"
  if [[ ! -d "$LOG_DIR" ]]; then
    printf 'No log directory at %s\n' "$LOG_DIR"
    return 0
  fi

  local found=0
  local log_file
  while IFS= read -r -d '' log_file; do
    found=1
    printf '%s\n' "$log_file"
    tail -n "$lines" "$log_file"
  done < <(find "$LOG_DIR" -maxdepth 1 -type f -name '*.log' -print0 | sort -z)
  if (( ! found )); then
    printf 'No log files under %s\n' "$LOG_DIR"
  fi
}

usage() {
  cat <<EOF
Usage: $0 {install|configure|validate|up|console|down|status|list|logs [lines]}

Commands:
  install     Download Neo4j if needed, generate config, and initialize auth.
  configure   Generate config and initialize auth (also installs if missing).
  validate    Generate and validate config without initializing auth.
  up          Start Neo4j in daemon mode and wait for HTTP readiness.
  console     Run Neo4j in the foreground (recommended inside an HPC allocation).
  down        Stop the launcher-managed native Neo4j process.
  status/list Show installation, process, HTTP, and Bolt status.
  logs        Tail launcher-managed Neo4j logs (default: 120 lines).

Default browser: http://localhost:$HTTP_PORT/
Default auth:    neo4j / value of BIOKG_NEO4J_PASSWORD

Important environment overrides:
  BIOKG_NEO4J_VERSION             default: 5.26.27
  BIOKG_WORK_ROOT                 default: <release>/projections/biokg/_work
  BIOKG_NEO4J_NATIVE_ROOT         default: <work-root>/neo4j/native
  BIOKG_NEO4J_HOME                use an existing extracted Neo4j distribution
  BIOKG_NEO4J_DATA_DIR            default: <work-root>/neo4j/data
  BIOKG_NEO4J_LOG_DIR             default: <work-root>/neo4j/logs
  BIOKG_NEO4J_PLUGIN_DIR          default: <release>/projections/biokg/host/plugins
  BIOKG_NEO4J_IMPORT_DIR          default: <work-root>/build/graph
  BIOKG_NEO4J_HTTP_PORT           default: 7474
  BIOKG_NEO4J_BOLT_PORT           default: 7687
  BIOKG_NEO4J_LISTEN_ADDRESS      default: 127.0.0.1
  BIOKG_NEO4J_ADVERTISED_ADDRESS  default: 127.0.0.1
  BIOKG_NEO4J_PASSWORD            default: biokgpassword
  BIOKG_NEO4J_HEAP_INITIAL        default: 512m
  BIOKG_NEO4J_HEAP_MAX            default: 2G
  BIOKG_NEO4J_DIST_URL            override the pinned tarball URL
  BIOKG_NEO4J_DIST_SHA256         optional archive checksum

The native and Apptainer launchers use the same release-owned graph data by
default. Stop one backend before starting the other.
EOF
}

case "${1:-}" in
  install | configure)
    prepare_runtime
    print_status
    ;;
  validate)
    configure_runtime
    ;;
  up)
    start_native
    ;;
  console)
    run_console
    ;;
  down)
    stop_native
    ;;
  status | list)
    validate_settings
    print_status
    ;;
  logs)
    show_logs "${2:-120}"
    ;;
  help | --help | -h)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
