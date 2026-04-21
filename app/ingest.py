"""
CLI entrypoint for batch document ingestion.

Usage (inside the container):
    python -m app.ingest                        # ingest /app/data (default)
    python -m app.ingest --data-dir /app/data   # explicit path
    python -m app.ingest --file /app/data/foo.pdf
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import structlog

from app.ingestion.pipeline import ingest_directory, ingest_file

logger = structlog.get_logger(__name__)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest documents into the HealthTech RAG vector store."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--data-dir",
        type=Path,
        default=Path("/app/data"),
        help="Directory to recursively ingest (default: /app/data)",
    )
    group.add_argument(
        "--file",
        type=Path,
        default=None,
        help="Single file to ingest instead of a directory",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if args.file is not None:
        if not args.file.is_file():
            logger.error("file_not_found", path=str(args.file))
            return 1
        chunks = ingest_file(args.file)
        logger.info("file_ingestion_done", file=str(args.file), chunks=chunks)
        return 0

    data_dir: Path = args.data_dir
    if not data_dir.is_dir():
        logger.error("directory_not_found", path=str(data_dir))
        return 1

    results = ingest_directory(data_dir)
    # ingest_directory returns -1 for files that failed to ingest
    total = sum(n for n in results.values() if n >= 0)
    failed = [f for f, n in results.items() if n < 0]
    logger.info(
        "directory_ingestion_done",
        directory=str(data_dir),
        files_processed=len(results),
        total_chunks=total,
        failed=failed,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
