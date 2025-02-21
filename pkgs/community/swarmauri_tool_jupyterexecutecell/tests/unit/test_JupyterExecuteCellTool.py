import pytest
import subprocess
import atexit
import time
import swarmauri_tool_jupyterexecutecell.JupyterExecuteCellTool as ject
from swarmauri_tool_jupyterexecutecell.JupyterExecuteCellTool import (
    JupyterExecuteCellTool,
)


def test_tool_initialization():
    """
    Test the initialization of JupyterExecuteCellTool, verifying its default attributes.
    """
    tool = JupyterExecuteCellTool()
    assert tool.name == "JupyterExecuteCellTool", "Tool name should match."
    assert tool.version == "1.0.0", "Tool version should be '1.0.0'."
    assert (
        tool.description == "Executes code cells within a Jupyter kernel environment."
    )

    assert (
        tool.type == "JupyterExecuteCellTool"
    ), "Tool type should be 'JupyterExecuteCellTool'."
    assert (
        len(tool.parameters) == 2
    ), "There should be two default parameters: code, timeout."


def test_tool_parameters():
    """
    Test that the tool's parameter list includes the expected attributes.
    """
    tool = JupyterExecuteCellTool()
    param_names = [param.name for param in tool.parameters]
    assert "code" in param_names, "Parameters must include 'code'."
    assert "timeout" in param_names, "Parameters must include 'timeout'."


def test_tool_call_basic_execution(monkeypatch):
    """
    Test that the tool can execute a simple print statement and capture its output.
    """

    # Mock the get_ipython function to return a dummy shell for testing purposes.
    class DummyShell:
        def run_cell(self, code, **kwargs):
            print(
                "Hello, world!"
            )  # This seems to solve the issue of getting nothing in the std output
            return {"stdout": "Hello, world!", "stderr": "", "error": ""}

    monkeypatch.setattr(
        target=JupyterExecuteCellTool,
        name="get_ipython",
        value=lambda *args, **kwargs: DummyShell(),
    )

    tool = JupyterExecuteCellTool()
    result = tool("print('Hello, world!')")
    assert (
        "Hello, world!" in result["stdout"]
    ), "Expected code execution output not found in stdout."
    assert result["stderr"] == "", "stderr should be empty when executing valid code."
    assert result["error"] == "", "error should be empty when executing valid code."


def test_tool_call_syntax_error(monkeypatch):
    """
    Test that the tool captures Python syntax errors appropriately.
    """

    # Mock the get_ipython function to return a dummy shell for testing purposes.
    class DummyShell:
        def run_cell(self, code, **kwargs):
            raise SyntaxError("Mocked syntax error")

    monkeypatch.setattr(
        target=JupyterExecuteCellTool,
        name="get_ipython",
        value=lambda *args, **kwargs: DummyShell(),
    )

    tool = JupyterExecuteCellTool()
    result = tool("print('Missing parenthesis'")
    assert (
        "SyntaxError" in result["error"]
    ), "Expected a SyntaxError in the error field."
    assert result["stderr"] != "", "stderr should capture syntax error details."


def test_tool_call_timeout(monkeypatch):
    """
    Test that the tool handles code execution timeouts and returns an appropriate error message.
    """

    # Mock the get_ipython function to return a dummy shell for testing purposes.
    class DummyShell:
        def run_cell(self, code, **kwargs):
            time.sleep(3)  # Simulate long execution time
            return {"stdout": "", "stderr": "", "error": ""}

    monkeypatch.setattr(
        target=JupyterExecuteCellTool,
        name="get_ipython",
        value=lambda *args, **kwargs: DummyShell(),
    )

    tool = JupyterExecuteCellTool()
    result = tool("import time; time.sleep(3)", timeout=1)
    assert (
        "Execution timed out after 1 seconds." in result["error"]
    ), "Expected timeout error message."

    assert result["stdout"] == "", "stdout should be empty on timeout."
    assert result["stderr"] == "", "stderr should be empty on timeout."


def test_tool_call_no_active_kernel(monkeypatch):
    """
    Test that the tool reports an error when there is no active IPython kernel.
    """

    class DummyGetIPython:
        def __call__(self, *args, **kwargs):
            return None

    # Patch the module-level get_ipython in the JupyterExecuteCellTool module so that it returns None.
    monkeypatch.setattr(JupyterExecuteCellTool, "get_ipython", DummyGetIPython())

    tool = JupyterExecuteCellTool()
    result = tool("print('Hello')", timeout=1)

    # Expect the tool to signal that no kernel is active.
    assert (
        result["stderr"] == "No active IPython kernel found."
    ), "Expected stderr to indicate no active IPython kernel."
    assert (
        result["error"] == "KernelNotFoundError"
    ), "Expected error to be 'KernelNotFoundError'."
    assert result["stdout"] == "", "stdout should be empty when no kernel is found."


def test_tool_call_exception_during_execution(monkeypatch):
    """
    Test that the tool captures and logs exceptions raised during code execution.
    """

    # Define a dummy shell whose run_cell method always raises an exception.
    class DummyShellThatRaises:
        def run_cell(self, code, **kwargs):
            raise RuntimeError("Mocked runtime error")

    # Patch the module-level get_ipython in the JupyterExecuteCellTool module to return our dummy shell.
    monkeypatch.setattr(
        ject, "get_ipython", lambda *args, **kwargs: DummyShellThatRaises()
    )

    tool = JupyterExecuteCellTool()
    result = tool("print('Testing exception')")
    assert (
        "Mocked runtime error" in result["error"]
    ), "Expected mocked runtime error in the error field."
    assert (
        "RuntimeError" in result["error"]
    ), "Expected 'RuntimeError' text in error field."
    assert result["stderr"] != "", "stderr should capture exception details."
    assert (
        "Testing exception" not in result["stdout"]
    ), "stdout should not have content from failing command."
