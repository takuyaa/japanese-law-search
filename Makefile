index:
	@poetry run python -m japanese_law_search index --path=data/

run:
	@poetry run streamlit run japanese_law_search/app.py

test:
	@poetry run python -m pytest tests
