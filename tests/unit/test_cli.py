import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from fastmango.cli.main import app


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.mark.unit
def test_cli_help(runner):
    """Test that CLI help command works."""
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "FastMango" in result.stdout
    assert "Commands" in result.stdout


@pytest.mark.unit
def test_cli_version(runner):
    """Test that CLI version command works."""
    result = runner.invoke(app, ["--version"])
    
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


@pytest.mark.unit
def test_cli_run_help(runner):
    """Test that run command help works."""
    result = runner.invoke(app, ["run", "--help"])
    
    assert result.exit_code == 0
    assert "--host" in result.stdout
    assert "--port" in result.stdout
    assert "--reload" in result.stdout


@pytest.mark.unit
def test_cli_new_help(runner):
    """Test that new command help works."""
    result = runner.invoke(app, ["new", "--help"])
    
    assert result.exit_code == 0
    assert "name" in result.stdout
    assert "--template" in result.stdout


@pytest.mark.unit
@patch('fastmango.cli.run.uvicorn.run')
@patch('fastmango.cli.run.Path')
def test_cli_run_default(mock_path, mock_uvicorn_run, runner):
    """Test run command with default parameters."""
    # Mock the Path.exists() to return True
    mock_path.return_value.exists.return_value = True
    mock_uvicorn_run.return_value = None
    
    result = runner.invoke(app, ["run"])
    
    assert result.exit_code == 0
    mock_uvicorn_run.assert_called_once()
    
    # Check that default parameters were passed
    call_args = mock_uvicorn_run.call_args
    assert "app" in str(call_args)
    assert call_args.kwargs.get("host") == "127.0.0.1"
    assert call_args.kwargs.get("port") == 8000


@pytest.mark.unit
@patch('fastmango.cli.run.uvicorn.run')
@patch('fastmango.cli.run.Path')
def test_cli_run_with_custom_params(mock_path, mock_uvicorn_run, runner):
    """Test run command with custom parameters."""
    # Mock the Path.exists() to return True
    mock_path.return_value.exists.return_value = True
    mock_uvicorn_run.return_value = None
    
    result = runner.invoke(app, [
        "run",
        "--host", "0.0.0.0",
        "--port", "9000",
        "--reload"
    ])
    
    assert result.exit_code == 0
    mock_uvicorn_run.assert_called_once()
    
    # Check that custom parameters were passed
    call_args = mock_uvicorn_run.call_args
    assert call_args.kwargs.get("host") == "0.0.0.0"
    assert call_args.kwargs.get("port") == 9000
    assert call_args.kwargs.get("reload") is True


@pytest.mark.unit
@patch('fastmango.cli.new.pathlib.Path.cwd')
@patch('fastmango.cli.new.pathlib.Path')
def test_cli_new_project(mock_path, mock_cwd, runner, tmp_path):
    """Test new project creation."""
    # Mock current working directory
    mock_cwd.return_value = tmp_path
    
    # Create a mock project directory path
    project_path = tmp_path / "test-project"
    
    # Mock Path constructor to return our mock path
    mock_path.return_value = project_path
    
    result = runner.invoke(app, ["new", "test-project"])
    
    assert result.exit_code == 0
    assert "test-project" in result.stdout


@pytest.mark.unit
@patch('fastmango.cli.new.pathlib.Path.cwd')
@patch('fastmango.cli.new.pathlib.Path')
def test_cli_new_project_with_template(mock_path, mock_cwd, runner, tmp_path):
    """Test new project creation with custom template."""
    # Mock current working directory
    mock_cwd.return_value = tmp_path
    
    # Create a mock project directory path
    project_path = tmp_path / "test-project"
    
    # Mock Path constructor to return our mock path
    mock_path.return_value = project_path
    
    result = runner.invoke(app, [
        "new", 
        "test-project",
        "--template", "basic"  # Use basic template since advanced doesn't exist
    ])
    
    assert result.exit_code == 0
    assert "test-project" in result.stdout


@pytest.mark.unit
def test_cli_new_project_no_name(runner):
    """Test new project creation without name fails."""
    result = runner.invoke(app, ["new"])
    
    assert result.exit_code != 0
    # Check for either "Missing argument" or typer's error message in stderr
    assert "Missing argument" in result.stderr or "Usage:" in result.stderr or "Error:" in result.stderr or "Aborted" in result.stderr