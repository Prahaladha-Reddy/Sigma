import contextvars
import shutil
import uuid
from pathlib import Path
from typing import Optional

_CURRENT_CONTEXT: contextvars.ContextVar["ProcessContext | None"] = contextvars.ContextVar(
    "process_context", default=None
)


class ProcessContext:
    """
    Manages per-request/process filesystem isolation.

    When used as a context manager, it:
    - Creates an isolated directory tree under processes/<process_id>/data/...
    - Sets a contextvar so downstream code can discover the active context
      without explicit parameter plumbing.
    - Optionally cleans up the directory tree on exit.
    """

    def __init__(
        self,
        process_id: Optional[str] = None,
        base_dir: str = "processes",
        cleanup: bool = True,
    ):
        self.process_id = process_id or str(uuid.uuid4())
        self.base_dir = Path(base_dir) / self.process_id
        self.data_dir = self.base_dir / "data"
        self.uploaded_dir = self.data_dir / "uploaded"
        self.analysis_dir = self.data_dir / "analysis"
        self.documents_dir = self.data_dir / "documents"
        self.notebook_dir = self.data_dir / "notebook"
        self.reports_dir = self.data_dir / "reports"
        self.cleanup = cleanup
        self._token = None

    @property
    def presentation_md(self) -> Path:
        return self.data_dir / "presentation.md"

    @property
    def final_story_md(self) -> Path:
        return self.data_dir / "Final_story.md"

    @property
    def final_slides_html(self) -> Path:
        return self.data_dir / "Final_slides.html"

    def ensure_dirs(self):
        for d in [
            self.data_dir,
            self.uploaded_dir,
            self.analysis_dir,
            self.documents_dir,
            self.notebook_dir,
            self.reports_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)

    def activate(self):
        """
        Set this context as current without using the context manager.
        Returns a token that can be passed to reset_current().
        """
        self.ensure_dirs()
        return _CURRENT_CONTEXT.set(self)

    def __enter__(self):
        self.ensure_dirs()
        self._token = _CURRENT_CONTEXT.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._token is not None:
            _CURRENT_CONTEXT.reset(self._token)
            self._token = None
        if self.cleanup:
            shutil.rmtree(self.base_dir, ignore_errors=True)

    @classmethod
    def get_current(cls) -> Optional["ProcessContext"]:
        return _CURRENT_CONTEXT.get()

    @classmethod
    def use(cls, ctx: Optional["ProcessContext"]):
        """
        Manually set the current context for code paths that don't use
        the context manager.
        """
        _CURRENT_CONTEXT.set(ctx)


def reset_current(token):
    if token is not None:
        _CURRENT_CONTEXT.reset(token)


def get_data_dir() -> Path:
    """
    Resolve the active data directory, falling back to the legacy ./data.
    """
    ctx = ProcessContext.get_current()
    if ctx:
        ctx.ensure_dirs()
        return ctx.data_dir
    return Path("data")


def get_uploaded_dir() -> Path:
    ctx = ProcessContext.get_current()
    if ctx:
        ctx.ensure_dirs()
        return ctx.uploaded_dir
    return Path("data") / "uploaded"


def get_analysis_dir() -> Path:
    ctx = ProcessContext.get_current()
    if ctx:
        ctx.ensure_dirs()
        return ctx.analysis_dir
    return Path("data") / "analysis"


def get_documents_dir() -> Path:
    ctx = ProcessContext.get_current()
    if ctx:
        ctx.ensure_dirs()
        return ctx.documents_dir
    return Path("data") / "documents"


def get_notebook_dir() -> Path:
    ctx = ProcessContext.get_current()
    if ctx:
        ctx.ensure_dirs()
        return ctx.notebook_dir
    return Path("data") / "notebook"


def get_reports_dir() -> Path:
    ctx = ProcessContext.get_current()
    if ctx:
        ctx.ensure_dirs()
        return ctx.reports_dir
    return Path("data") / "reports"
