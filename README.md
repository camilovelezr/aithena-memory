# How to use it
1. Create a directory called `.data`
2. Save `sample.env` as `.env` and fill in the missing fields
3. Start postgres with pgvector: `docker compose up`
4. Run the test script to initialize all the tables, generate a vector, and insert