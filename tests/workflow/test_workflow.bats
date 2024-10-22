#!/usr/bin/env bats

setup() {
    # 一時ディレクトリを作成
    TMPDIR=$(mktemp -d)
}

teardown() {
    # 一時ディレクトリを削除
    rm -rf "$TMPDIR"
    cleanup_act_containers
}

run_act() {
    local jobname=$1
    local filename=$2
    local event_file=$3
    act -j "$jobname" -W "$filename" -e "$event_file" --reuse
}

cleanup_act_containers() {
    # actで使用したコンテナを停止して削除する
    docker ps -a --filter "name=act-" --format "{{.ID}}" | while read -r container_id; do
        docker stop "$container_id"  # コンテナを停止
        docker rm "$container_id"    # コンテナを削除
    done
}

@test "test_publish_to_testpypi" {
    events=(
        '{"inputs": {"version": "v0.0.1", "recreate": "true", "dry_run": "true"}}'
        '{"inputs": {"version": "", "recreate": "true", "dry_run": "true"}}'
        '{"inputs": {"version": "", "recreate": "false", "dry_run": "true"}}'
    )
    jobname='publish'
    filename='.github/workflows/publish-to-testpypi.yaml'

    for event in "${events[@]}"; do
        event_file="$TMPDIR/event.json"
        echo "$event" > "$event_file"
        
        run run_act "$jobname" "$filename" "$event_file"
        [ "$status" -eq 0 ]
        [[ "$output" == *"Job succeeded"* ]]
    done
}

@test "test_publish_to_pypi" {
    events=(
        '{"inputs": {"version": "v0.0.1", "recreate": "true", "dry_run": "true"}}'
        '{"inputs": {"version": "", "recreate": "true", "dry_run": "true"}}'
        '{"inputs": {"version": "", "recreate": "false", "dry_run": "true"}}'
    )
    jobname='publish'
    filename='.github/workflows/publish-to-pypi.yaml'

    for event in "${events[@]}"; do
        event_file="$TMPDIR/event.json"
        echo "$event" > "$event_file"
        
        run run_act "$jobname" "$filename" "$event_file"
        [ "$status" -eq 0 ]
        [[ "$output" == *"Job succeeded"* ]]
    done
}

@test "test_update_version_sh" {
    argument_cases=(
        "-v v0.0.1 -n"
        "-i patch -n"
    )

    for args in "${argument_cases[@]}"; do
        run bash .github/scripts/update_version.sh $args
        [ "$status" -eq 0 ]
    done
}
