mkfile_path := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
install:
	  uv sync
	  uv pip install -e .
		mkdir ~/.local/bin -p
		ln -sf ${mkfile_path}/.venv/bin/file_val ~/.local/bin
