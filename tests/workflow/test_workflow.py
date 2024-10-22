import subprocess
import pytest

pytestmark = pytest.mark.workflow


@pytest.fixture(scope="module", autouse=True)
def teardown():
    """全てのテストが完了した後にactで使用したコンテナを削除する"""
    yield
    cleanup_act_containers()


def run_act(jobname, filename, event_file):
    """指定されたイベントファイルでactを実行し、結果を返す"""
    try:
        result = subprocess.run(
            ["act", "-j", jobname, "-W", filename, "-e", event_file, "--reuse"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


def cleanup_act_containers():
    """actで使用したコンテナを削除する"""
    try:
        # actで使用したコンテナをリストアップ
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=act-", "--format", "{{.ID}}"],
            capture_output=True,
            text=True,
            check=True,
        )
        container_ids = result.stdout.strip().split("\n")

        # 各コンテナを削除
        for container_id in container_ids:
            if container_id:  # 空のIDを避ける
                subprocess.run(["docker", "stop", container_id], check=True)
                subprocess.run(["docker", "rm", container_id], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove act containers: {e}")


def test_publish_to_testpypi():
    events = [
        {"inputs": {"version": "v0.0.1", "recreate": "true", "dry_run": "true"}},
        {"inputs": {"version": "", "recreate": "true", "dry_run": "true"}},
        {"inputs": {"version": "", "recreate": "false", "dry_run": "true"}},
    ]
    jobname = "publish"
    filename = ".github/workflows/publish-to-testpypi.yaml"
    for event in events:
        import json
        import tempfile

        # 処理が終わったら一時ファイルを削除
        import os

        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(event, temp_file)
            temp_file_path = temp_file.name
            print(temp_file_path)

        output = run_act(jobname, filename, temp_file_path)
        os.remove(temp_file_path)
        # print(output)

        assert "Job succeeded" in output
    # cleanup_act_containers()


def test_publish_to_pypi():
    events = [
        {"inputs": {"version": "v0.0.1", "recreate": "true", "dry_run": "true"}},
        {"inputs": {"version": "", "recreate": "true", "dry_run": "true"}},
        {"inputs": {"version": "", "recreate": "false", "dry_run": "true"}},
    ]
    jobname = "publish"
    filename = ".github/workflows/publish-to-pypi.yaml"
    for event in events:
        import json
        import tempfile

        # 処理が終わったら一時ファイルを削除
        import os

        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(event, temp_file)
            temp_file_path = temp_file.name
            print(temp_file_path)

        output = run_act(jobname, filename, temp_file_path)
        os.remove(temp_file_path)
        # print(output)

        assert "Job succeeded" in output
    # cleanup_act_containers()


def test_update_version_sh():
    argument_cases = ["-v v0.0.1 -n", "-i patch -n"]

    for args in argument_cases:
        result = subprocess.run(
            f"bash .github/scripts/update_version.sh {args}",
            shell=True,
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"Script failed with args: {args}\n{result.stderr}"
