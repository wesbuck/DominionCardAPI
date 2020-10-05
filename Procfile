release: cp DominionCardAPI/settings-sample.py DominionCardAPI/settings.py
release: python manage.py migrate
release: python manage.py ingest_csv dominion_cards.csv
