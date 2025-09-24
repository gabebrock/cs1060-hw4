# Homework 4 
*due September 29, 9 pm ET:*

## API Prototyping with Generative AI (50 points)

*Please follow all instructions carefully.* Although there is a lot of detail in the instructions, the implementation is straightforward, especially if you start with a working system like the existing API from the cs1060-hw2-base Links to an external site. example.

**You should work alone on this assignment.** You may use any generative AI or other online resources you like, excluding any materials by or discussions with other students in this course (and of course you may not pay other people to do it for you.) You must indicate in your code files where you obtained any code, whether from GenAI, StackOverflow, or your friend's dog.

There are two data sources you will need for this assignment, which are CSV data sources from the following free public data sources:

- RowZero Zip Code to County (based on public data sets) https://rowzero.io/blog/zip-code-to-state-county-metro
    - CSV Data: (Feb 2025) `zip_county.csv`

- County Health Rankings & Roadmaps Analytic Data https://www.countyhealthrankings.org/health-data
    - CSV Data: (Feb 2025) `county_health_rankings.csv`

### Part 1: Data Processing (15 points)

Use generative AI to create a Python 3 script called csv_to_sqlite.py.

- It should accept valid CSV files with a header row of field names (these should be valid SQL column names, with no escaping or spaces).
- Behavior on bad CSV is undefined.
- On valid inputs, it should output a sqlite3 database called data.db.
- sqlite3 works on Windows, Mac, and Linux.
- Your script should take two arguments: the name of your sqlite3 database and the name of the CSV file.
- 💡 Using GPT-4o in the Harvard Sandbox, this task took course staff 15 minutes, with one prompt and one change. The AI output SQL commands with column names in quotes instead of bare SQL, which needed to be altered. Your prompt and model may well get it right the first time.

Here is an example of how you might implement a basic test for your script.

```bash
cat$ rm data.db
cat$ python3 csv_to_sqlite.py data.db zip_county.csv
cat$ python3 csv_to_sqlite.py data.db county_health_rankings.csv
cat$ sqlite3 data.db 
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .schema zip_county
CREATE TABLE zip_county (zip TEXT, default_state TEXT, county TEXT, county_state TEXT, 
    state_abbreviation TEXT, county_code TEXT, zip_pop TEXT, zip_pop_in_county TEXT, 
    n_counties TEXT, default_city TEXT);
sqlite> select count(*) from zip_county;
54553
sqlite> .schema county_health_rankings 
CREATE TABLE county_health_rankings (state TEXT, county TEXT, state_code TEXT, 
    county_code TEXT, year_span TEXT, measure_name TEXT, measure_id TEXT, numerator TEXT, 
    denominator TEXT, raw_value TEXT, confidence_interval_lower_bound TEXT, 
    confidence_interval_upper_bound TEXT, data_release_year TEXT, fipscode TEXT);
sqlite> select count(*) from county_health_rankings;
303864
sqlite> .q
```
## Part 2: API Prototype (35 points)

Create an API prototype with a county_data endpoint that uses the data.db you generated in Part 1, and host it on your choice of platforms—Netlify, Vercel, Render, Bolt, Lovable, ... they're all fine.

You can use the `cs1060-hw2-base` example from HW2 as a way to easily get started deploying to Vercel. If you choose to use Vercel on a free/hobby plan, keep in mind you'll have to copy it to your own private GitHub instead of the cs1060f25 organization, and copy/clone that repo into the cs1060 organization for submission.

Here is one way to test an API endpoint:

```bash
cat$ curl -H'content-type:application/json' \
  -d'{"input": "five", "inputType": "text", "outputType": "decimal"}' \
  https://cat-hw2-render.onrender.com/convert
```

This should yield the following output:

```json
{"error":null,"result":"5"}
```

You can use `https://cat-hw2-render.onrender.com/convert` to play with an example endpoint; note it only accepts `POST` requests and navigating to it with a browser will send a `GET` request. If you want to use a more powerful API testing tool, you might like the Postman Links to an external site. application which has a free offering.

The `county_data` endpoint should have the following behavior:

It should accept an HTTP POST with key/value pairs in JSON, using the `content-type:application/json` header and JSON inputs. See above example.
It should output all applicable results in JSON, using the same schema as the county_health_rankings database. A subset of the output from input `{"zip":"02138","measure_name":"Adult obesity"}` would look like:

```json
[
  {
    "confidence_interval_lower_bound": "0.22",
    "confidence_interval_upper_bound": "0.24",
    "county": "Middlesex County",
    "county_code": "17",
    "data_release_year": "2012",
    "denominator": "263078",
    "fipscode": "25017",
    "measure_id": "11",
    "measure_name": "Adult obesity",
    "numerator": "60771.02",
    "raw_value": "0.23",
    "state": "MA",
    "state_code": "25",
    "year_span": "2009"
  },
  {
    "confidence_interval_lower_bound": "0.224",
    "confidence_interval_upper_bound": "0.242",
    "county": "Middlesex County",
    "county_code": "17",
    "data_release_year": "2014",
    "denominator": "1143459.228",
    "fipscode": "25017",
    "measure_id": "11",
    "measure_name": "Adult obesity",
    "numerator": "266426",
    "raw_value": "0.233",
    "state": "MA",
    "state_code": "25",
    "year_span": "2010"
  }
]
```

The `zip` key in the POST data is required, and is a 5-digit ZIP code.
The `measure_name` in the POST data is required, and should be one of the following strings:

- Violent crime rate
- Unemployment
- Children in poverty
- Diabetic screening
- Mammography screening
- Preventable hospital stays
- Uninsured
- Sexually transmitted infections
- Physical inactivity
- Adult obesity
- Premature Death
- Daily fine particulate matter

If the `coffee=teapot` key=value pair is supplied in the POST data, the request should return HTTP error code 418. [Learn more. Links to an external site.] This supersedes any other behavior.

Not supplying both `zip` and `measure_name` should yield a 400 (bad request) error.
Supplying a zip/measure_name pair that does not exist in the data, or an endpoint other than county_data, should yield a 404 (not found) error.

You may choose to implement the query as two separate queries, or use a database join. Providing the schema to your generative AI system may help you.

It should sanitize any inputs when creating SQL queries.

## Submission requirements:

In Canvas, submit a link to a private GitHub repository in the cs1060f25 organization. It should be in the format `<username>-hw4`, as before.
Your repository should be a copy of what you deployed.
Your repository must have the following files:

- `./link.txt`
- `./csv_to_sqlite.py`
- `./requirements.txt` (if needed)
- `./README.md`
- `./.gitignore`

Your implementation structure is up to you, and may depend on where you deploy it. If you are deploying to Vercel, you might have a `vercel.json` file and an `api` directory.

Your `.gitignore` file may be simple, preventing caches from being checked in, or boilerplate. See for example [this discussion](https://stackoverflow.com/questions/3719243/best-practices-for-adding-gitignore-file-for-python-projects) or
[https://github.com/github/gitignore/blob/main/Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore).

Your `link.txt` file should contain only a URL that points to your API endpoint, but nothing in the query string. An example endpoint (not implemented) might be
`https://myuser-cs1060-hw4.vercel.app/county_data`.

## How we will grade HW4:

Because this is an API assignment, Homework 4 will be graded by scripts and AI. We will:

- check out your repository from GitHub
- automatically run your csv_to_sqlite.py program on the original data sources (do not change the CSV files!)
- automatically run your `csv_to_sqlite.py `program on other data sources not provided to you, to ensure it works on arbitrary CSV files and is not hard-coding the provided data sources
- follow the endpoint in link.txt to your deployed API to test its functionality according to the specification. We will also verify that your link.txt is unique.
- We may attempt a SQL injection attack against your endpoint, which could lead to destructive operations on your database which we would be able to detect with further queries. We will only do this after all other tests are complete. Submitting this assignment implies your consent to this penetration test.

You should test all this on your own using a fresh directory. Completely following the specification will yield full credit; we will not be looking into the implementation beyond whether it works or doesn't work. Therefore, testing your software thoroughly before you submit it is extremely important. Going without a test suite is like walking a tightrope without a net, but it's up to you.